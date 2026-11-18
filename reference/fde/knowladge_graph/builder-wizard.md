# Ontology Builder Wizard / オントロジー設計

- **View:** this diagram renders in a Markdown viewer with Mermaid support.
- **Data:** [builder-wizard.json](builder-wizard.json).
- **Boundary:** converted source slides/notes are excluded from this skill context.

```mermaid
flowchart TD
  n0["domain-driven-design"]
  n1["Discovery Interviewer / 業務発見インタビュー"]
  n2["Discovery and responsibility / 業務発見と責任"]
  n3["Scope, success, and stakeholders / スコープ・成功・関係者"]
  n4["Scope &amp; Success Designer / スコープ・成功条件"]
  n5["Evidence and provenance / 根拠と出典"]
  n6["Decision judgment and ontology design / 判断とオントロジー"]
  n7["Diagnosis, value, and decision communication / 原因・価値・意思決定"]
  n8["Actions and impact tracing / アクションと影響"]
  n9["Competency questions / モデルが答える問い"]
  n10["Ontology discovery and graph editing / 設計と編集"]
  n11["Ontology Builder Wizard / オントロジー設計 — failure patterns / 失敗パターン"]
  n12["Ontology Builder Wizard / オントロジー設計"]
  n13["Source mapping and gaps / データ対応と食い違い"]
  n14["Ontology Builder Wizard / オントロジー設計 — worksheet / ワークシート"]
  n15["Problem &amp; Value Explorer / 課題・価値の探索"]
  n16["Ontology Builder Wizard / オントロジー設計 [skill]"]
  n17["Ontology Designer / オントロジー設計 [skill]"]
  n1 -->|derived_from| n2
  n1 -->|references| n4
  n1 -->|references| n5
  n1 -->|references| n12
  n1 -->|references| n15
  n2 -->|references| n1
  n3 -->|references| n4
  n4 -->|derived_from| n3
  n4 -->|references| n5
  n4 -->|references| n15
  n5 -->|derived_from| n3
  n5 -->|derived_from| n6
  n6 -->|references| n12
  n7 -->|references| n15
  n8 -->|derived_from| n6
  n8 -->|references| n12
  n8 -->|produces| n14
  n9 -->|derived_from| n6
  n9 -->|references| n12
  n9 -->|produces| n14
  n10 -->|references| n0
  n10 -->|derived_from| n6
  n10 -->|references| n12
  n10 -->|references| n16
  n11 -->|derived_from| n6
  n11 -->|references| n12
  n12 -->|references| n1
  n12 -->|references| n4
  n12 -->|references| n5
  n12 -->|derived_from| n6
  n12 -->|references| n8
  n12 -->|references| n9
  n12 -->|checks_with| n11
  n12 -->|references| n13
  n12 -->|produces| n14
  n12 -->|references| n15
  n12 -->|references| n16
  n12 -->|references| n17
  n13 -->|derived_from| n6
  n13 -->|references| n12
  n13 -->|produces| n14
  n14 -->|references| n5
  n14 -->|derived_from| n6
  n14 -->|references| n12
  n15 -->|references| n1
  n15 -->|references| n4
  n15 -->|references| n5
  n15 -->|derived_from| n7
  n16 -->|derived_from| n6
  n16 -->|uses| n11
  n16 -->|uses| n12
  n16 -->|uses| n14
  n16 -->|uses| n17
  n17 -->|derived_from| n6
  n17 -->|uses| n12
  n17 -->|uses| n14
```

## Knowledge pages

- [domain-driven-design](../../design-principles/domain-driven-design.md).
- [Discovery Interviewer / 業務発見インタビュー](../../ds/discovery-interviewer/index.md).
- [Discovery and responsibility / 業務発見と責任](../../ds/methods/discovery-and-ownership.md).
- [Scope, success, and stakeholders / スコープ・成功・関係者](../../ds/methods/scope-and-stakeholders.md).
- [Scope & Success Designer / スコープ・成功条件](../../ds/scope-success/index.md).
- [Evidence and provenance / 根拠と出典](../evidence-and-provenance.md).
- [Decision judgment and ontology design / 判断とオントロジー](../methods/decisions-and-ontology.md).
- [Diagnosis, value, and decision communication / 原因・価値・意思決定](../methods/diagnosis-and-value.md).
- [Actions and impact tracing / アクションと影響](../ontology-builder/actions-and-impact.md).
- [Competency questions / モデルが答える問い](../ontology-builder/competency-questions.md).
- [Ontology discovery and graph editing / 設計と編集](../ontology-builder/discovery-and-editing.md).
- [Ontology Builder Wizard / オントロジー設計 — failure patterns / 失敗パターン](../ontology-builder/failure-patterns.md).
- [Ontology Builder Wizard / オントロジー設計](../ontology-builder/index.md).
- [Source mapping and gaps / データ対応と食い違い](../ontology-builder/source-mapping.md).
- [Ontology Builder Wizard / オントロジー設計 — worksheet / ワークシート](../ontology-builder/worksheet.md).
- [Problem & Value Explorer / 課題・価値の探索](../problem-value/index.md).
- [Ontology Builder Wizard / オントロジー設計 [skill]](../../../skills/BUILDER_WIZARD.md).
- [Ontology Designer / オントロジー設計 [skill]](../../../skills/ONTOLOGY_SKETCHER.md).
