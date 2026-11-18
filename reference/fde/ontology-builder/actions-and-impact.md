# Actions and impact tracing / アクションと影響

- **Use:** describe what changes an object and test what else that change might affect.

## Action design / 設計

- Put the action on the entity whose state it changes.
- Describe the intended input, precondition, and state transition.
- Record who should be allowed to perform it as a design question.
- Describe the intended code, model, or workflow only when known.
- Record any writeback target and the system of record.
- Identify the log, verification, or human confirmation the intended process needs.

## Impact walkthrough / 影響確認

- Choose a hypothetical action and a starting entity.
- Follow the relationships in the relevant direction.
- State which downstream facts or decisions might change and why.
- Mark where a missing business rule prevents predicting the result.
- Recheck the competency questions affected by the change.
- Treat reachability as a list of potentially affected objects, not a proven state transition or numeric simulation.

## graph editor handoff / 引き継ぎ

- An action definition has a key, label, and description.
- The current graph editor does not execute actions or enforce their permissions.
- Keep unsupported operational metadata in the design worksheet.
- Use an available validated Builder tool for actual definition edits.

## Continue / 続き

- [Tool guide](index.md).
- [Output worksheet](worksheet.md).
- [Source record](../methods/decisions-and-ontology.md).
