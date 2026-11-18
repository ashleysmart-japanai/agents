# Decision judgment and ontology design / 判断とオントロジー

## Judgment / 判断

- Examine whether an action can be undone.
- Examine who and what it affects beyond the immediate workspace.
- Consider unknown restore behavior and downstream consequences explicitly.
- Bring customer scope, priorities, or commercial questions to the appropriate business owner.
- Bring shared implementation questions to the relevant technical owner.
- Apply current project authorization and policy rather than installing a new approval rule from a generic matrix.

## Coordination / 連携

- A useful check-in records goal, decided, consulted, stopped, waiting, and recurring pattern.
- A useful help request names the needed action and the role able to take it.
- Keep waiting dependencies visible before they become a surprise.

## Six ontology stages / 六段階

- **Decisions:** write competency questions a business role needs answered.
- **Events:** reconstruct past-tense events in order with their actors.
- **Vocabulary:** identify domain objects, synonyms, and ambiguous terms.
- **Sources:** map each object to actual systems, tables, and identifiers.
- **Relationships/actions:** express verb links and changes to objects.
- **Tests:** walk each question and trace the consequences of one hypothetical change.
- Suggest a small first sketch when the task is open-ended.
- Preserve the full catalog when the user supplies an explicit larger model.

## Data semantics / データの意味

- Record units, meaning, source, and identity separately from a property’s primitive type.
- Check incompatible IDs, formatting differences, missing joins, multiple values, free-text meaning, and missing history.
- Check whether the same status word has different meanings in different contexts.
- An object can be derived from several sources without appearing as a stored table.
- Do not invent a source column to make the design appear complete.

## Actions and tests / 変更と確認

- Put an action on the object it changes.
- Describe the intended precondition, actor, state change, and writeback target.
- Treat permissions and execution mechanisms as design questions until implemented.
- Question traversal tests whether the model contains the information needed for an answer.
- An impact trace identifies potentially affected objects; it is not a validated business simulation.
- Keep unsupported metadata in a worksheet instead of adding unknown fields to a strict graph format.

## Example / 例

- A complaint question needs Call, Complaint, Policy, and Staff objects.
- If the complaint source lacks a call identifier, the answer path breaks at that join.
- Record that gap and the role who can confirm how calls are matched.
- A schema diagram alone does not prove the join is possible.

## Apply / 実務で使う

- [Decision Advisor / 判断の整理](../decision-advisor/index.md).
- [Ontology Builder Wizard / オントロジー設計](../ontology-builder/index.md).
