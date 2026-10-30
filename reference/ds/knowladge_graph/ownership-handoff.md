# Ownership & Handoff Designer / 責任分担・引き継ぎ

- **View:** this diagram renders in a Markdown viewer with Mermaid support.
- **Data:** [ownership-handoff.json](ownership-handoff.json).
- **Boundary:** converted source slides/notes are excluded from this skill context.

```mermaid
flowchart TD
  n0["Discovery and responsibility / 業務発見と責任"]
  n1["Scope, success, and stakeholders / スコープ・成功・関係者"]
  n2["Ownership &amp; Handoff Designer / 責任分担・引き継ぎ — failure patterns / 失敗パターン"]
  n3["Ownership &amp; Handoff Designer / 責任分担・引き継ぎ"]
  n4["Ownership &amp; Handoff Designer / 責任分担・引き継ぎ — worksheet / ワークシート"]
  n5["Scope &amp; Success Designer / スコープ・成功条件"]
  n6["Decision Advisor / 判断の整理"]
  n7["Deployment Planner / 導入計画"]
  n8["Evidence and provenance / 根拠と出典"]
  n9["Decision judgment and ontology design / 判断とオントロジー"]
  n10["Delivery ownership and adversarial review / 導入責任と批判的レビュー"]
  n11["Ownership &amp; Handoff Designer / 責任分担・引き継ぎ [skill]"]
  n0 -->|references| n3
  n1 -->|references| n5
  n2 -->|derived_from| n0
  n2 -->|references| n3
  n3 -->|derived_from| n0
  n3 -->|checks_with| n2
  n3 -->|produces| n4
  n3 -->|references| n5
  n3 -->|references| n6
  n3 -->|references| n7
  n3 -->|references| n8
  n3 -->|references| n11
  n4 -->|derived_from| n0
  n4 -->|references| n3
  n4 -->|references| n8
  n5 -->|derived_from| n1
  n5 -->|references| n3
  n5 -->|references| n8
  n6 -->|references| n3
  n6 -->|references| n8
  n6 -->|derived_from| n9
  n7 -->|references| n3
  n7 -->|references| n8
  n7 -->|derived_from| n10
  n8 -->|derived_from| n1
  n8 -->|derived_from| n9
  n9 -->|references| n6
  n10 -->|references| n7
  n11 -->|derived_from| n0
  n11 -->|uses| n2
  n11 -->|uses| n3
  n11 -->|uses| n4
```

## Knowledge pages

- [Discovery and responsibility / 業務発見と責任](../methods/discovery-and-ownership.md).
- [Scope, success, and stakeholders / スコープ・成功・関係者](../methods/scope-and-stakeholders.md).
- [Ownership & Handoff Designer / 責任分担・引き継ぎ — failure patterns / 失敗パターン](../ownership-handoff/failure-patterns.md).
- [Ownership & Handoff Designer / 責任分担・引き継ぎ](../ownership-handoff/index.md).
- [Ownership & Handoff Designer / 責任分担・引き継ぎ — worksheet / ワークシート](../ownership-handoff/worksheet.md).
- [Scope & Success Designer / スコープ・成功条件](../scope-success/index.md).
- [Decision Advisor / 判断の整理](../../fde/decision-advisor/index.md).
- [Deployment Planner / 導入計画](../../fde/deployment-planner/index.md).
- [Evidence and provenance / 根拠と出典](../../fde/evidence-and-provenance.md).
- [Decision judgment and ontology design / 判断とオントロジー](../../fde/methods/decisions-and-ontology.md).
- [Delivery ownership and adversarial review / 導入責任と批判的レビュー](../../fde/methods/delivery-and-review.md).
- [Ownership & Handoff Designer / 責任分担・引き継ぎ [skill]](../../../skills/OWNERSHIP_HANDOFF.md).
