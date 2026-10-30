#!/usr/bin/env python3
"""Build portable FDE / DS knowledge graphs and Markdown diagrams (standard library)."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

PAYLOAD = Path(__file__).resolve().parents[1]
MANIFESTS = [Path('reference') / track / 'knowladge_graph/manifest.json' for track in ['fde','ds']]
LINK = re.compile(r'\[[^\]\n]+\]\(([^)\n]+)\)')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def checked_path(root, relative):
    rel = Path(relative)
    if rel.is_absolute() or '..' in rel.parts or not rel.parts:
        raise ValueError(f'Unsafe path: {relative}')
    result = root / rel
    for parent in [result, *result.parents]:
        if parent == root:
            break
        if parent.is_symlink():
            raise ValueError(f'Symlink path: {relative}')
    if not result.resolve().is_relative_to(root.resolve()):
        raise ValueError(f'Path escapes root: {relative}')
    return result


def read_manifest(payload):
    records = [json.loads(checked_path(payload, file).read_text()) for file in MANIFESTS]
    if any(record.get('version') != 1 for record in records):
        raise ValueError('Unsupported wiki manifest')
    data = dict(version=1,pages=[page for record in records for page in record['pages']])
    if data.get('version') != 1 or not isinstance(data.get('pages'), list):
        raise ValueError('Unsupported wiki manifest')
    ids, paths = set(), set()
    for page in data['pages']:
        if page['id'] in ids or page['path'] in paths:
            raise ValueError('Duplicate wiki page identity or path')
        ids.add(page['id']); paths.add(page['path'])
        if not checked_path(payload, page['path']).is_file():
            raise ValueError(f'Missing page: {page["path"]}')
    return data


def page_links(content, source):
    for match in LINK.finditer(content):
        raw = match.group(1)
        parsed = urlsplit(raw)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        target = os.path.normpath(str(Path(source).parent / unquote(parsed.path)))
        # Keep the heading containing the link as an evidence locator.
        headings = re.findall(r'^#{1,6} (.+)$', content[:match.start()], re.M)
        yield target, parsed.fragment, headings[-1] if headings else ''


def project(payload=PAYLOAD, agents_root=None):
    manifest = read_manifest(payload)
    pages = {page['path']: dict(page) for page in manifest['pages']}
    links = []
    for source, page in list(pages.items()):
        content = checked_path(payload, source).read_text()
        if len(content) > 10000:
            raise ValueError(f'Page exceeds graph description limit: {source}')
        for origin in page.get('sources', []):
            if origin not in pages or pages[origin]['type'] != 'method':
                raise ValueError(f'Invalid provenance on {source}: {origin}')
        if page['type'] in ['guide', 'tool', 'skill', 'template', 'patterns', 'review'] and not page.get('sources'):
            raise ValueError(f'Missing provenance: {source}')
        targets = list(page_links(content, source))
        if any(origin not in {t[0] for t in targets} for origin in page.get('sources', [])):
            raise ValueError(f'Provenance is not linked in {source}')
        for target, fragment, section in targets:
            if '/knowladge_graph/' in target:
                continue  # Generated navigation is not a knowledge-input dependency.
            if '/source/' in target:
                raise ValueError(f'Operational page links undigested source material: {source}')
            destination = checked_path(payload, target)
            if target not in pages:
                if destination.is_file():
                    external = destination.suffix == '.md'
                    pages[target] = dict(id=('external:' if external else 'asset:')+target, path=target, title=Path(target).stem, type='existing_reference' if external else 'catalog', sources=[], external=external)
                else:
                    if agents_root is None or not checked_path(agents_root, target).is_file():
                        raise ValueError(f'Broken link in {source}: {target}')
                    pages[target] = dict(id='external:'+target, path=target, title=Path(target).stem, type='existing_reference', sources=[], external=True)
            if fragment and target in pages and not pages[target].get('external') and destination.suffix == '.md':
                # This package currently has no fragment links; reject unresolved additions.
                text = destination.read_text()
                anchors = {re.sub(r'[^\w\- ]', '', h.lower()).replace(' ', '-') for h in re.findall(r'^#{1,6} (.+)$', text, re.M)}
                if unquote(fragment) not in anchors:
                    raise ValueError(f'Broken anchor in {source}: {target}#{fragment}')
            links.append((source, target, fragment, section))
    entities = []
    for index, (relative, page) in enumerate(sorted(pages.items())):
        external = page.get('external', False)
        file = checked_path((agents_root or payload) if external else payload, relative)
        sha = digest(file)
        description = file.read_text() if not external and file.suffix == '.md' else 'Existing wiki reference; retrieve its original page.' if external else 'Training source catalog with relative document locators and fingerprints.'
        values = dict(wiki_path=relative, content_sha256=sha, evidence_pages=page.get('sources', []), external=external)
        entities.append(dict(id=page['id'], label=page['title']+(' [skill]' if page['type']=='skill' else ''), type=page['type'], description=description,
                             properties=[dict(key=k, label=k, dataType='json' if isinstance(v, list) else 'boolean' if isinstance(v, bool) else 'text', defaultValue=v) for k,v in values.items()],
                             actions=[], x=(index % 10)*250, y=(index // 10)*170, pinned=False))
    edges = []
    for source, target, fragment, section in sorted(set(links)):
        target_type = pages[target]['type']
        label = 'derived_from' if target_type == 'method' else 'uses' if pages[source]['type'] == 'skill' else 'checks_with' if target_type == 'patterns' else 'produces' if target_type == 'template' else 'references'
        identity = json.dumps([pages[source]['id'], pages[target]['id'], fragment, section], ensure_ascii=False)
        edges.append(dict(id='link:'+hashlib.sha256(identity.encode()).hexdigest()[:24],source=pages[source]['id'],target=pages[target]['id'],label=label,
                          properties=dict(source_page=source,source_section=section,target_fragment=fragment)))
    graph = dict(schemaVersion=2,id='deployment-knowledge',title='FDE / DS work tools',revision=0,entities=entities,relationships=edges)
    subgraphs = {}
    for page in manifest['pages']:
        if page['type'] != 'skill':
            continue
        owned = str(Path(page['entrypoint']).parent)+'/'
        paths = {page['path']} | {p for p in pages if p.startswith(owned)}
        paths |= {t for s,t,_,_ in links if s in paths}
        paths |= {origin for p in list(paths) for origin in pages[p].get('sources', [])}
        ids = {pages[p]['id'] for p in paths}
        subgraphs[page['id'].removeprefix('skill:')] = {**graph,'id':page['id']+'-knowledge','title':page['title'],'entities':[e for e in entities if e['id'] in ids],'relationships':[e for e in edges if e['source'] in ids and e['target'] in ids]}
    for g in [graph, *subgraphs.values()]:
        if len(g['entities']) > 500 or len(g['relationships']) > 2000 or len(json.dumps(g,ensure_ascii=False).encode()) > 1000000:
            raise ValueError('Projected graph exceeds canonical graph limits')
    return graph, subgraphs


def track_graph(graph, pages, track):
    owned = {p['id'] for p in pages if p['track'] == track or track in p.get('roles',[]) or track == 'fde' and p['track'] == 'shared'}
    ids = owned | {e['target'] for e in graph['relationships'] if e['source'] in owned}
    by_id = {p['id']:p for p in pages}
    origins = {s for identity in ids if identity in by_id for s in by_id[identity].get('sources', [])}
    ids |= {p['id'] for p in pages if p['path'] in origins}
    return {**graph,'id':track+'-knowledge','title':track.upper()+' work knowledge','entities':[n for n in graph['entities'] if n['id'] in ids],'relationships':[e for e in graph['relationships'] if e['source'] in ids and e['target'] in ids]}


def mermaid(graph):
    import html
    keys = {node['id']:'n'+str(i) for i,node in enumerate(graph['entities'])}
    lines = ['```mermaid','flowchart TD']
    for node in graph['entities']:
        lines.append('  '+keys[node['id']]+'["'+html.escape(node['label'],quote=True)+'"]')
    seen = set()
    for edge in graph['relationships']:
        value = (edge['source'],edge['target'],edge['label'])
        if value not in seen:
            seen.add(value)
            lines.append('  '+keys[edge['source']]+' -->|'+edge['label']+'| '+keys[edge['target']])
    return '\n'.join(lines+['```'])


def graph_markdown(graph, path):
    text = '# '+graph['title']+'\n\n- **View:** this diagram renders in a Markdown viewer with Mermaid support.\n- **Data:** ['+path.stem+'.json]('+path.stem+'.json).\n- **Boundary:** converted source slides/notes are excluded from this skill context.\n\n'+mermaid(graph)+'\n\n## Knowledge pages\n\n'
    for node in graph['entities']:
        wiki_path = next(p['defaultValue'] for p in node['properties'] if p['key']=='wiki_path')
        text += '- ['+node['label']+']('+os.path.relpath(wiki_path,path.parent)+').\n'
    return text


def build(payload=PAYLOAD, agents_root=None):
    graph, subgraphs = project(payload, agents_root)
    pages = read_manifest(payload)['pages']
    for track in ['fde','ds']:
        directory = Path('reference') / track / 'knowladge_graph'
        checked_path(payload,directory).mkdir(parents=True,exist_ok=True)
        selected = {p['id'].removeprefix('skill:'):subgraphs[p['id'].removeprefix('skill:')] for p in pages if p['type']=='skill' and (p['track']==track or track in p.get('roles',[]))}
        values = {track:track_graph(graph,pages,track),**selected}
        for name,value in values.items():
            relative = directory / (name+'.json')
            checked_path(payload,relative).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
            if name != track:
                md = directory / (name+'.md')
                checked_path(payload,md).write_text(graph_markdown(value,md))
        overview = values[track]
        overview_ids = {p['id'] for p in pages if (p['type'] in ['tool','skill','method']) and (p['track']==track or track in p.get('roles',[]))}
        small = {**overview,'entities':[n for n in overview['entities'] if n['id'] in overview_ids],'relationships':[e for e in overview['relationships'] if e['source'] in overview_ids and e['target'] in overview_ids]}
        text = '# '+track.upper()+' knowledge graph\n\n- **Rebuild:** run `python3 scripts/build_knowledge_graphs.py` from the repository root.\n- **Validate:** run `python3 scripts/build_knowledge_graphs.py --check`.\n- **Overview:** a compact map of tools, skills, and digested methods.\n- **Full graph:** ['+track+'.json]('+track+'.json).\n- **Source boundary:** background slide and note archives are not default skill knowledge.\n\n'+mermaid(small)+'\n\n## Skill graphs\n\n'
        text += '\n'.join('- ['+name+']('+name+'.md).' for name in sorted(selected))+'\n'
        checked_path(payload,directory/'README.md').write_text(text)
    return dict(pages=len(graph['entities']),links=len(graph['relationships']),skillGraphs=len(subgraphs),trackGraphs=2)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Validate without regenerating artifacts')
    parser.add_argument('--wiki-root', type=Path, default=PAYLOAD)
    args = parser.parse_args()
    if args.check:
        graph, skills = project(args.wiki_root, args.wiki_root)
        result = dict(pages=len(graph['entities']),links=len(graph['relationships']),skillGraphs=len(skills))
    else:
        result = build(args.wiki_root, args.wiki_root)
    print(json.dumps(result))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, json.JSONDecodeError) as error:
        sys.exit(str(error))
