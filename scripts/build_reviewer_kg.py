#!/usr/bin/env python3
"""Build, update, and query the reviewer knowledge graph (standard library only).

The graph joins prior review findings from the review store (~/reviews) with the
reference guidance in this repository (reference/). It is written as a
Graphify-compatible graph.json so `graphify query|explain|path --graph` work on it.

Commands:
  build   parse every review store and reference doc, write the graph
  update  reparse only stores and reference docs whose files changed
  match   rank prior findings and reference docs against a claim, file, or diff
"""
import argparse
import hashlib
import json
import math
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

AGENTS_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REVIEWS = Path.home() / 'reviews'
DEFAULT_REFERENCE = AGENTS_ROOT / 'reference'
DEFAULT_OUT = Path.home() / 'agents-secret' / 'kg' / 'reviewer'
DEFAULT_LOG_ROOT = Path.home() / 'review-kg'  # per-run debug logs of /kg-review
REFERENCE_CATEGORIES = ['anti-patterns', 'design-principles', 'design-patterns', 'security-principles']
SKIP_REFERENCE_NAMES = {'CHECKLIST.md', 'README.md', 'index.md'}
FORMAT_VERSION = 1

# Finding-type prefixes from review/REVIEW_METHOD.md § ID prefixes.
TYPE_NAMES = {'B': 'BUG', 'SEC': 'SECURITY', 'I': 'ISSUE', 'S': 'SCOPING_AUTH', 'O': 'OPTIMIZATION',
              'D': 'DESIGN', 'T': 'TEST', 'M': 'MINOR'}
FIELD = re.compile(r'^([a-z][a-z0-9-]*):(.*)$')
DETAIL_NAME = re.compile(r'^((?:SEC|[BISODTM])\d+)\.([0-9A-Za-z]+)\.md$')
SUMMARY_LINE = re.compile(r'^- \[.\] ((?:SEC|[BISODTM])\d+\.[0-9A-Za-z]+) - (\S+(?: verified:\S+)?) \[([A-Z]+)\] - (.*)$')
WORD = re.compile(r'[A-Za-z][A-Za-z0-9_]+')
CAMEL = re.compile(r'(?<=[a-z0-9])(?=[A-Z])')
STOPWORDS = set('''
the and for with that this from are was were not but you your our its into onto than then them they
there their which when what where who will would should could can may might must does did has have had
been being also only just any all each every one two per via use used uses using after before over under
more most less other such same some very new now out off how why yes see set get got make made does
file line code test tests pr review reviewer claim finding issue current head commit fix fixed status
http https www com github pull pullrequestreview issuecomment japan inc'''.split())
SIMILAR_TOP_K = 5
SIMILAR_MIN_SCORE = 0.25
REFERENCE_TOP_K = 3
REFERENCE_MIN_SCORE = 0.12
REFERENCE_TITLE_BOOST = 0.3
REFERENCE_BOOST_FLOOR = 0.05  # a title hit only boosts a doc whose body also matches
REFERENCE_LINK_MIN_SCORE = 0.2  # build-time exemplifies links; stricter than interactive match
VECTOR_TERMS = 40
STEERING_TOP_K = 3
STEERING_MIN_SCORE = 0.2
REFERENCE_VECTOR_TERMS = 150  # long guidance docs keep more terms

# Outcome of a prior decision, from the status token.
OUTCOMES = {
    'CLOSED': 'fixed',
    'WILL_NOT_FIX': 'rejected',
    'OUT_OF_SCOPE': 'out-of-scope',
    'UNPROVEN': 'not-reproduced',
    'INVALIDATED_INGESTION_ERROR': 'invalid',
    'OBSOLETE': 'obsolete',
    'DEFERRED': 'deferred',
}


def sha256_text(text):
    return hashlib.sha256(text.encode()).hexdigest()


def tokens(text):
    out = []
    for word in WORD.findall(text or ''):
        parts = CAMEL.sub(' ', word).replace('_', ' ').split()
        if len(parts) > 1:
            out.append(word.lower())  # keep the whole identifier: OrderModeService is more specific than its parts
        for part in parts:
            low = part.lower()
            if len(low) >= 3 and low not in STOPWORDS and not low.isdigit():
                out.append(stem(low))
    return out


def stem(word):
    """Light suffix stripping so swallows/swallowing/swallowed share a term."""
    for suffix in ('ing', 'ed', 'es', 's'):
        if len(word) - len(suffix) >= 4 and word.endswith(suffix):
            return word[:-len(suffix)]
    return word


class ReferenceIndex:
    """TF-IDF over reference docs only, so finding vocabulary does not dilute guidance terms.
    A query term in a doc's title or alias adds a boost."""

    def __init__(self, refs):
        self.refs = refs
        self.model = TfIdf([' '.join([r['title']] * 3 + list(r.get('aliases', [])) + [r.get('text', '')]) for r in refs],
                           [REFERENCE_VECTOR_TERMS] * len(refs))
        self.titles = [set(tokens(' '.join([r['title']] + list(r.get('aliases', []))))) for r in refs]

    def rank(self, text, top, min_score=None):
        min_score = REFERENCE_MIN_SCORE if min_score is None else min_score
        query = self.model.query(text)
        scores = self.model.scores(query)
        terms = set(query)
        for i, title in enumerate(self.titles):
            hits = len(terms & title)
            if hits and scores.get(i, 0) >= REFERENCE_BOOST_FLOOR:
                scores[i] += REFERENCE_TITLE_BOOST * hits / len(title)
        return sorted(((s, i) for i, s in scores.items() if s >= min_score), reverse=True)[:top]


def parse_detail(text):
    """Parse an <ID>.md detail file into {key: value | [values]} (repeated keys become lists)."""
    fields, key, buf = {}, None, []

    def flush():
        if key is None:
            return
        value = '\n'.join(buf).strip()
        if key in fields:
            prev = fields[key]
            fields[key] = (prev if isinstance(prev, list) else [prev]) + [value]
        else:
            fields[key] = value

    in_fence = False
    for line in text.splitlines():
        if line.startswith('```'):
            in_fence = not in_fence
            buf.append(line)
            continue
        match = None if in_fence else FIELD.match(line)
        # A wrapped URL line (`https://...`) continues the current field.
        if match and not match.group(2).startswith('//'):
            flush()
            key, buf = match.group(1), [match.group(2)]
        elif key is not None:
            buf.append(line)
    flush()
    return fields


def first(value):
    if isinstance(value, list):
        return value[-1] if value else ''
    return value or ''


def strip_ticks(value):
    return first(value).strip().strip('`').strip()


def parse_meta_and_summary(text):
    meta, summary, section = {}, {}, None
    for line in text.splitlines():
        if line.startswith('# '):
            section = line[2:].strip()
            continue
        if section == 'META':
            match = FIELD.match(line)
            if match:
                meta[match.group(1)] = match.group(2).strip()
        elif section == 'SUMMARY':
            match = SUMMARY_LINE.match(line.strip())
            if match:
                summary[match.group(1)] = dict(status=match.group(2), severity=match.group(3), title=match.group(4))
    return meta, summary


def store_signature(store):
    """Hash of names, sizes, and mtimes of the store files; changes when any file changes."""
    parts = []
    for path in sorted(store.glob('*.md')):
        stat = path.stat()
        parts.append(f'{path.name}:{stat.st_size}:{stat.st_mtime_ns}')
    return sha256_text('\n'.join(parts))


