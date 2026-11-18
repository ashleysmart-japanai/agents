import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import time
import unittest

REPO = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('reviewer_kg', REPO / 'scripts/build_reviewer_kg.py')
kg = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(kg)

REVIEW_MD = '''** WARNING do not delete review entries ever **

# META
repo:acme/shop
pr:{pr}
branch:feature/{pr}
reviewed:2026-11-01 10:00

# SUMMARY
{summary}
'''

DETAIL = '''## {id}
ID:{id}
type:B
severity:HIGH
title:{title}
file:`{file}`
pr:`#{pr}`
status:{status}

description:
{description}
https://github.com/acme/shop/pull/{pr}#discussion

evidence:
```evidence
{evidence}
```

fix:{fix}
fixed:{fixed}
justification:{justification}
reviewer:review-bot[bot]
'''


def write_store(root, pr, findings, extra_summary=''):
    store = root / f'shop-pr-{pr}'
    store.mkdir(parents=True, exist_ok=True)
    lines = []
    for f in findings:
        lines.append(f"- [ ] {f['id']} - {f['status']} [HIGH] - {f['title']} `{f['file']}`")
        (store / f"{f['id']}.md").write_text(DETAIL.format(pr=pr, **f))
    (store / 'review.md').write_text(REVIEW_MD.format(pr=pr, summary='\n'.join(lines) + extra_summary))
    return store


NULL_FALLBACK = dict(
    id='B1.aaaaaaaaaaaaaaaaaaaaaa', title='Request body fallback validates a fabricated empty object',
    file='src/api/orders.ts:12', status='CLOSED verified:2026-11-02',
    description='parseOrder(body ?? {}) validates an object the caller never sent and discards the parsed result.',
    evidence='parseOrder(body ?? {});', fix='Validate once at the boundary and pass the parsed order inward.',
    fixed='Removed the inline fallback; controller rejects a missing body with 400.',
    justification='Defensive duct-taping hid a missing body.')
NULL_FALLBACK_REJECTED = dict(
    NULL_FALLBACK, id='B2.bbbbbbbbbbbbbbbbbbbbbb', status='WILL_NOT_FIX', fixed='',
    justification='User ruled the fallback acceptable for the legacy endpoint.')
SQL_COLUMN = dict(
    id='B1.cccccccccccccccccccccc', title='Availability SQL references wrong release channel column',
    file='src/server/featureGate.ts:36', status='OPEN',
    description='Raw SQL uses release_channel but the migrated column is quoted releaseChannel.',
    evidence='WHERE c.release_channel = o.release_channel', fix='Use the mapped Prisma model.',
    fixed='', justification='')


class ReviewerKgTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.reviews = self.root / 'reviews'
        self.out = self.root / 'kg'
        self.reference = self.root / 'reference'
        for category in ('anti-patterns', 'security-principles'):
            shutil.copytree(REPO / 'reference' / category, self.reference / category)
        self.reference_count = sum(1 for p in self.reference.rglob('*.md') if p.name not in kg.SKIP_REFERENCE_NAMES)
        write_store(self.reviews, 1, [NULL_FALLBACK, NULL_FALLBACK_REJECTED])
        write_store(self.reviews, 2, [SQL_COLUMN], extra_summary='\n- [ ] B9.zzzzzzzzzzzzzzzzzzzzzz - OPEN [LOW] - orphan')

    def run_cli(self, *argv):
        buffer = io.StringIO()
        base = ['--reviews', str(self.reviews), '--reference', str(self.reference), '--out', str(self.out)]
        with contextlib.redirect_stdout(buffer):
            kg.main(base + list(argv))
        return buffer.getvalue()

    def graph(self):
        return json.loads((self.out / 'graph.json').read_text())

    def nodes(self):
        return {n['id']: n for n in self.graph()['nodes']}

    def test_build_parses_findings_fields_and_references(self):
        result = json.loads(self.run_cli('build'))
        self.assertEqual(result['findings'], 3)
        self.assertEqual(result['references'], self.reference_count)
        node = self.nodes()['finding:shop-pr-1/B1.aaaaaaaaaaaaaaaaaaaaaa']
        self.assertEqual(node['outcome'], 'fixed')
        self.assertEqual((node['file'], node['line']), ('src/api/orders.ts', '12'))
        self.assertIn('discussion', node['description'])  # wrapped URL line stays in its field
        self.assertIn('parseOrder(body ?? {});', node['evidence'])
        self.assertEqual(self.nodes()['finding:shop-pr-1/B2.bbbbbbbbbbbbbbbbbbbbbb']['outcome'], 'rejected')
        relations = {(l['source'], l['relation'], l['target']) for l in self.graph()['links']}
        self.assertIn(('finding:shop-pr-1/B1.aaaaaaaaaaaaaaaaaaaaaa', 'cites',
                       'reference:reference/anti-patterns/defensive-duct-taping.md'), relations)
        self.assertIn(('finding:shop-pr-1/B1.aaaaaaaaaaaaaaaaaaaaaa', 'similar_to',
                       'finding:shop-pr-1/B2.bbbbbbbbbbbbbbbbbbbbbb'), relations)
        self.assertFalse(any('CHECKLIST' in n for n in self.nodes()))

    def test_update_reparses_only_changed_stores(self):
        self.run_cli('build')
        self.assertEqual(json.loads(self.run_cli('update'))['stores_reparsed'], 0)
        time.sleep(0.01)
        detail = self.reviews / 'shop-pr-2' / f"{SQL_COLUMN['id']}.md"
        detail.write_text(detail.read_text().replace('status:OPEN', 'status:CLOSED verified:2026-11-03'))
        result = json.loads(self.run_cli('update'))
        self.assertEqual(result['stores_reparsed'], 1)
        self.assertEqual(self.nodes()[f"finding:shop-pr-2/{SQL_COLUMN['id']}"]['outcome'], 'fixed')
        shutil.rmtree(self.reviews / 'shop-pr-2')
        self.assertEqual(json.loads(self.run_cli('update'))['stores_removed'], ['shop-pr-2'])

    def test_match_ranks_prior_decision_and_reference(self):
        self.run_cli('build')
        report = json.loads(self.run_cli('match', '--text', 'handler adds an inline fallback validate(input ?? {}) and discards the parsed result',
                                         '--file', 'src/api/orders.ts', '--format', 'json'))
        top_two = {r['id']: r['outcome'] for r in report['findings'][:2]}
        self.assertEqual(top_two, {NULL_FALLBACK['id']: 'fixed', NULL_FALLBACK_REJECTED['id']: 'rejected'})
        self.assertNotIn(SQL_COLUMN['id'], [r['id'] for r in report['findings']])
        self.assertIn('Defensive Duct-Taping', [r['title'] for r in report['references']])

    def test_remember_supersedes_without_deleting_and_match_shows_current(self):
        self.run_cli('build')
        old = 'shop-pr-1/' + NULL_FALLBACK_REJECTED['id']
        self.run_cli('remember', '--kind', 'supersede', '--supersedes', old, '--outcome', 'fixed', '--confidence', 'verified',
                     '--title', 'Inline body fallbacks are fixed at the boundary, including legacy endpoints',
                     '--fix', 'Reject a missing body with 400', '--rationale', 'Legacy exemption withdrawn.')
        memory = (self.out / kg.MEMORY_FILE).read_text().splitlines()
        self.assertEqual(len(memory), 1)
        nodes = self.nodes()
        old_node = nodes[f'finding:{old}']
        self.assertEqual(old_node['outcome'], 'rejected')  # prior result kept as-is
        self.assertTrue(old_node['superseded_by'][0].startswith('memory:mem-'))
        report = json.loads(self.run_cli('match', '--text', 'body ?? {} fallback legacy endpoint', '--top', '10',
                                         '--format', 'json'))
        row = next(r for r in report['findings'] if r['id'] == NULL_FALLBACK_REJECTED['id'])
        self.assertEqual(row['current_decision'][0]['outcome'], 'fixed')
        # A second supersede chains: newest wins, both prior items remain.
        first_mem = old_node['superseded_by'][0]
        self.run_cli('remember', '--kind', 'supersede', '--supersedes', first_mem, '--outcome', 'rejected',
                     '--rationale', 'Exemption restored for the legacy endpoint.')
        nodes = self.nodes()
        self.assertIn(first_mem, nodes)
        current = kg.current_of(f'finding:{old}', nodes)
        self.assertEqual(nodes[current[0]]['rationale'], 'Exemption restored for the legacy endpoint.')

    def test_lint_reports_errors_and_warnings(self):
        self.run_cli('build')
        with (self.out / kg.MEMORY_FILE).open('a') as handle:
            handle.write('{not json\n')
            handle.write(json.dumps(dict(id='mem-dangling', at='2026-11-04T00:00:00+00:00', kind='note',
                                         confidence='verified', about=['finding:nope/B1.x'],
                                         rationale='points nowhere')) + '\n')
            handle.write(json.dumps(dict(id='mem-drift', at='2026-11-04T00:00:00+00:00', kind='decision',
                                         outcome='kinda-fixed', confidence='sure', rationale='hand-edited')) + '\n')
        self.run_cli('update')
        report = kg.lint(self.out, self.reviews)
        self.assertEqual(len(report['E1 memory format']), 1)
        self.assertEqual(len(report['E2 dangling reference']), 1)
        self.assertEqual(len(report['E4 vocabulary']), 2)
        with self.assertRaises(SystemExit):  # unknown outcome is rejected at write time
            self.run_cli('remember', '--outcome', 'kinda-fixed', '--rationale', 'x')
        self.assertEqual(len(report['W2 conflicting decisions']), 1)  # fixed vs rejected, counted once
        self.assertEqual(report['W6 summary row without detail file'], ['shop-pr-2/B9.zzzzzzzzzzzzzzzzzzzzzz'])
        with self.assertRaises(SystemExit):
            self.run_cli('lint')
        time.sleep(0.01)
        (self.reviews / 'shop-pr-1' / 'review.md').write_text((self.reviews / 'shop-pr-1' / 'review.md').read_text() + '\n')
        self.assertIn('W5 stale graph', kg.lint(self.out, self.reviews))

    def test_told_once_ruling_prejudges_the_next_claim(self):
        self.run_cli('build')
        claim = ['--text', 'legacy endpoint handler passes body ?? {} into the validator', '--file', 'src/api/orders.ts',
                 '--format', 'json']
        first = json.loads(self.run_cli('match', *claim))['prejudgement']
        self.assertTrue(first['ask'])
        self.assertNotEqual(first['basis'], 'user-ruling')
        # The user rules once.
        self.run_cli('remember', '--about', 'shop-pr-1/' + NULL_FALLBACK['id'], '--outcome', 'fixed',
                     '--confidence', 'verified', '--title', 'Inline body fallback on any endpoint is fixed at the boundary',
                     '--fix', 'Reject a missing body with 400 in the controller; pass the parsed value inward.',
                     '--rationale', 'User ruling: legacy endpoints get no exemption for body ?? {} fallbacks.')
        # A differently worded claim on the same file is pre-judged without asking.
        again = json.loads(self.run_cli('match', '--text', 'orders controller defaults the request body with ?? {}',
                                        '--file', 'src/api/orders.ts', '--format', 'json'))['prejudgement']
        self.assertEqual((again['basis'], again['verdict'], again['ask']), ('user-ruling', 'fixed', False))
        ruling_id = again['ruling']['id']
        # A later ruling supersedes it; the new one decides, the old one stays.
        self.run_cli('remember', '--kind', 'supersede', '--supersedes', ruling_id, '--outcome', 'rejected',
                     '--confidence', 'verified', '--title', 'Inline body fallback on the legacy orders endpoint stays',
                     '--rationale', 'User ruling: legacy orders endpoint is frozen; leave body ?? {} until removal.')
        latest = json.loads(self.run_cli('match', *claim))['prejudgement']
        self.assertEqual((latest['basis'], latest['verdict'], latest['ask']), ('user-ruling', 'rejected', False))
        self.assertNotEqual(latest['ruling']['id'], ruling_id)
        self.assertIn(f'memory:{ruling_id}', self.nodes())
        # An agent guess (hypothesis) never decides on its own.
        self.run_cli('remember', '--outcome', 'fixed', '--title', 'Billing SQL column mismatch guess',
                     '--rationale', 'Agent thinks the billing SQL column is wrong.')
        guess = json.loads(self.run_cli('match', '--text', 'Agent thinks the billing SQL column is wrong',
                                        '--format', 'json'))['prejudgement']
        self.assertNotEqual(guess['basis'], 'user-ruling')

    def test_conflicting_rulings_ask(self):
        self.run_cli('build')
        about = 'shop-pr-2/' + SQL_COLUMN['id']
        for outcome in ('fixed', 'rejected'):
            self.run_cli('remember', '--about', about, '--outcome', outcome, '--confidence', 'verified',
                         '--title', 'Raw SQL release channel column mismatch',
                         '--rationale', f'Raw SQL release channel column mismatch ruled {outcome}.')
        pj = json.loads(self.run_cli('match', '--text', 'raw SQL release channel column mismatch',
                                     '--format', 'json'))['prejudgement']
        self.assertEqual((pj['verdict'], pj['ask']), ('conflict', True))

    def test_lint_detects_supersede_cycle(self):
        self.run_cli('build')
        a, b = f"finding:shop-pr-1/{NULL_FALLBACK['id']}", f"finding:shop-pr-1/{NULL_FALLBACK_REJECTED['id']}"
        self.run_cli('remember', '--kind', 'supersede', '--by', a, '--supersedes', b, '--rationale', 'a wins')
        self.run_cli('remember', '--kind', 'supersede', '--by', b, '--supersedes', a, '--rationale', 'b wins')
        self.assertIn('E3 supersede cycle', kg.lint(self.out, self.reviews))

    @unittest.skipUnless(shutil.which('graphify') or os.path.exists(os.path.expanduser('~/.local/bin/graphify')),
                         'graphify not installed')
    def test_graphify_reads_the_graph(self):
        self.run_cli('build')
        binary = shutil.which('graphify') or os.path.expanduser('~/.local/bin/graphify')
        result = subprocess.run([binary, 'explain', f"finding:shop-pr-1/{NULL_FALLBACK['id']}",
                                 '--graph', str(self.out / 'graph.json')], capture_output=True, text=True, timeout=60)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('similar_to', result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
