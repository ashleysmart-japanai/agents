# Scope & Success Designer / スコープ・成功条件

- **View:** this diagram renders in a Markdown viewer with Mermaid support.
- **Data:** [scope-success.json](scope-success.json).
- **Boundary:** converted source slides/notes are excluded from this skill context.

```mermaid
flowchart TD
  n0["Discovery and responsibility / 業務発見と責任"]
  n1["Scope, success, and stakeholders / スコープ・成功・関係者"]
  n2["Ownership &amp; Handoff Designer / 責任分担・引き継ぎ"]
  n3["Scope &amp; Success Designer / スコープ・成功条件 — failure patterns / 失敗パターン"]
  n4["Scope &amp; Success Designer / スコープ・成功条件"]
  n5["Scope &amp; Success Designer / スコープ・成功条件 — worksheet / ワークシート"]
  n6["Stakeholder &amp; Conversation Planner / 関係者・対話計画"]
  n7["Evidence and provenance / 根拠と出典"]
  n8["Decision judgment and ontology design / 判断とオントロジー"]
  n9["Diagnosis, value, and decision communication / 原因・価値・意思決定"]
  n10["Problem &amp; Value Explorer / 課題・価値の探索"]
  n11["DS scope checker [skill]"]
  n12["Scope &amp; Success Designer / スコープ・成功条件 [skill]"]
  n0 -->|references| n2
  n1 -->|references| n4
  n1 -->|references| n6
  n2 -->|derived_from| n0
  n2 -->|references| n4
  n2 -->|references| n7
  n3 -->|derived_from| n1
  n3 -->|references| n4
  n4 -->|derived_from| n1
  n4 -->|references| n2
  n4 -->|checks_with| n3
  n4 -->|produces| n5
  n4 -->|references| n6
  n4 -->|references| n7
  n4 -->|references| n10
  n4 -->|references| n11
  n4 -->|references| n12
  n5 -->|derived_from| n1
  n5 -->|references| n4
  n5 -->|references| n7
  n6 -->|derived_from| n1
  n6 -->|references| n4
  n6 -->|references| n7
  n7 -->|derived_from| n1
  n7 -->|derived_from| n8
  n9 -->|references| n10
  n10 -->|references| n4
  n10 -->|references| n7
  n10 -->|derived_from| n9
  n11 -->|derived_from| n1
  n11 -->|uses| n5
  n11 -->|uses| n6
  n12 -->|derived_from| n1
  n12 -->|uses| n3
  n12 -->|uses| n4
  n12 -->|uses| n5
  n12 -->|uses| n11
```

## Knowledge pages

- [Discovery and responsibility / 業務発見と責任](../methods/discovery-and-ownership.md).
- [Scope, success, and stakeholders / スコープ・成功・関係者](../methods/scope-and-stakeholders.md).
- [Ownership & Handoff Designer / 責任分担・引き継ぎ](../ownership-handoff/index.md).
- [Scope & Success Designer / スコープ・成功条件 — failure patterns / 失敗パターン](../scope-success/failure-patterns.md).
- [Scope & Success Designer / スコープ・成功条件](../scope-success/index.md).
- [Scope & Success Designer / スコープ・成功条件 — worksheet / ワークシート](../scope-success/worksheet.md).
- [Stakeholder & Conversation Planner / 関係者・対話計画](../stakeholder-conversation/index.md).
- [Evidence and provenance / 根拠と出典](../../fde/evidence-and-provenance.md).
- [Decision judgment and ontology design / 判断とオントロジー](../../fde/methods/decisions-and-ontology.md).
- [Diagnosis, value, and decision communication / 原因・価値・意思決定](../../fde/methods/diagnosis-and-value.md).
- [Problem & Value Explorer / 課題・価値の探索](../../fde/problem-value/index.md).
- [DS scope checker [skill]](../../../skills/DS_SCOPE_CHECKER.md).
- [Scope & Success Designer / スコープ・成功条件 [skill]](../../../skills/SCOPE_SUCCESS.md).
