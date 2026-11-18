# Ontology Builder Wizard / オントロジー設計 — failure patterns / 失敗パターン

- **Use:** identify a concrete observation before applying a pattern.
- **Finding:** name the consequence and the next useful check.
- **Uncertainty:** absence of evidence is not proof that a failure occurred.

## Tables mistaken for domain

- **Signal:** Physical tables are copied without checking what the business cares about.
- **Response:** Ask which real-world object each table represents; retain technical tables when that is the user’s explicit subject.

## Unsupported fields

- **Signal:** Units or permissions are added as invented canonical JSON fields.
- **Response:** Keep design metadata in the worksheet or agreed descriptions.

## Magic simulation

- **Signal:** Following edges is described as executing the business process.
- **Response:** Label the impact trace hypothetical and list missing rules.

## Forced tiny catalog

- **Signal:** A suggested starter size truncates an explicitly requested ontology.
- **Response:** Use small defaults for discovery; preserve an explicit full catalog.

## Continue / 続き

- [Operating guide](index.md)
- [Source record](../methods/decisions-and-ontology.md)
