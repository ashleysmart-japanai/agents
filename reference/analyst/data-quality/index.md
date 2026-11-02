# Data Quality Assessment

- **Basis:** authored method guidance; validate suitability against the task evidence.
- **Shared method:** [Analytical evidence and handoff](../methods/evidence-and-handoff.md).

## Inputs

- Data snapshot, row grain, keys, schema, intended use, accepted ranges, and quality tolerances.

## Method

- Identify the unit represented by one row before counting duplicates or joining tables.
- Profile nulls, invalid types, uniqueness, ranges, freshness, and category coverage by relevant cohort.
- Distinguish absent, zero, not applicable, censored, and unrecorded values.
- Check join cardinality and referential integrity before interpreting aggregated results.
- Compare distributions across time and collection sources to detect instrumentation changes.
- Investigate missingness mechanisms before choosing deletion or imputation.
- Keep the raw data unchanged; propose transformations with before/after counts.
- Prioritize defects by their effect on the intended decision rather than a universal quality score.

## Deliverable

- Quality report with affected counts and denominators, source locations, decision impact, proposed fixes, and remaining coverage gaps.

## Validation probe

- A fixture with duplicated keys and a one-to-many join should expose both duplicate records and inflated joined totals.
