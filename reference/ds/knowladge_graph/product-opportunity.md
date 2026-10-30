# Product Opportunity Scout / 製品化機会の探索

- **View:** this diagram renders in a Markdown viewer with Mermaid support.
- **Data:** [product-opportunity.json](product-opportunity.json).
- **Boundary:** converted source slides/notes are excluded from this skill context.

```mermaid
flowchart TD
  n0["Account Growth Planner / アカウント成長計画"]
  n1["Product reuse and account growth / 製品再利用と成長"]
  n2["Scope, success, and stakeholders / スコープ・成功・関係者"]
  n3["Product Opportunity Scout / 製品化機会の探索 — failure patterns / 失敗パターン"]
  n4["Product Opportunity Scout / 製品化機会の探索"]
  n5["Product Opportunity Scout / 製品化機会の探索 — worksheet / ワークシート"]
  n6["Deployment Planner / 導入計画"]
  n7["Evidence and provenance / 根拠と出典"]
  n8["Decision judgment and ontology design / 判断とオントロジー"]
  n9["Delivery ownership and adversarial review / 導入責任と批判的レビュー"]
  n10["Diagnosis, value, and decision communication / 原因・価値・意思決定"]
  n11["Problem &amp; Value Explorer / 課題・価値の探索"]
  n12["Product Opportunity Scout / 製品化機会の探索 [skill]"]
  n0 -->|derived_from| n1
  n0 -->|references| n4
  n0 -->|references| n7
  n0 -->|references| n11
  n1 -->|references| n0
  n1 -->|references| n4
  n3 -->|derived_from| n1
  n3 -->|references| n4
  n4 -->|references| n0
  n4 -->|derived_from| n1
  n4 -->|checks_with| n3
  n4 -->|produces| n5
  n4 -->|references| n6
  n4 -->|references| n7
  n4 -->|references| n11
  n4 -->|references| n12
  n5 -->|derived_from| n1
  n5 -->|references| n4
  n5 -->|references| n7
  n6 -->|references| n7
  n6 -->|derived_from| n9
  n6 -->|references| n11
  n7 -->|derived_from| n2
  n7 -->|derived_from| n8
  n9 -->|references| n6
  n10 -->|references| n11
  n11 -->|references| n7
  n11 -->|derived_from| n10
  n12 -->|derived_from| n1
  n12 -->|uses| n3
  n12 -->|uses| n4
  n12 -->|uses| n5
```

## Knowledge pages

- [Account Growth Planner / アカウント成長計画](../account-growth/index.md).
- [Product reuse and account growth / 製品再利用と成長](../methods/product-reuse-and-growth.md).
- [Scope, success, and stakeholders / スコープ・成功・関係者](../methods/scope-and-stakeholders.md).
- [Product Opportunity Scout / 製品化機会の探索 — failure patterns / 失敗パターン](../product-opportunity/failure-patterns.md).
- [Product Opportunity Scout / 製品化機会の探索](../product-opportunity/index.md).
- [Product Opportunity Scout / 製品化機会の探索 — worksheet / ワークシート](../product-opportunity/worksheet.md).
- [Deployment Planner / 導入計画](../../fde/deployment-planner/index.md).
- [Evidence and provenance / 根拠と出典](../../fde/evidence-and-provenance.md).
- [Decision judgment and ontology design / 判断とオントロジー](../../fde/methods/decisions-and-ontology.md).
- [Delivery ownership and adversarial review / 導入責任と批判的レビュー](../../fde/methods/delivery-and-review.md).
- [Diagnosis, value, and decision communication / 原因・価値・意思決定](../../fde/methods/diagnosis-and-value.md).
- [Problem & Value Explorer / 課題・価値の探索](../../fde/problem-value/index.md).
- [Product Opportunity Scout / 製品化機会の探索 [skill]](../../../skills/PRODUCT_OPPORTUNITY.md).
