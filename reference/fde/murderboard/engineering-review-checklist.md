# Engineering review checks / 設計レビューの確認

- **Use:** select checks relevant to the actual proposed system.

## Evaluation / 評価

- What decisions does the output support?
- Which representative and difficult cases were tested?
- Who owns the correct answers and acceptable failure thresholds?
- Which claims are based on appearance rather than an evaluation result?

## Data and access / データ・アクセス

- Which source is authoritative, current, and permitted for this use?
- How are conflicting definitions or versions resolved?
- Can a user receive information they are not entitled to see?
- What evidence is retained to explain an answer or action?

## Human hand-back / 人への引き継ぎ

- Which uncertainty or exception causes a hand-back?
- Who receives it and what information do they need?
- What happens if that person is unavailable?
- Can the user correct a wrong outcome?

## Operations and cost / 運用・コスト

- Which dependencies can fail and how is that detected?
- What is the recovery path and how has it been checked?
- Which cost inputs are measured and which are assumptions?
- What changes under a larger workload?
- Who maintains the system and evaluates changes after handover?

## Finding / 指摘

- Identify the affected claim and requirement.
- Cite the observed evidence or explicitly record that it is missing.
- Explain the customer consequence.
- Propose a specific verification or remedy.
- Use the [failure-pattern guide](failure-patterns.md) to check whether the concern has been overstated.

## Continue / 続き

- [Tool guide](index.md).
- [Output worksheet](worksheet.md).
- [Source record](../methods/delivery-and-review.md).

## Existing wiki references / 既存の参照

- [Design principles](../../design-principles.md) for a design concern supported by the reviewed artifact.
- [Anti-pattern catalog](../../anti-patterns.md) for a specific observed code/design pattern.
- Avoid applying a code pattern solely because its name resembles a business problem.
