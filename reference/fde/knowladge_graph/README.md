# FDE knowledge graph

- **Rebuild:** run `python3 scripts/build_knowledge_graphs.py` from the repository root.
- **Validate:** run `python3 scripts/build_knowledge_graphs.py --check`.
- **Overview:** a compact map of tools, skills, and digested methods.
- **Full graph:** [fde.json](fde.json).
- **Source boundary:** background slide and note archives are not default skill knowledge.

```mermaid
flowchart TD
  n0["Customer Conversation Rehearsal / 顧客対話の練習"]
  n1["Decision Advisor / 判断の整理"]
  n2["Deployment Planner / 導入計画"]
  n3["Decision judgment and ontology design / 判断とオントロジー"]
  n4["Delivery ownership and adversarial review / 導入責任と批判的レビュー"]
  n5["Diagnosis, value, and decision communication / 原因・価値・意思決定"]
  n6["Production readiness and positioning / 本番準備と価値の説明"]
  n7["Murderboard / マーダーボード"]
  n8["Ontology Builder Wizard / オントロジー設計"]
  n9["Problem &amp; Value Explorer / 課題・価値の探索"]
  n10["Production Readiness Review / 本番準備レビュー"]
  n11["Steering &amp; Escalation Planner / 運営会議・エスカレーション"]
  n12["Advise me / 次の一手を相談する [skill]"]
  n13["Ontology Builder Wizard / オントロジー設計 [skill]"]
  n14["Customer Conversation Rehearsal / 顧客対話の練習 [skill]"]
  n15["Decision Advisor / 判断の整理 [skill]"]
  n16["Deployment Planner / 導入計画 [skill]"]
  n17["Murderboard / マーダーボード [skill]"]
  n18["Ontology Designer / オントロジー設計 [skill]"]
  n19["Problem &amp; Value Explorer / 課題・価値の探索 [skill]"]
  n20["Production Readiness Review / 本番準備レビュー [skill]"]
  n21["Steering &amp; Escalation Planner / 運営会議・エスカレーション [skill]"]
  n0 -->|derived_from| n6
  n0 -->|references| n9
  n0 -->|references| n10
  n0 -->|references| n14
  n1 -->|derived_from| n3
  n1 -->|references| n10
  n1 -->|references| n11
  n1 -->|references| n15
  n2 -->|derived_from| n4
  n2 -->|references| n9
  n2 -->|references| n10
  n2 -->|references| n16
  n3 -->|references| n1
  n3 -->|references| n8
  n4 -->|references| n2
  n4 -->|references| n7
  n5 -->|references| n9
  n5 -->|references| n11
  n6 -->|references| n0
  n6 -->|references| n10
  n7 -->|derived_from| n4
  n7 -->|references| n9
  n7 -->|references| n10
  n7 -->|references| n17
  n8 -->|derived_from| n3
  n8 -->|references| n9
  n8 -->|references| n13
  n8 -->|references| n18
  n9 -->|derived_from| n5
  n9 -->|references| n11
  n9 -->|references| n19
  n10 -->|references| n0
  n10 -->|derived_from| n6
  n10 -->|references| n7
  n10 -->|references| n20
  n11 -->|references| n1
  n11 -->|derived_from| n5
  n11 -->|references| n9
  n11 -->|references| n21
  n12 -->|derived_from| n3
  n13 -->|derived_from| n3
  n13 -->|uses| n8
  n13 -->|uses| n18
  n14 -->|uses| n0
  n14 -->|derived_from| n6
  n15 -->|uses| n1
  n15 -->|derived_from| n3
  n16 -->|uses| n2
  n16 -->|derived_from| n4
  n17 -->|derived_from| n4
  n17 -->|uses| n7
  n18 -->|derived_from| n3
  n18 -->|uses| n8
  n19 -->|derived_from| n5
  n19 -->|uses| n9
  n20 -->|derived_from| n6
  n20 -->|uses| n10
  n21 -->|derived_from| n5
  n21 -->|uses| n11
```

## Skill graphs

- [advise-me](advise-me.md).
- [builder-wizard](builder-wizard.md).
- [customer-conversation](customer-conversation.md).
- [decision-advisor](decision-advisor.md).
- [deployment-planner](deployment-planner.md).
- [murderboard](murderboard.md).
- [ontology-sketcher](ontology-sketcher.md).
- [problem-value](problem-value.md).
- [production-readiness](production-readiness.md).
- [steering-escalation](steering-escalation.md).
