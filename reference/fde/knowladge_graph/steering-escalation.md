# Steering & Escalation Planner / 運営会議・エスカレーション

- **View:** this diagram renders in a Markdown viewer with Mermaid support.
- **Data:** [steering-escalation.json](steering-escalation.json).
- **Boundary:** converted source slides/notes are excluded from this skill context.

```mermaid
flowchart TD
  n0["Scope, success, and stakeholders / スコープ・成功・関係者"]
  n1["Stakeholder &amp; Conversation Planner / 関係者・対話計画"]
  n2["Decision Advisor / 判断の整理"]
  n3["Evidence and provenance / 根拠と出典"]
  n4["Decision judgment and ontology design / 判断とオントロジー"]
  n5["Diagnosis, value, and decision communication / 原因・価値・意思決定"]
  n6["Problem &amp; Value Explorer / 課題・価値の探索"]
  n7["Steering &amp; Escalation Planner / 運営会議・エスカレーション — failure patterns / 失敗パターン"]
  n8["Steering &amp; Escalation Planner / 運営会議・エスカレーション"]
  n9["Steering &amp; Escalation Planner / 運営会議・エスカレーション — worksheet / ワークシート"]
  n10["Steering &amp; Escalation Planner / 運営会議・エスカレーション [skill]"]
  n0 -->|references| n1
  n1 -->|derived_from| n0
  n1 -->|references| n3
  n1 -->|references| n8
  n2 -->|references| n3
  n2 -->|derived_from| n4
  n2 -->|references| n8
  n3 -->|derived_from| n0
  n3 -->|derived_from| n4
  n4 -->|references| n2
  n5 -->|references| n6
  n5 -->|references| n8
  n6 -->|references| n3
  n6 -->|derived_from| n5
  n6 -->|references| n8
  n7 -->|derived_from| n5
  n7 -->|references| n8
  n8 -->|references| n1
  n8 -->|references| n2
  n8 -->|references| n3
  n8 -->|derived_from| n5
  n8 -->|references| n6
  n8 -->|checks_with| n7
  n8 -->|produces| n9
  n8 -->|references| n10
  n9 -->|references| n3
  n9 -->|derived_from| n5
  n9 -->|references| n8
  n10 -->|derived_from| n5
  n10 -->|uses| n7
  n10 -->|uses| n8
  n10 -->|uses| n9
```

## Knowledge pages

- [Scope, success, and stakeholders / スコープ・成功・関係者](../../ds/methods/scope-and-stakeholders.md).
- [Stakeholder & Conversation Planner / 関係者・対話計画](../../ds/stakeholder-conversation/index.md).
- [Decision Advisor / 判断の整理](../decision-advisor/index.md).
- [Evidence and provenance / 根拠と出典](../evidence-and-provenance.md).
- [Decision judgment and ontology design / 判断とオントロジー](../methods/decisions-and-ontology.md).
- [Diagnosis, value, and decision communication / 原因・価値・意思決定](../methods/diagnosis-and-value.md).
- [Problem & Value Explorer / 課題・価値の探索](../problem-value/index.md).
- [Steering & Escalation Planner / 運営会議・エスカレーション — failure patterns / 失敗パターン](../steering-escalation/failure-patterns.md).
- [Steering & Escalation Planner / 運営会議・エスカレーション](../steering-escalation/index.md).
- [Steering & Escalation Planner / 運営会議・エスカレーション — worksheet / ワークシート](../steering-escalation/worksheet.md).
- [Steering & Escalation Planner / 運営会議・エスカレーション [skill]](../../../skills/STEERING_ESCALATION.md).