def split_file_ref(raw):
    """`path/to/x.ts:36` -> ('path/to/x.ts', '36'); takes the first backticked path when several."""
    raw = first(raw)
    ticked = re.findall(r'`([^`]+)`', raw)
    ref = (ticked[0] if ticked else raw).strip()
    match = re.match(r'^(.*?):(\d+)(?:-\d+)?$', ref)
    return (match.group(1), match.group(2)) if match else (ref, '')


def outcome_of(status):
    head = (status or '').split()[0] if status else ''
    head = head.split(':')[0] if not head.startswith('NEEDS_REVIEW') else head
    return OUTCOMES.get(head, 'undecided')


def parse_store(store):
    review = store / 'review.md'
    meta, summary = parse_meta_and_summary(review.read_text(errors='replace'))
    repo = meta.get('repo', '') or store.name.rsplit('-pr-', 1)[0]
    pr = meta.get('pr', '')
    findings = []
    for path in sorted(store.glob('*.md')):
        match = DETAIL_NAME.match(path.name)
        if not match:
            continue
        detail = parse_detail(path.read_text(errors='replace'))
        full_id = f'{match.group(1)}.{match.group(2)}'
        row = summary.get(full_id, {})
        status = first(detail.get('status')) or row.get('status', '')
        file_path, file_line = split_file_ref(detail.get('file', ''))
        prefix = re.match(r'^(SEC|[A-Z])', full_id).group(1)
        findings.append(dict(
            id=full_id, store=store.name, repo=repo, pr=pr or strip_ticks(detail.get('pr')).lstrip('#'),
            type=TYPE_NAMES.get(prefix, prefix),
            severity=first(detail.get('severity')) or row.get('severity', ''),
            status=status, outcome=outcome_of(status),
            title=first(detail.get('title')) or row.get('title', ''),
            file=file_path, line=file_line,
            description=first(detail.get('description')),
            evidence=first(detail.get('evidence')),
            fix=first(detail.get('fix')), fixed=first(detail.get('fixed')),
            justification=first(detail.get('justification')),
            reviewer_ack=first(detail.get('reviewer-ack')),
            pushback=first(detail.get('pushback')),
            reply=first(detail.get('reply')), triage=first(detail.get('triage')),
            scope=first(detail.get('scope')),
            commit=first(detail.get('commit')),
            reviewer=first(detail.get('reviewer')), source=first(detail.get('source')),
            thread=first(detail.get('thread')),
            cascade_of=first(detail.get('cascade-of')),
            path=str(path),
        ))
    return dict(store=store.name, repo=repo, pr=pr, branch=meta.get('branch', ''),
                reviewed=meta.get('reviewed', ''), findings=findings, decisions=parse_task_decisions(store))


TASK_DECISION = re.compile(r'^- (\d{4}-\d{2}-\d{2}) - ([a-z0-9][a-z0-9-]*) - (.+)$')


def parse_task_decisions(store):
    """The user's steering decisions from `task.md` `# DECISIONS` (review/TASK_FILE.md grammar)."""
    path = store / 'task.md'
    if not path.is_file():
        return []
    decisions, section = [], None
    for line in path.read_text(errors='replace').splitlines():
        if line.startswith('# '):
            section = line[2:].strip()
        elif section == 'DECISIONS':
            match = TASK_DECISION.match(line.strip())
            if match:
                decisions.append(dict(date=match.group(1), name=match.group(2), text=match.group(3)))
    return decisions


def parse_reference(path, root):
    text = path.read_text(errors='replace')
    title = next((line[2:].strip() for line in text.splitlines() if line.startswith('# ')), path.stem)
    aliases = []
    also = re.search(r'\*\*Also known as:\*\*\s*(.+)', text)
    if also:
        aliases = [a.strip() for a in also.group(1).split(',') if a.strip()]
    rel = path.relative_to(root.parent).as_posix()
    return dict(path=rel, category=path.relative_to(root).parts[0], title=title, aliases=aliases,
                text=text, digest=sha256_text(text))


def reference_files(root):
    for category in REFERENCE_CATEGORIES:
        base = root / category
        if base.is_dir():
            for path in sorted(base.rglob('*.md')):
                if path.name not in SKIP_REFERENCE_NAMES:
                    yield path


def finding_text(finding):
    return ' '.join([finding['title'], finding['title'], finding['description'], finding['evidence'],
                     finding['fix'], finding['fixed'], finding.get('justification', ''), finding['file']])


class TfIdf:
    """Sparse TF-IDF vectors over a document list, truncated to the top terms per document."""

    def __init__(self, docs, limits=None):
        self.df = Counter()
        counts = [Counter(tokens(doc)) for doc in docs]
        for count in counts:
            self.df.update(count.keys())
        self.n = max(len(docs), 1)
        limits = limits or [VECTOR_TERMS] * len(docs)
        self.vectors = [self.vector(count, limit) for count, limit in zip(counts, limits)]
        self.index = defaultdict(list)
        for doc_id, vec in enumerate(self.vectors):
            for term, weight in vec.items():
                self.index[term].append((doc_id, weight))

    def vector(self, count, limit=VECTOR_TERMS):
        weights = {t: (1 + math.log(c)) * math.log((self.n + 1) / (self.df.get(t, 0) + 1)) for t, c in count.items()}
        top = dict(sorted(weights.items(), key=lambda kv: -kv[1])[:limit])
        norm = math.sqrt(sum(w * w for w in top.values())) or 1.0
        return {t: w / norm for t, w in top.items() if w > 0}

    def query(self, text):
        return self.vector(Counter(tokens(text)))

    def scores(self, vec):
        acc = defaultdict(float)
        for term, weight in vec.items():
            for doc_id, doc_weight in self.index.get(term, ()):
                acc[doc_id] += weight * doc_weight
        return acc


def finding_node_id(finding):
    return f"finding:{finding['store']}/{finding['id']}"


