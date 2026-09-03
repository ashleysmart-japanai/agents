# Dot-Point SRP Style

The writing style for guideline docs, specs, `task.md`, and status reports.

- Use `-` dot points.
- One clause per line.
- Each clause is terse, to the point, and single-responsibility: one instruction, one fact, or one decision.
- A clause carrying two responsibilities is two clauses — split it.
- Sub-clauses go in a sub-list nested under their parent clause.
- Do not hand-wrap lines; let the editor wrap.
- No filler: no preamble, no restating, no closing summary.

Example:

```md
- Push to the PR branch after each completed change.
- Do not merge PRs.
  - Merging is done by the user.
```
