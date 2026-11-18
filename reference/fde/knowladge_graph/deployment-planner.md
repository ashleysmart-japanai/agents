# Deployment Planner / 導入計画

- **View:** this diagram renders in a Markdown viewer with Mermaid support.
- **Data:** [deployment-planner.json](deployment-planner.json).
- **Boundary:** converted source slides/notes are excluded from this skill context.

```mermaid
flowchart TD
  n0["Discovery and responsibility / 業務発見と責任"]
  n1["Scope, success, and stakeholders / スコープ・成功・関係者"]
  n2["Ownership &amp; Handoff Designer / 責任分担・引き継ぎ"]
  n3["Deployment Planner / 導入計画 — failure patterns / 失敗パターン"]
  n4["Deployment Planner / 導入計画"]
  n5["Deployment Planner / 導入計画 — worksheet / ワークシート"]
  n6["Evidence and provenance / 根拠と出典"]
  n7["Decision judgment and ontology design / 判断とオントロジー"]
  n8["Delivery ownership and adversarial review / 導入責任と批判的レビュー"]
  n9["Diagnosis, value, and decision communication / 原因・価値・意思決定"]
  n10["Production readiness and positioning / 本番準備と価値の説明"]
  n11["Problem &amp; Value Explorer / 課題・価値の探索"]
  n12["Production Readiness Review / 本番準備レビュー"]
  n13["Deployment Planner / 導入計画 [skill]"]
  n0 -->|references| n2
  n2 -->|derived_from| n0
  n2 -->|references| n4
  n2 -->|references| n6
  n3 -->|references| n4
  n3 -->|derived_from| n8
  n4 -->|references| n2
  n4 -->|checks_with| n3
  n4 -->|produces| n5
  n4 -->|references| n6
  n4 -->|derived_from| n8
  n4 -->|references| n11
  n4 -->|references| n12
  n4 -->|references| n13
  n5 -->|references| n4
  n5 -->|references| n6
  n5 -->|derived_from| n8
  n6 -->|derived_from| n1
  n6 -->|derived_from| n7
  n8 -->|references| n4
  n9 -->|references| n11
  n10 -->|references| n12
  n11 -->|references| n6
  n11 -->|derived_from| n9
  n12 -->|references| n6
  n12 -->|derived_from| n10
  n13 -->|uses| n3
  n13 -->|uses| n4
  n13 -->|uses| n5
  n13 -->|derived_from| n8
```

## Knowledge pages

- [Discovery and responsibility / 業務発見と責任](../../ds/methods/discovery-and-ownership.md).
- [Scope, success, and stakeholders / スコープ・成功・関係者](../../ds/methods/scope-and-stakeholders.md).
- [Ownership & Handoff Designer / 責任分担・引き継ぎ](../../ds/ownership-handoff/index.md).
- [Deployment Planner / 導入計画 — failure patterns / 失敗パターン](../deployment-planner/failure-patterns.md).
- [Deployment Planner / 導入計画](../deployment-planner/index.md).
- [Deployment Planner / 導入計画 — worksheet / ワークシート](../deployment-planner/worksheet.md).
- [Evidence and provenance / 根拠と出典](../evidence-and-provenance.md).
- [Decision judgment and ontology design / 判断とオントロジー](../methods/decisions-and-ontology.md).
- [Delivery ownership and adversarial review / 導入責任と批判的レビュー](../methods/delivery-and-review.md).
- [Diagnosis, value, and decision communication / 原因・価値・意思決定](../methods/diagnosis-and-value.md).
- [Production readiness and positioning / 本番準備と価値の説明](../methods/readiness-and-positioning.md).
- [Problem & Value Explorer / 課題・価値の探索](../problem-value/index.md).
- [Production Readiness Review / 本番準備レビュー](../production-readiness/index.md).
- [Deployment Planner / 導入計画 [skill]](../../../skills/DEPLOYMENT_PLANNER.md).