def build_graph(stores, references, memory=()):
    nodes, links = {}, []

    def node(node_id, **attrs):
        nodes.setdefault(node_id, dict(id=node_id, **attrs))

    def link(source, target, relation, confidence='EXTRACTED', score=1.0, **attrs):
        # Graphify filters traversal on `context`; set it to the relation so `--context similar_to` works.
        links.append(dict(source=source, target=target, relation=relation, context=relation, confidence=confidence,
                          confidence_score=round(score, 4), weight=round(score, 4), _origin='reviewer_kg', **attrs))

    findings = [f for store in stores for f in store['findings']]
    for store in stores:
        repo_id = f"repo:{store['repo']}"
        node(repo_id, label=store['repo'], kind='repo', file_type='repo')
        store_id = f"store:{store['store']}"
        node(store_id, label=store['store'], kind='review_store', file_type='review', repo=store['repo'],
             pr=store['pr'], branch=store['branch'], reviewed=store['reviewed'])
        link(store_id, repo_id, 'in_repo')
        for decision in store.get('decisions', []):
            decision_id = f"steering:{store['store']}/{decision['name']}"
            node(decision_id, label=f"steering {decision['name']}", kind='steering', file_type='decision',
                 store=store['store'], repo=store['repo'], date=decision['date'], name=decision['name'],
                 text=decision['text'], confidence='verified', source_file=f"{store['store']}/task.md")
            link(decision_id, store_id, 'steers')
    for finding in findings:
        fid = finding_node_id(finding)
        node(fid, label=f"{finding['id'].split('.')[0]} {finding['title']}"[:160], kind='finding', file_type='finding',
             finding_id=finding['id'], **{k: v for k, v in finding.items() if k not in ('id', 'path')},
             source_file=finding['path'])
        link(fid, f"store:{finding['store']}", 'in_store')
        if finding['file']:
            file_id = f"file:{finding['repo']}:{finding['file']}"
            node(file_id, label=finding['file'], kind='code_file', file_type='code', repo=finding['repo'])
            link(fid, file_id, 'touches', source_location=f"L{finding['line']}" if finding['line'] else '')
        if finding['reviewer']:
            reviewer_id = f"reviewer:{finding['reviewer']}"
            node(reviewer_id, label=finding['reviewer'], kind='reviewer', file_type='actor')
            link(fid, reviewer_id, 'raised_by')
        node(f"outcome:{finding['outcome']}", label=finding['outcome'], kind='outcome', file_type='decision')
        link(fid, f"outcome:{finding['outcome']}", 'decided_as')
    by_store_id = {(f['store'], f['id']): f for f in findings}
    for finding in findings:
        if finding['cascade_of']:
            parent = by_store_id.get((finding['store'], finding['cascade_of'].strip().strip('`')))
            if parent:
                link(finding_node_id(finding), finding_node_id(parent), 'cascade_of')
    for ref in references:
        ref_id = f"reference:{ref['path']}"
        node(ref_id, label=ref['title'], kind='reference', file_type='document', category=ref['category'],
             aliases=ref['aliases'], source_file=ref['path'], text=ref['text'][:4000])
        cat_id = f"reference_category:{ref['category']}"
        node(cat_id, label=ref['category'], kind='reference_category', file_type='document')
        link(ref_id, cat_id, 'in_category')

    # Finding -> finding similarity and finding -> reference matching (INFERRED, scored).
    finding_docs = [finding_text(f) for f in findings]
    model = TfIdf(finding_docs)
    ref_index = ReferenceIndex(references)
    n_find = len(findings)
    ref_name_patterns = []
    for ref in references:
        names = [n for n in [ref['title']] + ref['aliases'] if re.search(r'[\s-]', n.strip()) and len(n) > 6]
        patterns = [re.compile(r'(?<![\w-])' + re.escape(n.lower()) + r'(?![\w-])') for n in names]
        if patterns:
            ref_name_patterns.append((ref, patterns))
    for i, finding in enumerate(findings):
        scores = model.scores(model.vectors[i])
        ranked = sorted(((s, j) for j, s in scores.items() if j != i), reverse=True)
        sims = [(s, j) for s, j in ranked if j < n_find and s >= SIMILAR_MIN_SCORE][:SIMILAR_TOP_K]
        refs = ref_index.rank(finding_docs[i], REFERENCE_TOP_K, REFERENCE_LINK_MIN_SCORE)
        for score, j in sims:
            link(finding_node_id(finding), finding_node_id(findings[j]), 'similar_to', 'INFERRED', score)
        for score, j in refs:
            link(finding_node_id(finding), f"reference:{references[j]['path']}", 'exemplifies', 'INFERRED', score)
        # An explicit multi-word name or alias in the claim text is an extracted link.
        # Single-word names (Adapter, Command) collide with ordinary code words, so they only link by similarity.
        claim = ' '.join([finding['title'], finding['description'], finding['fix'], finding['fixed'],
                          finding['justification']]).lower()
        for ref, patterns in ref_name_patterns:
            if any(p.search(claim) for p in patterns):
                link(finding_node_id(finding), f"reference:{ref['path']}", 'cites')
    # Steering decisions link to the findings they read like, so a traversal from a claim reaches them.
    for steer in (n for n in list(nodes.values()) if n['kind'] == 'steering'):
        scores = model.scores(model.query(f"{steer['name'].replace('-', ' ')} {steer['text']}"))
        for score, j in sorted(((s, j) for j, s in scores.items() if s >= STEERING_MIN_SCORE), reverse=True)[:STEERING_TOP_K]:
            link(finding_node_id(findings[j]), steer['id'], 'steered_by', 'INFERRED', score)
    add_memory(nodes, link, memory)
    return dict(directed=True, multigraph=True,
                graph=dict(name='reviewer_kg', format_version=FORMAT_VERSION,
                           built_at=datetime.now(timezone.utc).isoformat(timespec='seconds'),
                           stores=len(stores), findings=n_find, references=len(references)),
                nodes=list(nodes.values()), links=links, hyperedges=[])


# --- Memory: append-only decisions that add to or supersede prior results -------------------------

MEMORY_FILE = 'memory.jsonl'
MEMORY_KINDS = ('decision', 'supersede', 'note')
MEMORY_REQUIRED = ('id', 'at', 'kind', 'rationale')
# Fixed vocabularies, rejected at write time and checked by lint (no drift).
OUTCOME_VOCAB = tuple(sorted(set(OUTCOMES.values()) | {'undecided'}))
CONFIDENCE_VOCAB = ('verified', 'hypothesis', 'reported')  # human-confirmed / agent-inferred / external claim
CANONICAL_STATUS = re.compile(
    r'^(OPEN|NEEDS_REVIEW:(reviewer|coder|cascade|external)|DEFERRED|CLOSED verified:\d{4}-\d{2}-\d{2}'
    r'|WILL_NOT_FIX|OUT_OF_SCOPE|UNPROVEN)$')
ACCEPTED = {'fixed'}
DECLINED = {'rejected', 'out-of-scope', 'not-reproduced', 'invalid'}
CONFLICT_MIN_SCORE = 0.5


def memory_node_id(entry_id):
    return f'memory:{entry_id}'


def read_memory(out):
    """Return (entries, problems). Lines are never rewritten; a bad line is reported by lint."""
    path = out / MEMORY_FILE
    entries, problems = [], []
    if not path.is_file():
        return entries, problems
    for number, line in enumerate(path.read_text().splitlines(), 1):
        if not line.strip():
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError as error:
            problems.append(f'{MEMORY_FILE}:{number}: invalid JSON ({error.msg})')
            continue
        missing = [k for k in MEMORY_REQUIRED if not entry.get(k)]
        if missing or entry.get('kind') not in MEMORY_KINDS:
            problems.append(f"{MEMORY_FILE}:{number}: missing {missing or 'valid kind'}")
            continue
        entry['_line'] = number
        entries.append(entry)
    return entries, problems


def add_memory(nodes, link, memory):
    """Memory entries become nodes; `supersedes` keeps the old item and links the newer one to it."""
    for entry in memory:
        mid = memory_node_id(entry['id'])
        nodes.setdefault(mid, dict(
            id=mid, label=f"{entry['kind']}: {entry.get('title') or entry['rationale']}"[:160], kind='memory',
            file_type='decision', memory_id=entry['id'], memory_kind=entry['kind'], at=entry['at'],
            title=entry.get('title', ''), outcome=entry.get('outcome', ''), confidence=entry.get('confidence', ''),
            fix=entry.get('fix', ''),
            rationale=entry['rationale'], source=entry.get('source', ''), author=entry.get('author', ''),
            about=entry.get('about', []), supersedes=entry.get('supersedes', []), by=entry.get('by', ''),
            source_file=MEMORY_FILE, source_location=f"L{entry['_line']}"))
        for target in entry.get('about', []):
            link(mid, target, 'about')
        newer = entry.get('by') or mid
        if entry.get('by'):
            link(mid, newer, 'records')
        for old in entry.get('supersedes', []):
            link(newer, old, 'supersedes', recorded_by=mid, at=entry['at'])
            if old in nodes:
                nodes[old].setdefault('superseded_by', [])
                if newer not in nodes[old]['superseded_by']:
                    nodes[old]['superseded_by'].append(newer)


def current_of(node_id, nodes, seen=None):
    """Follow superseded_by to the newest item(s); stops on cycles (lint reports them)."""
    seen = seen or set()
    if node_id in seen:
        return [node_id]
    seen.add(node_id)
    newer = nodes.get(node_id, {}).get('superseded_by', [])
    if not newer:
        return [node_id]
    return [c for n in newer for c in current_of(n, nodes, set(seen))]


