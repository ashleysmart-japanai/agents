# Discovery Interviewer / 業務発見インタビュー

- **View:** this diagram renders in a Markdown viewer with Mermaid support.
- **Data:** [discovery-interviewer.json](discovery-interviewer.json).
- **Boundary:** converted source slides/notes are excluded from this skill context.

```mermaid
flowchart TD
  n0["Discovery Interviewer / 業務発見インタビュー — failure patterns / 失敗パターン"]
  n1["Discovery Interviewer / 業務発見インタビュー"]
  n2["Discovery Interviewer / 業務発見インタビュー — worksheet / ワークシート"]
  n3["Discovery and responsibility / 業務発見と責任"]
  n4["Scope, success, and stakeholders / スコープ・成功・関係者"]
  n5["Scope &amp; Success Designer / スコープ・成功条件"]
  n6["Evidence and provenance / 根拠と出典"]
  n7["Decision judgment and ontology design / 判断とオントロジー"]
  n8["Diagnosis, value, and decision communication / 原因・価値・意思決定"]
  n9["Ontology Builder Wizard / オントロジー設計"]
  n10["Problem &amp; Value Explorer / 課題・価値の探索"]
  n11["Discovery Interviewer / 業務発見インタビュー [skill]"]
  n0 -->|references| n1
  n0 -->|derived_from| n3
  n1 -->|checks_with| n0
  n1 -->|produces| n2
  n1 -->|derived_from| n3
  n1 -->|references| n5
  n1 -->|references| n6
  n1 -->|references| n9
  n1 -->|references| n10
  n1 -->|references| n11
  n2 -->|references| n1
  n2 -->|derived_from| n3
  n2 -->|references| n6
  n3 -->|references| n1
  n4 -->|references| n5
  n5 -->|derived_from| n4
  n5 -->|references| n6
  n5 -->|references| n10
  n6 -->|derived_from| n4
  n6 -->|derived_from| n7
  n7 -->|references| n9
  n8 -->|references| n10
  n9 -->|references| n1
  n9 -->|references| n5
  n9 -->|references| n6
  n9 -->|derived_from| n7
  n9 -->|references| n10
  n10 -->|references| n1
  n10 -->|references| n5
  n10 -->|references| n6
  n10 -->|derived_from| n8
  n11 -->|uses| n0
  n11 -->|uses| n1
  n11 -->|uses| n2
  n11 -->|derived_from| n3
```

## Knowledge pages

- [Discovery Interviewer / 業務発見インタビュー — failure patterns / 失敗パターン](../discovery-interviewer/failure-patterns.md).
- [Discovery Interviewer / 業務発見インタビュー](../discovery-interviewer/index.md).
- [Discovery Interviewer / 業務発見インタビュー — worksheet / ワークシート](../discovery-interviewer/worksheet.md).
- [Discovery and responsibility / 業務発見と責任](../methods/discovery-and-ownership.md).
- [Scope, success, and stakeholders / スコープ・成功・関係者](../methods/scope-and-stakeholders.md).
- [Scope & Success Designer / スコープ・成功条件](../scope-success/index.md).
- [Evidence and provenance / 根拠と出典](../../fde/evidence-and-provenance.md).
- [Decision judgment and ontology design / 判断とオントロジー](../../fde/methods/decisions-and-ontology.md).
- [Diagnosis, value, and decision communication / 原因・価値・意思決定](../../fde/methods/diagnosis-and-value.md).
- [Ontology Builder Wizard / オントロジー設計](../../fde/ontology-builder/index.md).
- [Problem & Value Explorer / 課題・価値の探索](../../fde/problem-value/index.md).
- [Discovery Interviewer / 業務発見インタビュー [skill]](../../../skills/DISCOVERY_INTERVIEWER.md).
