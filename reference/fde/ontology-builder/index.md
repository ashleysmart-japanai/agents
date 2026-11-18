# Ontology Builder Wizard / オントロジー設計

## Purpose / 目的

- Build a testable shared model of a customer’s world from decisions, vocabulary, and data structure.
- **Format:** agent-assisted work tool; these guides do not provision an application or execute external systems.

## Bring / 入力

- Business decisions, roles, and descriptions of actual work.
- Domain words, system/table/column names, and data types.
- Existing ontology, if any, and the questions it should answer.

## How to run / 進め方

- **1.** Start with competency questions tied to a role and decision; suggest labeled assumptions if the user has not supplied them.
- **2.** Walk past-tense business events in time order with the actor for each event.
- **3.** Extract domain objects in the customer’s language; record synonyms and words with different meanings.
- **4.** Map each object to source systems, tables, and IDs; expose conflicting keys, units, cardinality, history, and meaning.
- **5.** Add directed verb relationships and actions on the entity they change; describe preconditions, intended authority, writeback, and the system of record.
- **6.** Walk every competency question through the map; mark where an answer breaks.
- **7.** Trace a hypothetical action’s downstream effects; distinguish structural reachability from a tested business simulation.
- **8.** Produce a design worksheet and hand supported definitions to the existing validated Builder tool; keep unresolved operational metadata in the worksheet.

## Check the result / 確認

- Each competency question can be traced or has an explicit gap.
- Source IDs and terminology have not been fabricated.
- Actions remain definitions until a real execution system exists.

## Working pages / 関連ページ

- [Output worksheet / 成果物](worksheet.md)
- [Failure patterns / 失敗パターン](failure-patterns.md)
- [Agent skill / エージェントスキル](../../../skills/BUILDER_WIZARD.md)
- [Evidence and provenance / 根拠と出典](../evidence-and-provenance.md)
- [Discovery Interviewer / 業務発見インタビュー](../../ds/discovery-interviewer/index.md)
- [Problem & Value Explorer / 課題・価値の探索](../problem-value/index.md)
- [Scope & Success Designer / スコープ・成功条件](../../ds/scope-success/index.md)

## Sources / 出典

- [Method reference](../methods/decisions-and-ontology.md)
- **Adaptation:** tool packaging, persistent artifacts, and graph editor handoffs are proposed implementation choices.

## Detailed guides / 詳細ガイド

- [Competency questions / モデルが答える問い](competency-questions.md).
- [Source mapping and gaps / データ対応と食い違い](source-mapping.md).
- [Actions and impact tracing / アクションと影響](actions-and-impact.md).

- [Ontology Designer skill](../../../skills/ONTOLOGY_SKETCHER.md).