def supersede_reaches(start, goal, nodes):
    """True when following superseded_by from start arrives back at goal."""
    stack, seen = list(nodes.get(start, {}).get('superseded_by', [])), set()
    while stack:
        current = stack.pop()
        if current == goal:
            return True
        if current not in seen:
            seen.add(current)
            stack.extend(nodes.get(current, {}).get('superseded_by', []))
    return False


def resolve_node(token, nodes):
    """Accept a node id, a memory id, `store/ID`, or a full finding ID that is unique."""
    for candidate in (token, f'finding:{token}', memory_node_id(token)):
        if candidate in nodes:
            return candidate
    hits = [n['id'] for n in nodes.values() if n.get('finding_id') == token]
    if len(hits) == 1:
        return hits[0]
    raise SystemExit(f'Cannot resolve {token!r}: ' + (f'ambiguous, use one of {hits}' if hits else 'no such node'))


def load_graph(out):
    path = out / 'graph.json'
    if not path.is_file():
        raise SystemExit(f'No graph at {path}; run build first')
    return json.loads(path.read_text())


def cmd_remember(args):
    out = Path(args.out).expanduser()
    graph = load_graph(out)
    nodes = {n['id']: n for n in graph['nodes']}
    about = [resolve_node(t, nodes) for t in args.about or []]
    supersedes = [resolve_node(t, nodes) for t in args.supersedes or []]
    by = resolve_node(args.by, nodes) if args.by else ''
    if args.kind == 'supersede' and not supersedes:
        raise SystemExit('supersede needs --supersedes')
    at = datetime.now(timezone.utc).isoformat(timespec='seconds')
    body = dict(at=at, kind=args.kind, about=about, supersedes=supersedes, by=by, title=args.title or '',
                outcome=args.outcome or '', confidence=args.confidence, fix=args.fix or '', rationale=args.rationale,
                source=args.source or '', author=args.author or '')
    entry = dict(id='mem-' + sha256_text(json.dumps(body, sort_keys=True))[:12], **body)
    out.mkdir(parents=True, exist_ok=True)
    with (out / MEMORY_FILE).open('a') as handle:
        handle.write(json.dumps(entry, ensure_ascii=False) + '\n')
    print(json.dumps(dict(remembered=entry['id'], kind=entry['kind'], about=about, supersedes=supersedes, by=by)))
    if not args.no_update:
        cmd_build(args, incremental=True)


def lint(out, reviews):
    """Return {check: [messages]}; checks prefixed E are errors, W are warnings."""
    graph = load_graph(out)
    nodes = {n['id']: n for n in graph['nodes']}
    memory, problems = read_memory(out)
    report = defaultdict(list)
    report['E1 memory format'] += problems
    ids = Counter(e['id'] for e in memory)
    report['E1 memory format'] += [f'duplicate memory id {i}' for i, c in ids.items() if c > 1]
    for entry in memory:
        for field in ('about', 'supersedes'):
            for target in entry.get(field, []):
                if target not in nodes:
                    report['E2 dangling reference'].append(f"{entry['id']} {field} {target}: not in graph")
        if entry.get('by') and entry['by'] not in nodes:
            report['E2 dangling reference'].append(f"{entry['id']} by {entry['by']}: not in graph")
        if entry.get('outcome') and entry['outcome'] not in OUTCOME_VOCAB:
            report['E4 vocabulary'].append(f"{entry['id']} outcome {entry['outcome']!r} not in {OUTCOME_VOCAB}")
        if entry.get('confidence') not in CONFIDENCE_VOCAB:
            report['E4 vocabulary'].append(f"{entry['id']} confidence {entry.get('confidence')!r} not in {CONFIDENCE_VOCAB}")
    for node_id, node in nodes.items():
        if supersede_reaches(node_id, node_id, nodes):
            report['E3 supersede cycle'].append(f'{node_id} is superseded by an item it supersedes')
        live = [n for n in node.get('superseded_by', []) if not nodes.get(n, {}).get('superseded_by')]
        if len(live) > 1:
            report['W1 supersede fork'].append(f'{node_id} superseded by {len(live)} current items: {live}')
    seen_pairs = set()
    for link in graph['links']:
        if link['relation'] != 'similar_to' or link['confidence_score'] < CONFLICT_MIN_SCORE:
            continue
        pair_key = frozenset((link['source'], link['target']))
        if pair_key in seen_pairs:
            continue
        seen_pairs.add(pair_key)
        a, b = nodes[link['source']], nodes[link['target']]
        pair = {a.get('outcome'), b.get('outcome')}
        if pair & ACCEPTED and pair & DECLINED and not a.get('superseded_by') and not b.get('superseded_by'):
            report['W2 conflicting decisions'].append(
                f"{a['finding_id']} ({a['outcome']}) vs {b['finding_id']} ({b['outcome']}) "
                f"similarity {link['confidence_score']}: record which decision holds")
    for node in nodes.values():
        if node['kind'] != 'finding':
            continue
        if node.get('outcome') == 'fixed' and not (node.get('fixed') or node.get('fix')):
            report['W3 fixed without fix text'].append(f"{node['store']}/{node['finding_id']}")
        if node.get('status') and not CANONICAL_STATUS.match(node['status']):
            report['W4 non-canonical status'].append(f"{node['store']}/{node['finding_id']}: {node['status']}")
    cache = load_cache(out)
    for review in sorted(reviews.glob('*/review.md')):
        cached = cache['stores'].get(review.parent.name)
        if not cached:
            report['W5 stale graph'].append(f'{review.parent.name}: store not in graph; run update')
        elif cached['signature'] != store_signature(review.parent):
            report['W5 stale graph'].append(f'{review.parent.name}: changed since build; run update')
        if cached:
            have = {f['id'] for f in cached['data']['findings']}
            _, summary = parse_meta_and_summary(review.read_text(errors='replace'))
            for missing in sorted(set(summary) - have):
                report['W6 summary row without detail file'].append(f'{review.parent.name}/{missing}')
    return {k: v for k, v in sorted(report.items()) if v}


# --- Run log: why /kg-review did what it did --------------------------------------------------------

LOG_KINDS = ('understanding', 'kept', 'dropped', 'prior_decision', 'reference', 'steering', 'prejudgement',
             'decision', 'proposal', 'user_response', 'ruling', 'applied', 'gap', 'note')
EVENTS_FILE = 'events.jsonl'


def slug(text, limit=40):
    return re.sub(r'[^a-z0-9]+', '-', (text or 'run').lower()).strip('-')[:limit] or 'run'


def append_event(run, **event):
    if not (run / 'meta.json').is_file():
        raise SystemExit(f'No run at {run}; start one with run-start')
    event = dict(at=datetime.now(timezone.utc).isoformat(timespec='seconds'), **event)
    with (run / EVENTS_FILE).open('a') as handle:
        handle.write(json.dumps(event, ensure_ascii=False) + '\n')
    return event


def claim_slug(report, args):
    claim = report.get('claim')
    if claim:
        return f"{claim['store']}__{claim['id']}"
    return 'query-' + sha256_text(json.dumps([args.text, args.files], default=str))[:8]


