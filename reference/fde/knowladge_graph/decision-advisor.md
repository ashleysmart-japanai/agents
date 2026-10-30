# Decision Advisor / 判断の整理

- **View:** this diagram renders in a Markdown viewer with Mermaid support.
- **Data:** [decision-advisor.json](decision-advisor.json).
- **Boundary:** converted source slides/notes are excluded from this skill context.

```mermaid
flowchart TD
  n0["Discovery and responsibility / 業務発見と責任"]
  n1["Scope, success, and stakeholders / スコープ・成功・関係者"]
  n2["Ownership &amp; Handoff Designer / 責任分担・引き継ぎ"]
  n3["Decision Advisor / 判断の整理 — failure patterns / 失敗パターン"]
  n4["Decision Advisor / 判断の整理"]
  n5["Decision Advisor / 判断の整理 — worksheet / ワークシート"]
  n6["Evidence and provenance / 根拠と出典"]
  n7["Decision judgment and ontology design / 判断とオントロジー"]
  n8["Diagnosis, value, and decision communication / 原因・価値・意思決定"]
  n9["Production readiness and positioning / 本番準備と価値の説明"]
  n10["Production Readiness Review / 本番準備レビュー"]
  n11["Steering &amp; Escalation Planner / 運営会議・エスカレーション"]
  n12["Decision Advisor / 判断の整理 [skill]"]
  n0 -->|references| n2
  n2 -->|derived_from| n0
  n2 -->|references| n4
  n2 -->|references| n6
  n3 -->|references| n4
  n3 -->|derived_from| n7
  n4 -->|references| n2
  n4 -->|checks_with| n3
  n4 -->|produces| n5
  n4 -->|references| n6
  n4 -->|derived_from| n7
  n4 -->|references| n10
  n4 -->|references| n11
  n4 -->|references| n12
  n5 -->|references| n4
  n5 -->|references| n6
  n5 -->|derived_from| n7
  n6 -->|derived_from| n1
  n6 -->|derived_from| n7
  n7 -->|references| n4
  n8 -->|references| n11
  n9 -->|references| n10
  n10 -->|references| n6
  n10 -->|derived_from| n9
  n11 -->|references| n4
  n11 -->|references| n6
  n11 -->|derived_from| n8
  n12 -->|uses| n3
  n12 -->|uses| n4
  n12 -->|uses| n5
  n12 -->|derived_from| n7
```

## Knowledge pages

- [Discovery and responsibility / 業務発見と責任](../../ds/methods/discovery-and-ownership.md).
- [Scope, success, and stakeholders / スコープ・成功・関係者](../../ds/methods/scope-and-stakeholders.md).
- [Ownership & Handoff Designer / 責任分担・引き継ぎ](../../ds/ownership-handoff/index.md).
- [Decision Advisor / 判断の整理 — failure patterns / 失敗パターン](../decision-advisor/failure-patterns.md).
- [Decision Advisor / 判断の整理](../decision-advisor/index.md).
- [Decision Advisor / 判断の整理 — worksheet / ワークシート](../decision-advisor/worksheet.md).
- [Evidence and provenance / 根拠と出典](../evidence-and-provenance.md).
- [Decision judgment and ontology design / 判断とオントロジー](../methods/decisions-and-ontology.md).
- [Diagnosis, value, and decision communication / 原因・価値・意思決定](../methods/diagnosis-and-value.md).
- [Production readiness and positioning / 本番準備と価値の説明](../methods/readiness-and-positioning.md).
- [Production Readiness Review / 本番準備レビュー](../production-readiness/index.md).
- [Steering & Escalation Planner / 運営会議・エスカレーション](../steering-escalation/index.md).
- [Decision Advisor / 判断の整理 [skill]](../../../skills/DECISION_ADVISOR.md).
