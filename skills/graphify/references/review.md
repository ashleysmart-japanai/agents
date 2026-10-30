# Ontology-enhanced review

- Preserve the selected review skill's scope, finding format, and evidence requirements.
- Start from the diff and the user's architectural question.
- Identify affected modules, symbols, data contracts, entry points, and tests.
- Load existing domain definitions and invariants from repository specs or supplied schemas.
- Separate business concepts from code symbols; an AST graph does not establish business meaning.
- Map each relevant domain concept to its implementation with a source location.
- Mark proposed concept mappings as assumptions until supported by evidence.
- Trace callers, consumers, parallel paths, and boundary crossings around changed symbols.
- Check documented identity, cardinality, ownership, permissions, lifecycle transitions, and contract invariants where relevant.
- Use graph results to select source paths for inspection.
- Prove each finding using current code, a trace, or a test.
- Record the dependency path and violated invariant with the finding when useful.
- Report unmapped concepts and missing edges as coverage gaps.
- Keep the graph advisory; it does not replace reading the diff or executing required checks.
