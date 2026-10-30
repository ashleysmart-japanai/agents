---
name: graphify
description: Use Graphify for explicitly requested repository indexing, architecture mapping, cross-module impact analysis, or KG/ontology-enhanced code review. Skip ordinary edits and ordinary reviews without a graph-analysis request.
---

# Gated knowledge graph analysis

- Execute Graphify when the user requests indexing, workspace dependency analysis, system architecture mapping, cross-module impact analysis, or a KG/ontology-enhanced review.
- Treat invocation of this skill as an explicit graph-analysis request.
- Keep ordinary coding and reviews on their existing workflow.
- Use the repository root as the working directory.
- Resolve `graphify` from PATH or `~/.local/bin/graphify`.
- Keep each repository's graph in its own `graphify-out/` directory.
- Check `graphify --version` and `graphify --help` when the installed interface differs from these commands.
- Build or refresh the graph with `graphify extract . --code-only` when the requested analysis needs a current index.
- Record the repository, HEAD, dirty-worktree state, and index time with the analysis.
- Refresh after source changes; a matching HEAD does not establish freshness for uncommitted files.
- Keep code extraction local with `--code-only`.
- Require an explicit semantic-extraction request before sending documents or media to a model backend.
- Query a scoped question with `graphify query "<question containing actual symbol names>" --budget 2000`.
- Inspect dependencies with `graphify affected "<symbol>" --depth 2 --relation calls`.
- Inspect a node with `graphify explain "<symbol>"`.
- Trace a connection with `graphify path "<source>" "<target>"`.
- Resolve ambiguous matches using the returned candidates.
- Treat missing graph matches as incomplete evidence, not proof that a dependency is absent.
- Verify relevant graph edges against current source and tests.
- Distinguish extracted relationships from inferred relationships.
- Report graph failures or missing language coverage before continuing with source-based analysis.
- Do not install search interceptors, automatic indexing hooks, or graph-first global instructions.
- For ontology-enhanced review, read [references/review.md](references/review.md).