def log_match(run, args, report):
    """Save the full match result and log what the KG found for this claim."""
    name = claim_slug(report, args)
    (run / f'{name}.match.json').write_text(json.dumps(report, indent=2, ensure_ascii=False))
    append_event(run, claim=name, kind='kg_match', text='KG retrieval and ranking',
                 data=dict(graphify_output=args.graphify, files=report['files'], query_terms=report['query_terms'],
                           prejudgement=report['prejudgement'],
                           priors=[dict(id=r['id'], store=r['store'], score=r['score'], outcome=r['outcome'],
                                        retrieved_by=r['retrieved_by'], superseded_by=r['superseded_by'],
                                        rulings=[c['id'] for c in r['rulings']], title=r['title'])
                                   for r in report['findings']],
                           steering=[dict(name=st['name'], store=st['store'], score=st['score']) for st in report['steering']],
                           references=report['references'],
                           match_file=f'{name}.match.json'))


def cmd_run_start(args):
    root = Path(args.log_root).expanduser()
    run = root / f"{datetime.now().strftime('%Y%m%d-%H%M%S')}-{slug(args.target)}"
    run.mkdir(parents=True, exist_ok=False)
    meta = dict(target=args.target, started=datetime.now(timezone.utc).isoformat(timespec='seconds'),
                cwd=str(Path.cwd()), agent=args.agent or '', graph=str(Path(args.out).expanduser() / 'graph.json'))
    (run / 'meta.json').write_text(json.dumps(meta, indent=2))
    (run / EVENTS_FILE).touch()
    print(run)


def cmd_log(args):
    run = Path(args.run).expanduser()
    event = append_event(run, claim=args.claim, kind=args.kind, text=args.text,
                         evidence=args.evidence or [], refs=args.ref or [])
    print(json.dumps(dict(logged=event['kind'], claim=event['claim'], run=str(run))))


def cmd_run_report(args):
    run = Path(args.run).expanduser()
    meta = json.loads((run / 'meta.json').read_text())
    events = [json.loads(line) for line in (run / EVENTS_FILE).read_text().splitlines() if line.strip()]
    by_claim = defaultdict(list)
    for event in events:
        by_claim[event.get('claim') or 'run'].append(event)
    lines = [f"# KG review run {run.name}", '', f"- target: {meta['target']}", f"- started: {meta['started']}",
             f"- agent: {meta.get('agent') or 'unknown'}", f"- cwd: `{meta['cwd']}`", f"- graph: `{meta['graph']}`",
             f'- events: {len(events)}', '']
    for claim, items in by_claim.items():
        lines += [f'## {claim}', '']
        for event in items:
            if event['kind'] == 'kg_match':
                d = event['data']
                pj = d['prejudgement']
                lines += ['### KG found', '', f"- match file: `{d['match_file']}`",
                          f"- graphify output: `{d['graphify_output'] or 'none (text only)'}`",
                          f"- pre-judgement: {pj['basis']} / {pj['verdict'] or 'none'} / ask={pj['ask']}"]
                lines += [f"- prior {p['id']} ({p['store']}) {p['outcome']} score {p['score']} via {p['retrieved_by']}"
                          f"{' superseded' if p['superseded_by'] else ''}{' rulings ' + ','.join(p['rulings']) if p['rulings'] else ''}"
                          f": {p['title'][:120]}" for p in d['priors']]
                lines += [f"- steering {st['name']} ({st['store']}) score {st['score']}" for st in d['steering']]
                lines += [f"- reference {r['title']} ({r['score']}) `{r['path']}`" for r in d['references']]
                lines.append('')
            else:
                lines.append(f"### {event['kind']} ({event['at']})")
                lines += ['', f"- {' '.join(event['text'].split())}"]
                lines += [f'- evidence: {e}' for e in event.get('evidence', [])]
                lines += [f'- uses: {r}' for r in event.get('refs', [])]
                lines.append('')
    (run / 'run.md').write_text('\n'.join(lines) + '\n')
    print(run / 'run.md')


def cmd_lint(args):
    report = lint(Path(args.out).expanduser(), Path(args.reviews).expanduser())
    errors = sum(len(v) for k, v in report.items() if k.startswith('E'))
    if args.format == 'json':
        print(json.dumps(dict(errors=errors, checks=report), indent=2, ensure_ascii=False))
    else:
        print(f"# Reviewer KG lint\n\n- errors: {errors}\n- warnings: {sum(len(v) for k, v in report.items() if k.startswith('W'))}\n")
        for check, messages in report.items():
            print(f'## {check} ({len(messages)})\n')
            for message in messages[:args.limit]:
                print(f'- {message}')
            if len(messages) > args.limit:
                print(f'- … {len(messages) - args.limit} more (use --limit or --format json)')
            print()
    if errors:
        raise SystemExit(1)


def load_cache(out):
    path = out / 'cache.json'
    if path.is_file():
        cache = json.loads(path.read_text())
        if cache.get('format_version') == FORMAT_VERSION:
            return cache
    return dict(format_version=FORMAT_VERSION, stores={}, references={})


def collect(reviews, reference, out, incremental):
    cache = load_cache(out) if incremental else dict(format_version=FORMAT_VERSION, stores={}, references={})
    stores, reparsed, live = [], 0, set()
    for review in sorted(reviews.glob('*/review.md')):
        store = review.parent
        live.add(store.name)
        signature = store_signature(store)
        cached = cache['stores'].get(store.name)
        if cached and cached['signature'] == signature:
            stores.append(cached['data'])
            continue
        data = parse_store(store)
        cache['stores'][store.name] = dict(signature=signature, data=data)
        stores.append(data)
        reparsed += 1
    removed = sorted(set(cache['stores']) - live)
    for name in removed:
        del cache['stores'][name]
    references, ref_reparsed = [], 0
    for path in reference_files(reference):
        rel = path.relative_to(reference.parent).as_posix()
        digest = sha256_text(path.read_text(errors='replace'))
        cached = cache['references'].get(rel)
        if cached and cached['digest'] == digest:
            references.append(cached)
            continue
        ref = parse_reference(path, reference)
        cache['references'][rel] = ref
        references.append(ref)
        ref_reparsed += 1
    for rel in set(cache['references']) - {r['path'] for r in references}:
        del cache['references'][rel]
    return stores, references, cache, dict(stores_reparsed=reparsed, stores_removed=removed,
                                           references_reparsed=ref_reparsed)


def write_outputs(out, graph, cache):
    out.mkdir(parents=True, exist_ok=True)
    (out / 'graph.json').write_text(json.dumps(graph, ensure_ascii=False))
    (out / 'cache.json').write_text(json.dumps(cache, ensure_ascii=False))
    counts = Counter(n['kind'] for n in graph['nodes'])
    relations = Counter(l['relation'] for l in graph['links'])
    outcomes = Counter(n.get('outcome') for n in graph['nodes'] if n['kind'] == 'finding')
    lines = ['# Reviewer KG', '', f"- built: {graph['graph']['built_at']}",
             f"- stores: {graph['graph']['stores']}", f"- findings: {graph['graph']['findings']}",
             f"- references: {graph['graph']['references']}", '', '## Nodes', '']
    lines += [f'- {kind}: {n}' for kind, n in sorted(counts.items())]
    lines += ['', '## Links', ''] + [f'- {rel}: {n}' for rel, n in sorted(relations.items())]
    lines += ['', '## Finding outcomes', ''] + [f'- {o}: {n}' for o, n in sorted(outcomes.items())]
    lines += ['', '## Memory', '', f"- entries: {counts.get('memory', 0)}",
              f"- superseded items: {sum(1 for n in graph['nodes'] if n.get('superseded_by'))}"]
    (out / 'REPORT.md').write_text('\n'.join(lines) + '\n')
    return counts, relations


