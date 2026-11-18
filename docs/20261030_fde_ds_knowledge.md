# FDE / DS work-tool knowledge

- **What:** portable FDE and DS methods, skills, and knowledge graphs.
- **When:** 2026-10-30.
- **Owner:** repository maintainer.

## Goal

- Give agents substantive methods for doing FDE and DS work.
- Make the wiki usable without access to the original local documents.

## Scope

- Add operating guides and distilled methods under `reference/fde/` and `reference/ds/`.
- Keep redacted presentation and accompanying-note conversions in each track's `source/` directory.
- Use the existing flat `skills/UPPER_SNAKE_CASE.md` convention.
- Preserve the ontology designer and DS scope checker as explicit specialized skills.
- Explain each skill's role, lifecycle stage, purpose, inputs, method, outputs, and handoff checks.
- Provide a general guide for when to use FDE and DS methods.
- Provide `ADVISE_ME.md` to recommend a suitable next skill from the current situation.
- Place graphs under each track's `knowladge_graph/` directory.
- Render graph overviews and skill diagrams in Markdown without an application server.
- Keep organization, trainer, participant, customer, and product identities out of the new content.
- Include the pending local review-workflow, reference-formatting, and container-launcher files in this PR.
- Preserve existing command mappings and graph-review guidance when merging those files.
- Leave hosted application retrieval and workbench interfaces to the application project.

## Interfaces

- `skills/SKILL.md` maps work commands to flat skill files.
- Operational guides and skills link to distilled in-repository knowledge.
- Background slides and notes stay outside default skill graph retrieval.
- Graph records retain their in-repository page paths and content hashes.
- A standalone graph builder recreates the JSON and Mermaid diagrams from the wiki.

## Behaviour

- **AC1:** Fourteen work-tool areas support the available FDE and DS capabilities.
- **AC2:** Murderboard includes preparation, facilitation, questioning, and follow-up.
- **AC3:** Guides provide procedures and decision criteria rather than local-file catalogs.
- **AC4:** Seventeen flat skills include the supplied ontology designer and DS scope checker.
- **AC5:** Graphs resolve their supporting wiki pages without local document access.
- **AC6:** Redacted Markdown retains 313 slides across seven presentations and identifies accompanying-note availability.
- **AC7:** Graphs render as Mermaid Markdown in a compatible repository viewer.
- **AC8:** The advisor explains the role, stage, reason, expected artifact, and handoff for its recommendation.
- **AC9:** The advisor uses distilled knowledge and respects an explicitly selected skill.

## Error cases

- Missing facts remain explicit gaps.
- Proposed organizational practices remain distinct from actual policy.
- Unsupported product claims remain unverified.
- Undigested source material is rejected as an operational knowledge dependency.
- Missing links and invalid metadata stop graph generation.

## Test plan

- **AC1:** Verify the tool map and entrypoints.
- **AC2:** Check the board's guide and knowledge references.
- **AC3:** Check link closure and absence of original-document dependencies.
- **AC4:** Resolve registry commands to the flat skill files.
- **AC5:** Validate graph identities, endpoints, paths, and page hashes.
- **AC6:** Check contiguous slide sections and redaction markers.
- **AC7:** Regenerate the JSON and diagrams deterministically.
- **AC8:** Check advisor command discovery and its knowledge graph connections to the selectable skills.
- **AC9:** Check the advisor context excludes source archives and retains its distilled method references.

## Open questions

- Hosted retrieval and synchronization remain application integration work.

## Related

- [FDE tools](../reference/fde/index.md).
- [DS tools](../reference/ds/index.md).
- [Knowledge provenance](../reference/fde/evidence-and-provenance.md).
