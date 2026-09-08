# Task File

The grammar of `task.md`, the coder's task context file. `ISSUE_TRACKING.md` owns the rest of the review directory; this file owns `task.md`.

## Rules

- `task.md` is a sibling of `review.md` in the review directory.
- `task.md` is not the tasking file: `agent_tasking.md` is the agent's spec in the repo (`design/AGENT_SPECS.md` § Tasking file); `task.md` is the review-store context file with user-owned content.
- The coder owns `task.md`; reviewers and subagents read it, never edit it.
- No update to `task.md` without the user's approval.
  - Propose the exact text in chat; write it only after the user approves.
- Record the user's text as close to verbatim as possible.
  - Allowed corrections: grammar, spelling, and expanding shorthand.
  - Not allowed: rephrasing, summarising in the agent's own words, or adding content the user did not say.
- Create `task.md` at task start.
- Write it in dot-point-srp style (`~/agents/style/DOT_POINT_SRP.md`).
- Three top-level sections, always in this order: `# GOAL`, `# STATUS`, `# DECISIONS`.
- No other top-level sections.
- `# GOAL` — what the task is for this PR.
  - Written at task start.
  - Changes only when the user changes scope.
- `# STATUS` — a summary of where the work is at.
  - Rewritten in place at each update.
  - Proposed after each push and at session end; written on approval.
- `# DECISIONS` — a linear log of direction-affecting decisions and the reason(s) for each.
  - Entry gate: only major actions and direction shifts qualify — calls that change what gets built.
  - An entry that fails the gate is not appended.
  - Minor choices, task steps, and work narration never pass the gate.
  - Tag each entry with a short kebab-case name for the decision (e.g. `spec-before-code`, `record-not-resource`).
  - Entry format: `- <yyyy-mm-dd> - <tag> - <decision> — <reason(s)>`.
  - One entry per decision, trimmed to the call and its reason — no blather.
  - Append-only: never rewrite, delete, or reorder entries.
  - Appended when the decision is made, in the user's words — not reconstructed later.
  - A reversed decision gets a new entry naming the entry it reverses.

## Example

```markdown
# GOAL
- Extract the record adapter behind a capability interface for this PR.

# STATUS
- Adapter extracted; create path green; browse slice pending.

# DECISIONS
- 2026-06-10 - tasking-before-code - Write and commit the tasking file, then stop before implementation.
- 2026-06-11 - no-root-sentinel - No fake `current` value — it enables the create button and guarantees an upstream failure.

```

## Validation

- `scripts/validate_review.py` checks the section order and the `# DECISIONS` entry grammar.