def cmd_build(args, incremental):
    out = Path(args.out).expanduser()
    stores, references, cache, delta = collect(Path(args.reviews).expanduser(), Path(args.reference).expanduser(),
                                               out, incremental)
    memory, problems = read_memory(out)
    graph = build_graph(stores, references, memory)
    graph['graph']['memory'] = len(memory)
    counts, relations = write_outputs(out, graph, cache)
    superseded = sum(1 for n in graph['nodes'] if n.get('superseded_by'))
    print(json.dumps(dict(out=str(out / 'graph.json'), nodes=len(graph['nodes']), links=len(graph['links']),
                          findings=graph['graph']['findings'], references=graph['graph']['references'],
                          memory=len(memory), superseded=superseded, memory_problems=len(problems),
                          **delta), indent=2))


SUPERSEDED_WEIGHT = 0.5
UNDECIDED_WEIGHT = 0.85  # orders an open prior below a decided one of similar score


def candidate_text(node):
    if node['kind'] == 'steering':
        return f"{node['name'].replace('-', ' ')} {node['text']}"
    if node['kind'] == 'memory':
        return ' '.join([node.get('title', '')] * 2 + [node.get('rationale', ''), node.get('fix', '')])
    return finding_text(node)


def decision_summary(node):
    return dict(id=node.get('finding_id') or node.get('memory_id') or node['id'], node=node['id'],
                kind=node['kind'], outcome=node.get('outcome', ''), confidence=node.get('confidence', ''),
                title=node.get('title', ''), fix=node.get('fix', ''), rationale=node.get('rationale', ''),
                summary=node.get('fixed') or node.get('fix') or node.get('rationale') or node.get('justification', ''))


PREJUDGE_RULING_MIN = 0.3   # a verified user ruling at or above this score decides the handling
PREJUDGE_PRIOR_MIN = 0.35   # prior findings at or above this score form a hypothesis
PREJUDGE_CONFLICT_GAP = 0.1  # rulings within this score of the top with another outcome are a conflict


def prejudge(results):
    """Pre-judgement from matches: a current verified user ruling decides; agreeing priors suggest; else none.

    A superseded match contributes its current decision, so a ruling that replaced an old result still applies."""
    rulings = []
    for r in results:
        if not r['superseded_by'] and r['type'] == 'MEMORY' and r['confidence'] == 'verified':
            rulings.append(dict(score=r['score'], id=r['id'], outcome=r['outcome'], title=r['title'],
                                handling=r['fix'] or r['rationale'], rationale=r['rationale'], via=r['id']))
        for c in r['current_decision'] + r['rulings']:
            if c['kind'] == 'memory' and c['confidence'] == 'verified':
                rulings.append(dict(score=r['score'], id=c['id'], outcome=c['outcome'], title=c['title'],
                                    handling=c['fix'] or c['rationale'], rationale=c['rationale'], via=r['id']))
    rulings = [x for x in sorted(rulings, key=lambda x: -x['score']) if x['score'] >= PREJUDGE_RULING_MIN]
    if rulings:
        top = rulings[0]
        rivals = [x for x in rulings[1:] if x['outcome'] != top['outcome'] and x['id'] != top['id']
                  and top['score'] - x['score'] <= PREJUDGE_CONFLICT_GAP]
        if rivals:
            return dict(verdict='conflict', basis='user-rulings', ask=True, rulings=[top] + rivals,
                        instruction='Rulings disagree; show both and ask which holds, then supersede the other.')
        return dict(verdict=top['outcome'], basis='user-ruling', ask=False, ruling=top,
                    instruction='Follow this ruling without asking how to handle it; cite the ruling id.')
    priors = [r for r in results if not r['superseded_by'] and r['type'] != 'MEMORY'
              and r['outcome'] not in ('', 'undecided') and r['score'] >= PREJUDGE_PRIOR_MIN][:3]
    if priors:
        outcomes = Counter(r['outcome'] for r in priors)
        outcome, count = outcomes.most_common(1)[0]
        return dict(verdict=outcome if count == len(priors) else 'mixed', basis='prior-findings', ask=True,
                    priors=[dict(id=r['id'], store=r['store'], outcome=r['outcome'], score=r['score'], fix=r['fixed'] or r['fix'],
                                 justification=r['justification']) for r in priors],
                    instruction='No user ruling yet; propose this as a hypothesis and ask once, then remember the answer.')
    return dict(verdict=None, basis='none', ask=True,
                instruction='No prior decision; research the issue, propose a fix, ask once, then remember the answer.')


GRAPH_RETRIEVAL_BONUS = 0.05


def graphify_candidates(source, nodes):
    """Node ids named in `graphify query` output: detail-file `src=` paths, else exact node labels."""
    text = sys.stdin.read() if source == '-' else Path(source).read_text(errors='replace')
    by_src, by_label = defaultdict(set), defaultdict(set)
    for n in nodes.values():
        if n.get('source_file'):
            by_src[n['source_file']].add(n['id'])
        by_label[n.get('label', '')].add(n['id'])
    found = set()
    for line in text.splitlines():
        match = re.match(r'^NODE (.*?) \[src=([^\]]*?) loc=', line)
        if not match:
            continue
        label, src = match.group(1).strip(), match.group(2).strip()
        hits = by_label.get(label, set()) & by_src.get(src, set()) or by_label.get(label, set())
        found |= hits
    return found


def read_query(args):
    parts = []
    if args.text:
        parts.append(args.text)
    if args.query_file:
        parts.append(Path(args.query_file).read_text(errors='replace'))
    if args.diff:
        diff = Path(args.diff).read_text(errors='replace') if args.diff != '-' else sys.stdin.read()
        parts.append('\n'.join(line[1:] for line in diff.splitlines()
                               if line.startswith('+') and not line.startswith('+++')))
        args.files = (args.files or []) + re.findall(r'^\+\+\+ b/(\S+)', diff, re.M)
    if not parts and not args.files:
        raise SystemExit('match needs --text, --query-file, --diff, --file, or --finding')
    return '\n'.join(parts)


BOT_REVIEWER = re.compile(r'\[bot\]|\bbot\b|agent|github-actions|\bgpt\b|claude|codex|copilot|coderabbit', re.I)


def reviewer_kind(reviewer):
    """bot, human, or unknown; a bot's suggested fix is a hint to check, not a decision."""
    if not reviewer:
        return 'unknown'
    return 'bot' if BOT_REVIEWER.search(reviewer) else 'human'


def claim_from_reviews(token, reviews):
    """Read a claim that is not in the graph yet straight from its review store (read-only, no rebuild)."""
    store_name, _, full_id = token.replace('finding:', '').partition('/')
    store = reviews / store_name
    if not full_id or not (store / 'review.md').is_file():
        return None
    for finding in parse_store(store)['findings']:
        if finding['id'] == full_id:
            return dict(id=finding_node_id(finding), finding_id=finding['id'], in_graph=False,
                        **{k: v for k, v in finding.items() if k not in ('id', 'path')}, source_file=finding['path'])
    return None


def stale_stores(graph_dir, reviews):
    """Review stores changed after the graph was built."""
    graph_file = graph_dir / 'graph.json'
    if not graph_file.is_file() or not reviews.is_dir():
        return []
    built = graph_file.stat().st_mtime
    return sorted(s.name for s in reviews.iterdir()
                  if (s / 'review.md').is_file() and max(p.stat().st_mtime for p in s.glob('*.md')) > built)


