# Stakeholder & Conversation Planner / 関係者・対話計画

- **View:** this diagram renders in a Markdown viewer with Mermaid support.
- **Data:** [stakeholder-conversation.json](stakeholder-conversation.json).
- **Boundary:** converted source slides/notes are excluded from this skill context.

```mermaid
flowchart TD
  n0["Scope, success, and stakeholders / スコープ・成功・関係者"]
  n1["Scope &amp; Success Designer / スコープ・成功条件"]
  n2["Stakeholder &amp; Conversation Planner / 関係者・対話計画 — failure patterns / 失敗パターン"]
  n3["Stakeholder &amp; Conversation Planner / 関係者・対話計画"]
  n4["Stakeholder &amp; Conversation Planner / 関係者・対話計画 — worksheet / ワークシート"]
  n5["Customer Conversation Rehearsal / 顧客対話の練習"]
  n6["Evidence and provenance / 根拠と出典"]
  n7["Decision judgment and ontology design / 判断とオントロジー"]
  n8["Diagnosis, value, and decision communication / 原因・価値・意思決定"]
  n9["Production readiness and positioning / 本番準備と価値の説明"]
  n10["Steering &amp; Escalation Planner / 運営会議・エスカレーション"]
  n11["Stakeholder &amp; Conversation Planner / 関係者・対話計画 [skill]"]
  n0 -->|references| n1
  n0 -->|references| n3
  n1 -->|derived_from| n0
  n1 -->|references| n3
  n1 -->|references| n6
  n2 -->|derived_from| n0
  n2 -->|references| n3
  n3 -->|derived_from| n0
  n3 -->|references| n1
  n3 -->|checks_with| n2
  n3 -->|produces| n4
  n3 -->|references| n5
  n3 -->|references| n6
  n3 -->|references| n10
  n3 -->|references| n11
  n4 -->|derived_from| n0
  n4 -->|references| n3
  n4 -->|references| n6
  n5 -->|references| n3
  n5 -->|references| n6
  n5 -->|derived_from| n9
  n6 -->|derived_from| n0
  n6 -->|derived_from| n7
  n8 -->|references| n10
  n9 -->|references| n5
  n10 -->|references| n3
  n10 -->|references| n6
  n10 -->|derived_from| n8
  n11 -->|derived_from| n0
  n11 -->|uses| n2
  n11 -->|uses| n3
  n11 -->|uses| n4
```

## Knowledge pages

- [Scope, success, and stakeholders / スコープ・成功・関係者](../methods/scope-and-stakeholders.md).
- [Scope & Success Designer / スコープ・成功条件](../scope-success/index.md).
- [Stakeholder & Conversation Planner / 関係者・対話計画 — failure patterns / 失敗パターン](../stakeholder-conversation/failure-patterns.md).
- [Stakeholder & Conversation Planner / 関係者・対話計画](../stakeholder-conversation/index.md).
- [Stakeholder & Conversation Planner / 関係者・対話計画 — worksheet / ワークシート](../stakeholder-conversation/worksheet.md).
- [Customer Conversation Rehearsal / 顧客対話の練習](../../fde/customer-conversation/index.md).
- [Evidence and provenance / 根拠と出典](../../fde/evidence-and-provenance.md).
- [Decision judgment and ontology design / 判断とオントロジー](../../fde/methods/decisions-and-ontology.md).
- [Diagnosis, value, and decision communication / 原因・価値・意思決定](../../fde/methods/diagnosis-and-value.md).
- [Production readiness and positioning / 本番準備と価値の説明](../../fde/methods/readiness-and-positioning.md).
- [Steering & Escalation Planner / 運営会議・エスカレーション](../../fde/steering-escalation/index.md).
- [Stakeholder & Conversation Planner / 関係者・対話計画 [skill]](../../../skills/STAKEHOLDER_CONVERSATION.md).
