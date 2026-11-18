# Ontology discovery and graph editing / 設計と編集

- **Purpose:** add a systematic design assistant without weakening the existing graph-edit contract.

## Adopt / 採用

- Start open-ended ontology discovery from business decisions and competency questions.
- Walk events with actors before extracting objects.
- Preserve domain words and expose synonyms and ambiguous meanings.
- Map objects to systems, tables, identifiers, and joins.
- Record unit, source, cardinality, status, and history gaps with answer owners.
- Test question paths and trace a hypothetical action’s consequences.
- Label heard, data, and assumed statements.

## Keep distinct / 分担

- **Builder Wizard:** guides discovery and produces a design worksheet.
- **Existing Builder:** creates or edits supported entities, relationships, property definitions, and action definitions through its validated tool.
- **Direct edits:** adding a named property, action, or relationship does not require completing the discovery method.
- **Explicit catalogs:** preserve the requested catalog size; a small starter suggestion is a discovery default.
- **Canonical schema:** do not add invented unit/source/permissions fields to strict property or action definitions.
- **Operational design:** keep permissions, writeback, and system-of-record questions in the worksheet unless a supported representation is agreed.
- **Impact tracing:** following relationships is not execution or validated business simulation.
- **Privacy:** structure-only discovery does not mean an assistant may silently remove authorized data from an existing graph.
- **Provisioning:** verify an available execution system before claiming that a design creates runtime resources.

## Entry points / 入口

- [Ontology operating guide](index.md).
- [Builder Wizard skill](../../../skills/BUILDER_WIZARD.md).
- [Domain-driven design reference](../../design-principles/domain-driven-design.md).


## Knowledge reference / 判断の根拠

- [Decision and ontology methods](../methods/decisions-and-ontology.md).
