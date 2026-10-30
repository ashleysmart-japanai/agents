import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shutil
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('knowledge', REPO/'scripts/build_knowledge_graphs.py')
knowledge = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(knowledge)


class KnowledgeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for track in ['fde','ds']:
            shutil.copytree(REPO/'reference'/track,self.root/'reference'/track)
        pages = knowledge.read_manifest(REPO)['pages']
        for page in pages:
            if page['type']=='skill':
                target = self.root/page['path'];target.parent.mkdir(exist_ok=True)
                shutil.copy2(REPO/page['path'],target)
        (self.root/'skills/SKILL.md').write_text((REPO/'skills/SKILL.md').read_text())
        for relative in ['reference/design-principles.md','reference/anti-patterns.md','reference/design-principles/domain-driven-design.md']:
            target = self.root/relative;target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(REPO/relative,target)

    def project(self):
        return knowledge.project(self.root,self.root)

    def test_skill_graphs_have_valid_endpoints_and_in_repo_evidence(self):
        graph, skills = self.project()
        self.assertEqual(len(skills),17)
        for subgraph in [graph,*skills.values()]:
            ids = {n['id'] for n in subgraph['entities']}
            self.assertEqual(len(ids),len(subgraph['entities']))
            self.assertTrue(any(n['type']=='method' for n in subgraph['entities']))
            for node in subgraph['entities']:
                values = {p['key']:p['defaultValue'] for p in node['properties']}
                source = self.root/values['wiki_path']
                self.assertTrue(source.is_file())
                self.assertEqual(values['content_sha256'],hashlib.sha256(source.read_bytes()).hexdigest())
                self.assertNotIn('/source/',values['wiki_path'])
                self.assertNotEqual(node['label'],'---')
            for edge in subgraph['relationships']:
                self.assertIn(edge['source'],ids)
                self.assertIn(edge['target'],ids)
                self.assertTrue((self.root/edge['properties']['source_page']).is_file())
        self.assertTrue(any('premortem' in n['id'] for n in skills['murderboard']['entities']))

    def test_graph_and_diagram_generation_is_deterministic(self):
        first = knowledge.build(self.root,self.root)
        self.assertEqual(first['trackGraphs'],2)
        files = lambda: {str(p.relative_to(self.root)):p.read_bytes() for track in ['fde','ds'] for p in (self.root/'reference'/track/'knowladge_graph').iterdir() if p.suffix in ['.json','.md']}
        before = files()
        self.assertEqual(knowledge.build(self.root,self.root),first)
        self.assertEqual(files(),before)
        for track in ['fde','ds']:
            overview = (self.root/'reference'/track/'knowladge_graph/README.md').read_text()
            self.assertIn('```mermaid\nflowchart TD',overview)
            self.assertIn('## Skill graphs',overview)

    def test_undigested_source_is_not_an_operational_dependency(self):
        path = self.root/'reference/fde/murderboard/index.md'
        path.write_text(path.read_text()+'\n- [Slides](../source/delivery-and-review/slides.md).\n')
        with self.assertRaisesRegex(ValueError,'undigested'):
            self.project()

    def test_broken_link_is_reported(self):
        path = self.root/'reference/fde/murderboard/index.md'
        path.write_text(path.read_text()+'\n- [Missing](missing.md).\n')
        with self.assertRaisesRegex(ValueError,'Broken link'):
            self.project()

    def test_missing_or_unlinked_method_provenance_is_reported(self):
        file = self.root/knowledge.MANIFESTS[0]
        original = json.loads(file.read_text())
        for sources in [[],['reference/fde/methods/readiness-and-positioning.md']]:
            data = json.loads(json.dumps(original))
            next(p for p in data['pages'] if p['type']=='skill')['sources'] = sources
            file.write_text(json.dumps(data))
            with self.assertRaisesRegex(ValueError,'provenance|Provenance'):
                self.project()

    def test_duplicate_page_identity_is_reported(self):
        file = self.root/knowledge.MANIFESTS[0]
        data = json.loads(file.read_text());data['pages'].append(data['pages'][0])
        file.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError,'Duplicate'):
            self.project()

    def test_unsafe_and_symlinked_paths_are_rejected(self):
        for relative in ['../outside','/absolute']:
            with self.assertRaises(ValueError):
                knowledge.checked_path(self.root,relative)
        link = self.root/'reference/escape.md'
        link.symlink_to(REPO/'CLAUDE.md')
        with self.assertRaisesRegex(ValueError,'Symlink'):
            knowledge.checked_path(self.root,'reference/escape.md')

    def test_work_commands_resolve_to_flat_skills(self):
        registry = (self.root/'skills/SKILL.md').read_text()
        aliases = dict(re.findall(r'- `/([^`]+)`[^\n]*→ \[([^\]]+\.md)\]',registry))
        for command,file in [('murderboard','MURDERBOARD.md'),('ontology-designer','ONTOLOGY_SKETCHER.md'),('ontology-sketcher','ONTOLOGY_SKETCHER.md'),('ds-scope-checker','DS_SCOPE_CHECKER.md'),('steering-escalation','STEERING_ESCALATION.md'),('advise_me','ADVISE_ME.md'),('advise-me','ADVISE_ME.md')]:
            self.assertEqual(aliases[command],file)
            text = (self.root/'skills'/file).read_text()
            self.assertIn('name:',text)
            self.assertIn('**Role:**',text)
            self.assertIn('**Stage:**',text)
            self.assertIn('**Why:**',text)
        self.assertFalse(list((self.root/'skills').glob('*/SKILL.md')))

    def test_advisor_context_covers_selectable_skills_for_both_roles(self):
        _, skills = self.project()
        advisor = skills['advise-me']
        ids = {node['id'] for node in advisor['entities']}
        self.assertTrue({'skill:'+name for name in skills}.issubset(ids))
        self.assertTrue(any(node['type']=='method' for node in advisor['entities']))
        self.assertFalse(any('/source/' in prop['defaultValue'] for node in advisor['entities'] for prop in node['properties'] if prop['key']=='wiki_path'))
        knowledge.build(self.root,self.root)
        for track in ['fde','ds']:
            path = self.root/'reference'/track/'knowladge_graph/advise-me.json'
            self.assertEqual(json.loads(path.read_text()),advisor)
            self.assertIn('[advise-me](advise-me.md)',(path.parent/'README.md').read_text())

    def test_source_conversion_is_complete_and_has_no_original_file_dependency(self):
        total = 0
        expected = {'delivery-and-review':46,'diagnosis-and-value':52,'decisions-and-ontology':50,'readiness-and-positioning':41,'discovery-and-ownership':43,'product-reuse-and-growth':39,'scope-and-stakeholders':42}
        for track in ['fde','ds']:
            for file in (self.root/'reference'/track/'source').glob('*/slides.md'):
                text = file.read_text();slides = list(map(int,re.findall(r'^## Slide (\d+)$',text,re.M)))
                self.assertEqual(slides,list(range(1,expected[file.parent.name]+1)))
                self.assertTrue((file.parent/'notes.md').is_file())
                self.assertNotRegex(text,r'(?i)(?:[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}|/Users/|\.pdf\b|\.rtf\b)')
                total += len(slides)
        self.assertEqual(total,313)
        for file in self.root.glob('reference/*/source/*/slides.md'):
            self.assertNotRegex(file.read_text(),r'\b(?:T O S T A R T|T O D A Y|M I N)\b')


if __name__=='__main__':
    unittest.main()
