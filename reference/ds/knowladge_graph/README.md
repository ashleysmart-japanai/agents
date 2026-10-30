# DS knowledge graph

- **Rebuild:** run `python3 scripts/build_knowledge_graphs.py` from the repository root.
- **Validate:** run `python3 scripts/build_knowledge_graphs.py --check`.
- **Overview:** a compact map of tools, skills, and digested methods.
- **Full graph:** [ds.json](ds.json).
- **Source boundary:** background slide and note archives are not default skill knowledge.

```mermaid
flowchart TD
  n0["Account Growth Planner / アカウント成長計画"]
  n1["Discovery Interviewer / 業務発見インタビュー"]
  n2["Discovery and responsibility / 業務発見と責任"]
  n3["Product reuse and account growth / 製品再利用と成長"]
  n4["Scope, success, and stakeholders / スコープ・成功・関係者"]
  n5["Ownership &amp; Handoff Designer / 責任分担・引き継ぎ"]
  n6["Product Opportunity Scout / 製品化機会の探索"]
  n7["Scope &amp; Success Designer / スコープ・成功条件"]
  n8["Stakeholder &amp; Conversation Planner / 関係者・対話計画"]
  n9["Account Growth Planner / アカウント成長計画 [skill]"]
  n10["Advise me / 次の一手を相談する [skill]"]
  n11["Discovery Interviewer / 業務発見インタビュー [skill]"]
  n12["DS scope checker [skill]"]
  n13["Ownership &amp; Handoff Designer / 責任分担・引き継ぎ [skill]"]
  n14["Product Opportunity Scout / 製品化機会の探索 [skill]"]
  n15["Scope &amp; Success Designer / スコープ・成功条件 [skill]"]
  n16["Stakeholder &amp; Conversation Planner / 関係者・対話計画 [skill]"]
  n0 -->|derived_from| n3
  n0 -->|references| n6
  n0 -->|references| n7
  n0 -->|references| n9
  n1 -->|derived_from| n2
  n1 -->|references| n7
  n1 -->|references| n11
  n2 -->|references| n1
  n2 -->|references| n5
  n3 -->|references| n0
  n3 -->|references| n6
  n4 -->|references| n7
  n4 -->|references| n8
  n5 -->|derived_from| n2
  n5 -->|references| n7
  n5 -->|references| n13
  n6 -->|references| n0
  n6 -->|derived_from| n3
  n6 -->|references| n14
  n7 -->|derived_from| n4
  n7 -->|references| n5
  n7 -->|references| n8
  n7 -->|references| n12
  n7 -->|references| n15
  n8 -->|derived_from| n4
  n8 -->|references| n7
  n8 -->|references| n16
  n9 -->|uses| n0
  n9 -->|derived_from| n3
  n10 -->|derived_from| n2
  n10 -->|derived_from| n4
  n11 -->|uses| n1
  n11 -->|derived_from| n2
  n12 -->|derived_from| n4
  n12 -->|uses| n8
  n13 -->|derived_from| n2
  n13 -->|uses| n5
  n14 -->|derived_from| n3
  n14 -->|uses| n6
  n15 -->|derived_from| n4
  n15 -->|uses| n7
  n15 -->|uses| n12
  n16 -->|derived_from| n4
  n16 -->|uses| n8
```

## Skill graphs

- [account-growth](account-growth.md).
- [advise-me](advise-me.md).
- [discovery-interviewer](discovery-interviewer.md).
- [ds-scope-checker](ds-scope-checker.md).
- [ownership-handoff](ownership-handoff.md).
- [product-opportunity](product-opportunity.md).
- [scope-success](scope-success.md).
- [stakeholder-conversation](stakeholder-conversation.md).
