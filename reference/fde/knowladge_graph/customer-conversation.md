# Customer Conversation Rehearsal / 顧客対話の練習

- **View:** this diagram renders in a Markdown viewer with Mermaid support.
- **Data:** [customer-conversation.json](customer-conversation.json).
- **Boundary:** converted source slides/notes are excluded from this skill context.

```mermaid
flowchart TD
  n0["Scope, success, and stakeholders / スコープ・成功・関係者"]
  n1["Stakeholder &amp; Conversation Planner / 関係者・対話計画"]
  n2["Customer Conversation Rehearsal / 顧客対話の練習 — failure patterns / 失敗パターン"]
  n3["Customer Conversation Rehearsal / 顧客対話の練習"]
  n4["Customer Conversation Rehearsal / 顧客対話の練習 — worksheet / ワークシート"]
  n5["Evidence and provenance / 根拠と出典"]
  n6["Decision judgment and ontology design / 判断とオントロジー"]
  n7["Diagnosis, value, and decision communication / 原因・価値・意思決定"]
  n8["Production readiness and positioning / 本番準備と価値の説明"]
  n9["Problem &amp; Value Explorer / 課題・価値の探索"]
  n10["Production Readiness Review / 本番準備レビュー"]
  n11["Customer Conversation Rehearsal / 顧客対話の練習 [skill]"]
  n0 -->|references| n1
  n1 -->|derived_from| n0
  n1 -->|references| n3
  n1 -->|references| n5
  n2 -->|references| n3
  n2 -->|derived_from| n8
  n3 -->|references| n1
  n3 -->|checks_with| n2
  n3 -->|produces| n4
  n3 -->|references| n5
  n3 -->|derived_from| n8
  n3 -->|references| n9
  n3 -->|references| n10
  n3 -->|references| n11
  n4 -->|references| n3
  n4 -->|references| n5
  n4 -->|derived_from| n8
  n5 -->|derived_from| n0
  n5 -->|derived_from| n6
  n7 -->|references| n9
  n8 -->|references| n3
  n8 -->|references| n10
  n9 -->|references| n5
  n9 -->|derived_from| n7
  n10 -->|references| n3
  n10 -->|references| n5
  n10 -->|derived_from| n8
  n11 -->|uses| n2
  n11 -->|uses| n3
  n11 -->|uses| n4
  n11 -->|derived_from| n8
```

## Knowledge pages

- [Scope, success, and stakeholders / スコープ・成功・関係者](../../ds/methods/scope-and-stakeholders.md).
- [Stakeholder & Conversation Planner / 関係者・対話計画](../../ds/stakeholder-conversation/index.md).
- [Customer Conversation Rehearsal / 顧客対話の練習 — failure patterns / 失敗パターン](../customer-conversation/failure-patterns.md).
- [Customer Conversation Rehearsal / 顧客対話の練習](../customer-conversation/index.md).
- [Customer Conversation Rehearsal / 顧客対話の練習 — worksheet / ワークシート](../customer-conversation/worksheet.md).
- [Evidence and provenance / 根拠と出典](../evidence-and-provenance.md).
- [Decision judgment and ontology design / 判断とオントロジー](../methods/decisions-and-ontology.md).
- [Diagnosis, value, and decision communication / 原因・価値・意思決定](../methods/diagnosis-and-value.md).
- [Production readiness and positioning / 本番準備と価値の説明](../methods/readiness-and-positioning.md).
- [Problem & Value Explorer / 課題・価値の探索](../problem-value/index.md).
- [Production Readiness Review / 本番準備レビュー](../production-readiness/index.md).
- [Customer Conversation Rehearsal / 顧客対話の練習 [skill]](../../../skills/CUSTOMER_CONVERSATION.md).
