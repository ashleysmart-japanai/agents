# Production Readiness Review / 本番準備レビュー

- **View:** this diagram renders in a Markdown viewer with Mermaid support.
- **Data:** [production-readiness.json](production-readiness.json).
- **Boundary:** converted source slides/notes are excluded from this skill context.

```mermaid
flowchart TD
  n0["Scope, success, and stakeholders / スコープ・成功・関係者"]
  n1["Scope &amp; Success Designer / スコープ・成功条件"]
  n2["Customer Conversation Rehearsal / 顧客対話の練習"]
  n3["Evidence and provenance / 根拠と出典"]
  n4["Decision judgment and ontology design / 判断とオントロジー"]
  n5["Delivery ownership and adversarial review / 導入責任と批判的レビュー"]
  n6["Production readiness and positioning / 本番準備と価値の説明"]
  n7["Murderboard / マーダーボード"]
  n8["Production Readiness Review / 本番準備レビュー — failure patterns / 失敗パターン"]
  n9["Production Readiness Review / 本番準備レビュー"]
  n10["Production Readiness Review / 本番準備レビュー — worksheet / ワークシート"]
  n11["Production Readiness Review / 本番準備レビュー [skill]"]
  n0 -->|references| n1
  n1 -->|derived_from| n0
  n1 -->|references| n3
  n2 -->|references| n3
  n2 -->|derived_from| n6
  n2 -->|references| n9
  n3 -->|derived_from| n0
  n3 -->|derived_from| n4
  n5 -->|references| n7
  n6 -->|references| n2
  n6 -->|references| n9
  n7 -->|references| n1
  n7 -->|references| n3
  n7 -->|derived_from| n5
  n7 -->|references| n9
  n8 -->|derived_from| n6
  n8 -->|references| n9
  n9 -->|references| n1
  n9 -->|references| n2
  n9 -->|references| n3
  n9 -->|derived_from| n6
  n9 -->|references| n7
  n9 -->|checks_with| n8
  n9 -->|produces| n10
  n9 -->|references| n11
  n10 -->|references| n3
  n10 -->|derived_from| n6
  n10 -->|references| n9
  n11 -->|derived_from| n6
  n11 -->|uses| n8
  n11 -->|uses| n9
  n11 -->|uses| n10
```

## Knowledge pages

- [Scope, success, and stakeholders / スコープ・成功・関係者](../../ds/methods/scope-and-stakeholders.md).
- [Scope & Success Designer / スコープ・成功条件](../../ds/scope-success/index.md).
- [Customer Conversation Rehearsal / 顧客対話の練習](../customer-conversation/index.md).
- [Evidence and provenance / 根拠と出典](../evidence-and-provenance.md).
- [Decision judgment and ontology design / 判断とオントロジー](../methods/decisions-and-ontology.md).
- [Delivery ownership and adversarial review / 導入責任と批判的レビュー](../methods/delivery-and-review.md).
- [Production readiness and positioning / 本番準備と価値の説明](../methods/readiness-and-positioning.md).
- [Murderboard / マーダーボード](../murderboard/index.md).
- [Production Readiness Review / 本番準備レビュー — failure patterns / 失敗パターン](../production-readiness/failure-patterns.md).
- [Production Readiness Review / 本番準備レビュー](../production-readiness/index.md).
- [Production Readiness Review / 本番準備レビュー — worksheet / ワークシート](../production-readiness/worksheet.md).
- [Production Readiness Review / 本番準備レビュー [skill]](../../../skills/PRODUCTION_READINESS.md).
