# Production Readiness Review / 本番準備レビュー — failure patterns / 失敗パターン

- **Use:** identify a concrete observation before applying a pattern.
- **Finding:** name the consequence and the next useful check.
- **Uncertainty:** absence of evidence is not proof that a failure occurred.

## Demo equals production

- **Signal:** A local success is taken as proof of operational readiness.
- **Response:** Test the intended data, permissions, usage, and failure path.

## Capability promise

- **Signal:** A connector, audit feature, or integration is asserted from old slides.
- **Response:** Verify against current implementation or keep it unconfirmed.

## Nobody next year

- **Signal:** Ownership disappears after handover.
- **Response:** Record maintenance, updates, and failure-response ownership.

## Continue / 続き

- [Operating guide](index.md)
- [Source record](../methods/readiness-and-positioning.md)