def cmd_match(args):
    graph = load_graph(Path(args.out).expanduser())
    nodes = {n['id']: n for n in graph['nodes']}
    findings = [n for n in graph['nodes'] if n['kind'] == 'finding'
                or (n['kind'] == 'memory' and n['memory_kind'] in ('decision', 'supersede'))]
    refs = {n['id']: n for n in graph['nodes'] if n['kind'] == 'reference'}
    linked_refs = defaultdict(list)
    for l in graph['links']:
        if l['relation'] in ('exemplifies', 'cites') and l['target'] in refs:
            linked_refs[l['source']].append((l['confidence_score'], refs[l['target']]['label'], refs[l['target']]['source_file']))
    rulings_about = defaultdict(list)  # finding node -> memory entries recorded about it
    for n in graph['nodes']:
        if n['kind'] == 'memory' and n['memory_kind'] in ('decision', 'supersede'):
            for target in n.get('about', []):
                rulings_about[target].append(n['id'])
    claim = None
    if args.finding:
        try:
            claim = nodes[resolve_node(args.finding, nodes)]
        except SystemExit:
            claim = claim_from_reviews(args.finding, Path(args.reviews).expanduser())
            if claim is None:
                raise SystemExit(f'Cannot resolve {args.finding!r}: not in the graph and not in {args.reviews}')
        args.text = ' '.join(filter(None, [args.text, finding_text(claim)]))
        args.files = (args.files or []) + ([claim['file']] if claim.get('file') else [])
    query = read_query(args)
    files = [f.split(':')[0] for f in (args.files or [])]
    steering = [n for n in graph['nodes'] if n['kind'] == 'steering']
    findings = findings + steering
    retrieved = graphify_candidates(args.graphify, nodes) if args.graphify else None
    ref_list = [dict(title=n['label'], aliases=n.get('aliases', []), text=n.get('text', ''),
                     category=n['category'], path=n['source_file']) for n in refs.values()]
    model = TfIdf([candidate_text(n) for n in findings])
    scores = model.scores(model.query(query)) if query.strip() else defaultdict(float)
    for i, n in enumerate(findings):
        for f in files:
            if n.get('file') and (n['file'] == f or Path(n['file']).name == Path(f).name):
                scores[i] += 0.3 if n['file'] == f else 0.15
        if args.repo and n.get('repo') and n['repo'] != args.repo:
            scores.pop(i, None)
        if claim is not None and n['id'] == claim['id']:
            scores.pop(i, None)  # the claim under review is not its own precedent
    graph_hits = set()
    if claim is not None:
        # Steering the graph links to the claim is relevant whatever its wording score.
        steered = {l['target'] for l in graph['links'] if l['relation'] == 'steered_by' and l['source'] == claim['id']}
        for i, n in enumerate(findings):
            if n['id'] in steered:
                scores[i] = scores.get(i, 0.0) + GRAPH_RETRIEVAL_BONUS
                graph_hits.add(i)
    if retrieved is not None:
        # GraphRAG: graph-retrieved candidates join the text matches with a bonus and pass the threshold.
        for i, n in enumerate(findings):
            if n['id'] in retrieved and (claim is None or n['id'] != claim['id']):
                scores[i] = scores.get(i, 0.0) + GRAPH_RETRIEVAL_BONUS
                graph_hits.add(i)
    # Threshold on the raw score so a superseded match still surfaces with its newer decision;
    # the superseded weight only orders it below current items. Ties prefer an actionable fix.
    def rank_key(item):
        i, s = item
        n = findings[i]
        weight = SUPERSEDED_WEIGHT if n.get('superseded_by') else 1.0
        if n['kind'] == 'finding' and n.get('outcome') in ('', 'undecided'):
            weight *= UNDECIDED_WEIGHT  # a decided prior says how to handle the claim; an open one does not
        return (round(s * weight, 6), n.get('outcome') == 'fixed', -i)
    ranked = [(s, i) for i, s in sorted(((i, s) for i, s in scores.items() if s >= args.min_score or i in graph_hits),
                                        key=rank_key, reverse=True)]
    if args.decided:
        ranked = [(s, i) for s, i in ranked if findings[i].get('outcome') != 'undecided']
    results, steering_hits, seen_ids = [], [], {}
    for score, i in ranked:
        if len(results) >= args.top and findings[i]['kind'] != 'steering':
            continue
        n = findings[i]
        if n['kind'] == 'finding' and n.get('finding_id') in seen_ids:
            seen_ids[n['finding_id']]['also_in'].append(n['store'])  # the same claim carried into a stacked PR
            continue
        current = [c for c in current_of(n['id'], nodes) if c != n['id']]
        if n['kind'] == 'steering':
            steering_hits.append(dict(score=round(score, 3), node=n['id'], store=n['store'], date=n['date'],
                                      name=n['name'], text=n['text'], detail=n['source_file']))
            continue
        results.append(dict(
            score=round(score, 3), node=n['id'], id=n.get('finding_id') or n.get('memory_id'),
            retrieved_by='graphify' if i in graph_hits else 'text',
            same_store=bool(claim is not None and n.get('store') == claim.get('store')),
            store=n.get('store', ''), repo=n.get('repo', ''), pr=n.get('pr', ''), type=n.get('type', 'MEMORY'),
            severity=n.get('severity', ''), status=n.get('status', ''), outcome=n.get('outcome', ''),
            title=n.get('title', ''), file=f"{n['file']}:{n['line']}" if n.get('line') else n.get('file', ''),
            fix=n.get('fix', ''), fixed=n.get('fixed', ''), justification=n.get('justification', ''),
            rationale=n.get('rationale', ''), confidence=n.get('confidence', ''), reviewer_ack=n.get('reviewer_ack', ''), pushback=n.get('pushback', ''),
            reply=n.get('reply', ''), triage=n.get('triage', ''), scope=n.get('scope', ''), commit=n.get('commit', ''), thread=n.get('thread', ''),
            detail=f"{n.get('source_file', '')}{':' + n['source_location'] if n.get('kind') == 'memory' else ''}",
            superseded_by=n.get('superseded_by', []),
            current_decision=[decision_summary(nodes[c]) for c in current if c in nodes],
            rulings=[decision_summary(nodes[c]) for m in rulings_about.get(n['id'], [])
                     for c in current_of(m, nodes) if c in nodes],
            references=[dict(title=t, path=p) for _, t, p in sorted(linked_refs[n['id']], reverse=True)[:3]],
            also_in=[]))
        if n['kind'] == 'finding':
            seen_ids[n['finding_id']] = results[-1]
    ref_ranked = ReferenceIndex(ref_list).rank(query, args.top_refs) if query.strip() else []
    report = dict(query_terms=sorted(model.query(query), key=lambda t: -model.query(query)[t])[:15] if query.strip() else [],
                  files=files, claim=claim and dict(id=claim.get('finding_id'), store=claim.get('store'),
                                                    title=claim.get('title'), file=claim.get('file'),
                                                    in_graph=claim.get('in_graph', True),
                                                    reviewer=claim.get('reviewer', ''),
                                                    reviewer_kind=reviewer_kind(claim.get('reviewer', '')),
                                                    reviewer_fix=' '.join((claim.get('fix') or '').split())),
                  stale_stores=stale_stores(Path(args.out).expanduser(), Path(args.reviews).expanduser()),
                  prejudgement=prejudge(results), findings=results, steering=steering_hits[:args.top],
                  references=[dict(score=round(s, 3), title=ref_list[i]['title'], category=ref_list[i]['category'],
                                   path=ref_list[i]['path']) for s, i in ref_ranked])
    if args.log_run:
        log_match(Path(args.log_run).expanduser(), args, report)
    if args.format == 'json':
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return
    pj = report['prejudgement']
    print(f"# Pre-judgement\n\n- verdict: {pj['verdict'] or 'none'}\n- basis: {pj['basis']}\n- ask user: {'yes' if pj['ask'] else 'no'}")
    if pj.get('ruling'):
        r = pj['ruling']
        print(f"- ruling: {r['id']} ({r['score']}) {r['title']}\n- handling: {' '.join(r['handling'].split())[:400]}")
    for r in pj.get('rulings', []):
        print(f"- conflicting ruling: {r['id']} {r['outcome']} ({r['score']}) {r['title']}")
    for r in pj.get('priors', []):
        print(f"- prior: {r['store']}/{r['id']} {r['outcome']} ({r['score']}) {' '.join((r['fix'] or '').split())[:200]}")
    print(f"- instruction: {pj['instruction']}\n")
    if report['claim']:
        c = report['claim']
        print(f"# Claim\n\n- {c['store']}/{c['id']}: {c['title']}\n- file: `{c['file']}`")
        if c['reviewer_fix']:
            print(f"- reviewer suggested ({c['reviewer_kind']}: {c['reviewer'] or 'unknown'}): {c['reviewer_fix'][:300]}")
            if c['reviewer_kind'] == 'bot':
                print('- bot suggestions are rarely right; prefer the decided priors below and state where they differ')
        if not c['in_graph']:
            print('- not in the graph yet: read from the review store; run `update` to link it')
        print()
    if report['stale_stores']:
        print(f"- graph is older than {len(report['stale_stores'])} review store(s); run `update`\n")
    print(f"# Prior matches\n\n- query terms: {', '.join(report['query_terms']) or 'none'}\n- files: {', '.join(files) or 'none'}\n")
    if not results:
        print('- No prior finding above the score threshold.\n')
    for r in results:
        print(f"## {r['id']} [{r['severity']}] {r['outcome']} ({r['score']})\n")
        print(f"- title: {r['title']}\n- where: {r['repo']} PR {r['pr']} `{r['file']}`\n- status: {r['status']}")
        print(f"- retrieved by: {r['retrieved_by']}{' (same PR store)' if r['same_store'] else ''}")
        if r['also_in']:
            print(f"- also in: {', '.join(r['also_in'])}")
        for key in ('fix', 'fixed', 'justification', 'rationale', 'reviewer_ack', 'pushback', 'reply', 'scope', 'commit', 'thread'):
            if r[key]:
                print(f"- {key}: {' '.join(r[key].split())[:400]}")
        for c in r['rulings']:
            print(f"- **user ruling**: {c['id']} {c['outcome']} [{c['confidence']}] — {' '.join(c['summary'].split())[:300]}")
        if r['superseded_by']:
            print(f"- **superseded by**: {', '.join(r['superseded_by'])}")
            for c in r['current_decision']:
                print(f"  - current: {c['id']} {c['outcome']} — {' '.join(c['summary'].split())[:300]}")
        for ref in r['references']:
            print(f"- reference: {ref['title']} (`{ref['path']}`)")
        print(f"- detail: `{r['detail']}`\n")
    print('# Steering decisions\n')
    if not report['steering']:
        print('- none matched\n')
    for st in report['steering']:
        print(f"- {st['date']} {st['name']} ({st['score']}) `{st['detail']}`: {' '.join(st['text'].split())[:300]}")
    print('\n# Reference matches\n')
    for ref in report['references']:
        print(f"- {ref['title']} [{ref['category']}] ({ref['score']}) `{ref['path']}`")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--reviews', default=str(DEFAULT_REVIEWS), help='review store root (default ~/reviews)')
    parser.add_argument('--reference', default=str(DEFAULT_REFERENCE), help='reference doc root (default <repo>/reference)')
    parser.add_argument('--out', default=str(DEFAULT_OUT), help='graph output dir (default ~/agents-secret/kg/reviewer)')
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('build', help='full rebuild')
    sub.add_parser('update', help='incremental rebuild from cache')
    match = sub.add_parser('match', help='rank prior findings and references')
    match.add_argument('--text', help='claim or finding text')
    match.add_argument('--finding', help='claim under review (store/ID, full ID, or node); excluded from its own matches')
    match.add_argument('--graphify', help='graphify query output (file or -); rank only the nodes it retrieved')
    match.add_argument('--log-run', help='run directory from run-start; saves the match result and logs what the KG found')
    match.add_argument('--query-file', help='file holding claim text')
    match.add_argument('--diff', help='unified diff file, or - for stdin')
    match.add_argument('--file', dest='files', action='append', help='code path touched (repeatable)')
    match.add_argument('--repo', help='restrict to one repo name as recorded in review META')
    match.add_argument('--decided', action='store_true', help='only findings with a recorded decision')
    match.add_argument('--top', type=int, default=5)
    match.add_argument('--top-refs', type=int, default=3)
    match.add_argument('--min-score', type=float, default=0.15)
    match.add_argument('--format', choices=['md', 'json'], default='md')
    remember = sub.add_parser('remember', help='append a decision, supersede, or note to memory (never rewrites)')
    remember.add_argument('--kind', choices=MEMORY_KINDS, default='decision')
    remember.add_argument('--about', action='append', help='node, store/ID, or finding ID this concerns (repeatable)')
    remember.add_argument('--supersedes', action='append', help='prior node this replaces (repeatable)')
    remember.add_argument('--by', help='existing newer node that supersedes; default is this memory entry')
    remember.add_argument('--title')
    remember.add_argument('--outcome', choices=OUTCOME_VOCAB)
    remember.add_argument('--confidence', choices=CONFIDENCE_VOCAB, default='hypothesis',
                          help='verified = a human confirmed it; hypothesis = agent-inferred (default); reported = external claim')
    remember.add_argument('--fix', help='the fix decided on')
    remember.add_argument('--rationale', required=True, help='why; required')
    remember.add_argument('--source', help='PR, thread URL, or session that produced the decision')
    remember.add_argument('--author')
    remember.add_argument('--no-update', action='store_true', help='skip the incremental graph rebuild')
    run_start = sub.add_parser('run-start', help='start a /kg-review run log under ~/review-kg; prints the run dir')
    run_start.add_argument('--target', required=True, help='claims, store, or branch under review')
    run_start.add_argument('--agent', help='agent name, e.g. codex or claude')
    run_start.add_argument('--log-root', default=str(DEFAULT_LOG_ROOT))
    log_cmd = sub.add_parser('log', help='append an agent step to a run log')
    log_cmd.add_argument('--run', required=True)
    log_cmd.add_argument('--claim', required=True, help='store__ID as used in the run (or store/ID)')
    log_cmd.add_argument('--kind', required=True, choices=LOG_KINDS)
    log_cmd.add_argument('--text', required=True, help='what was found, decided, or proposed')
    log_cmd.add_argument('--evidence', action='append', help='file:line, command and result, or URL (repeatable)')
    log_cmd.add_argument('--ref', action='append', help='prior ID, ruling ID, steering name, or reference doc used (repeatable)')
    run_report = sub.add_parser('run-report', help='render a run log to run.md')
    run_report.add_argument('--run', required=True)
    lint_cmd = sub.add_parser('lint', help='check memory and graph consistency; exit 1 on errors')
    lint_cmd.add_argument('--format', choices=['md', 'json'], default='md')
    lint_cmd.add_argument('--limit', type=int, default=10, help='messages shown per check')
    args = parser.parse_args(argv)
    if args.command == 'match':
        cmd_match(args)
    elif args.command == 'remember':
        cmd_remember(args)
    elif args.command == 'lint':
        cmd_lint(args)
    elif args.command == 'run-start':
        cmd_run_start(args)
    elif args.command == 'log':
        args.claim = args.claim.replace('/', '__')
        cmd_log(args)
    elif args.command == 'run-report':
        cmd_run_report(args)
    else:
        cmd_build(args, incremental=args.command == 'update')


if __name__ == '__main__':
    main()
