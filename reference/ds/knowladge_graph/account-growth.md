# Account Growth Planner / アカウント成長計画

- **View:** this diagram renders in a Markdown viewer with Mermaid support.
- **Data:** [account-growth.json](account-growth.json).
- **Boundary:** converted source slides/notes are excluded from this skill context.

```mermaid
flowchart TD
  n0["Account Growth Planner / アカウント成長計画 — failure patterns / 失敗パターン"]
  n1["Account Growth Planner / アカウント成長計画"]
  n2["Account Growth Planner / アカウント成長計画 — worksheet / ワークシート"]
  n3["Product reuse and account growth / 製品再利用と成長"]
  n4["Scope, success, and stakeholders / スコープ・成功・関係者"]
  n5["Product Opportunity Scout / 製品化機会の探索"]
  n6["Scope &amp; Success Designer / スコープ・成功条件"]
  n7["Evidence and provenance / 根拠と出典"]
  n8["Decision judgment and ontology design / 判断とオントロジー"]
  n9["Diagnosis, value, and decision communication / 原因・価値・意思決定"]
  n10["Problem &amp; Value Explorer / 課題・価値の探索"]
  n11["Account Growth Planner / アカウント成長計画 [skill]"]
  n0 -->|references| n1
  n0 -->|derived_from| n3
  n1 -->|checks_with| n0
  n1 -->|produces| n2
  n1 -->|derived_from| n3
  n1 -->|references| n5
  n1 -->|references| n6
  n1 -->|references| n7
  n1 -->|references| n10
  n1 -->|references| n11
  n2 -->|references| n1
  n2 -->|derived_from| n3
  n2 -->|references| n7
  n3 -->|references| n1
  n3 -->|references| n5
  n4 -->|references| n6
  n5 -->|references| n1
  n5 -->|derived_from| n3
  n5 -->|references| n7
  n5 -->|references| n10
  n6 -->|derived_from| n4
  n6 -->|references| n7
  n6 -->|references| n10
  n7 -->|derived_from| n4
  n7 -->|derived_from| n8
  n9 -->|references| n10
  n10 -->|references| n6
  n10 -->|references| n7
  n10 -->|derived_from| n9
  n11 -->|uses| n0
  n11 -->|uses| n1
  n11 -->|uses| n2
  n11 -->|derived_from| n3
```

## Knowledge pages

- [Account Growth Planner / アカウント成長計画 — failure patterns / 失敗パターン](../account-growth/failure-patterns.md).
- [Account Growth Planner / アカウント成長計画](../account-growth/index.md).
- [Account Growth Planner / アカウント成長計画 — worksheet / ワークシート](../account-growth/worksheet.md).
- [Product reuse and account growth / 製品再利用と成長](../methods/product-reuse-and-growth.md).
- [Scope, success, and stakeholders / スコープ・成功・関係者](../methods/scope-and-stakeholders.md).
- [Product Opportunity Scout / 製品化機会の探索](../product-opportunity/index.md).
- [Scope & Success Designer / スコープ・成功条件](../scope-success/index.md).
- [Evidence and provenance / 根拠と出典](../../fde/evidence-and-provenance.md).
- [Decision judgment and ontology design / 判断とオントロジー](../../fde/methods/decisions-and-ontology.md).
- [Diagnosis, value, and decision communication / 原因・価値・意思決定](../../fde/methods/diagnosis-and-value.md).
- [Problem & Value Explorer / 課題・価値の探索](../../fde/problem-value/index.md).
- [Account Growth Planner / アカウント成長計画 [skill]](../../../skills/ACCOUNT_GROWTH.md).
