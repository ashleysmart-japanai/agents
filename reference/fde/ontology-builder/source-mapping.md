# Source mapping and gaps / データ対応と食い違い

- **Use:** connect business objects to data structure without assuming a table is the domain model.

## Mapping / 対応

- Record object meaning before choosing its source.
- List the actual system, table, identifier, and known join keys.
- Distinguish authoritative identity from source-specific IDs.
- Record unit, meaning, and source for important properties in the design worksheet.
- Preserve ambiguous words as questions rather than silently merging meanings.

## Gap checks / 確認

- Do two systems use different identifiers for the same thing?
- Do formatting differences prevent a join?
- Does one field contain several values where the model needs several related entities?
- Is a business relationship hidden in free text?
- Does the source retain the history needed by the question?
- Does a status word mean different things in different teams?
- Is the property’s unit or authoritative source missing?
- Does the schema reveal personal-data fields that need separate access consideration?

## Closure / 解消

- Give each gap an answer owner role and next validation action.
- Do not invent a missing column or state that a connector exists without evidence.
- Use structure-only discovery for reusable work.
- Keep actual customer records outside this reusable wiki.

## Continue / 続き

- [Tool guide](index.md).
- [Output worksheet](worksheet.md).
- [Source record](../methods/decisions-and-ontology.md).
