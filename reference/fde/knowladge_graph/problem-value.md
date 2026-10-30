# Problem & Value Explorer / 課題・価値の探索

- **View:** this diagram renders in a Markdown viewer with Mermaid support.
- **Data:** [problem-value.json](problem-value.json).
- **Boundary:** converted source slides/notes are excluded from this skill context.

```mermaid
flowchart TD
  n0["Discovery Interviewer / 業務発見インタビュー"]
  n1["Discovery and responsibility / 業務発見と責任"]
  n2["Scope, success, and stakeholders / スコープ・成功・関係者"]
  n3["Scope &amp; Success Designer / スコープ・成功条件"]
  n4["Evidence and provenance / 根拠と出典"]
  n5["Decision judgment and ontology design / 判断とオントロジー"]
  n6["Diagnosis, value, and decision communication / 原因・価値・意思決定"]
  n7["Problem &amp; Value Explorer / 課題・価値の探索 — failure patterns / 失敗パターン"]
  n8["Problem &amp; Value Explorer / 課題・価値の探索"]
  n9["Problem &amp; Value Explorer / 課題・価値の探索 — worksheet / ワークシート"]
  n10["Steering &amp; Escalation Planner / 運営会議・エスカレーション"]
  n11["Problem &amp; Value Explorer / 課題・価値の探索 [skill]"]
  n0 -->|derived_from| n1
  n0 -->|references| n3
  n0 -->|references| n4
  n0 -->|references| n8
  n1 -->|references| n0
  n2 -->|references| n3
  n3 -->|derived_from| n2
  n3 -->|references| n4
  n3 -->|references| n8
  n4 -->|derived_from| n2
  n4 -->|derived_from| n5
  n6 -->|references| n8
  n6 -->|references| n10
  n7 -->|derived_from| n6
  n7 -->|references| n8
  n8 -->|references| n0
  n8 -->|references| n3
  n8 -->|references| n4
  n8 -->|derived_from| n6
  n8 -->|checks_with| n7
  n8 -->|produces| n9
  n8 -->|references| n10
  n8 -->|references| n11
  n9 -->|references| n4
  n9 -->|derived_from| n6
  n9 -->|references| n8
  n10 -->|references| n4
  n10 -->|derived_from| n6
  n10 -->|references| n8
  n11 -->|derived_from| n6
  n11 -->|uses| n7
  n11 -->|uses| n8
  n11 -->|uses| n9
```

## Knowledge pages

- [Discovery Interviewer / 業務発見インタビュー](../../ds/discovery-interviewer/index.md).
- [Discovery and responsibility / 業務発見と責任](../../ds/methods/discovery-and-ownership.md).
- [Scope, success, and stakeholders / スコープ・成功・関係者](../../ds/methods/scope-and-stakeholders.md).
- [Scope & Success Designer / スコープ・成功条件](../../ds/scope-success/index.md).
- [Evidence and provenance / 根拠と出典](../evidence-and-provenance.md).
- [Decision judgment and ontology design / 判断とオントロジー](../methods/decisions-and-ontology.md).
- [Diagnosis, value, and decision communication / 原因・価値・意思決定](../methods/diagnosis-and-value.md).
- [Problem & Value Explorer / 課題・価値の探索 — failure patterns / 失敗パターン](../problem-value/failure-patterns.md).
- [Problem & Value Explorer / 課題・価値の探索](../problem-value/index.md).
- [Problem & Value Explorer / 課題・価値の探索 — worksheet / ワークシート](../problem-value/worksheet.md).
- [Steering & Escalation Planner / 運営会議・エスカレーション](../steering-escalation/index.md).
- [Problem & Value Explorer / 課題・価値の探索 [skill]](../../../skills/PROBLEM_VALUE.md).
