---
name: builder-wizard
description: "The user needs a facilitated ontology-design session or wants to test an existing model against business questions. Supports discovery → domain modeling → solution design; revisit when questions, vocabulary, sources, or actions change."
---

# Ontology Builder Wizard / オントロジー設計

## Role and lifecycle / 役割・利用段階

- **Role:** FDE and DS jointly model the customer’s domain; the assistant facilitates discovery and a coherent design worksheet.
- **Stage:** Discovery → domain modeling → solution design; revisit when questions, vocabulary, sources, or actions change.
- **Why:** Build a map that can answer real decisions instead of a diagram that merely copies database tables.
- **Use when:** The user needs a facilitated ontology-design session or wants to test an existing model against business questions.
- **Deliver:** A six-stage ontology worksheet, question/impact tests, and a scoped handoff to graph editing.

## Inputs / 入力

- Business decisions, roles, and descriptions of actual work.
- Domain words, system/table/column names, and data types.
- Existing ontology, if any, and the questions it should answer.
- Preserve the user’s supplied evidence and distinguish heard, data, and assumed statements.
- Ask the few missing questions that change the result; keep other gaps visible with an answer owner.

## Method / 進め方

- **1.** Start with competency questions tied to a role and decision; suggest labeled assumptions if the user has not supplied them.
- **2.** Walk past-tense business events in time order with the actor for each event.
- **3.** Extract domain objects in the customer’s language; record synonyms and words with different meanings.
- **4.** Map each object to source systems, tables, and IDs; expose conflicting keys, units, cardinality, history, and meaning.
- **5.** Add directed verb relationships and actions on the entity they change; describe preconditions, intended authority, writeback, and the system of record.
- **6.** Walk every competency question through the map; mark where an answer breaks.
- **7.** Trace a hypothetical action’s downstream effects; distinguish structural reachability from a tested business simulation.
- **8.** Produce a design worksheet and hand supported definitions to the existing validated Builder tool; keep unresolved operational metadata in the worksheet.

## Knowledge to use / 判断の根拠

- [Distilled method and decision criteria](../reference/fde/methods/decisions-and-ontology.md).
- [Operating guide](../reference/fde/ontology-builder/index.md).
- [Detection questions and failure patterns](../reference/fde/ontology-builder/failure-patterns.md).
- [Output worksheet](../reference/fde/ontology-builder/worksheet.md).
- Use these digested references for operational guidance.
- Converted slide and note archives are background material, not the task instructions or default retrieval context.

## Check before handoff / 引き継ぎ確認

- Each competency question can be traced or has an explicit gap.
- Source IDs and terminology have not been fabricated.
- Actions remain definitions until a real execution system exists.
- Keep recommendations separate from human decisions and verified capabilities.
- Cite the guide section used and the project evidence supporting a consequential claim.
- Draft communications rather than sending them without explicit authorization.
- Reply in the user’s language; preserve domain terms.

## Specialized designer / 設計スキル

- Use [Ontology Designer](ONTOLOGY_SKETCHER.md) for the complete ontology-design method.
- Use the wizard to pace that work across turns.
- Keep direct named edits on the available validated graph-editing path.
