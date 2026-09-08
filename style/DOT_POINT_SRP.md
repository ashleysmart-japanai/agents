# Dot-Point SRP Style

The writing style for guideline docs, specs, `task.md`, status reports, and chat responses.

- Use `-` dot points.
- One clause per line.
- Each clause is terse, to the point, and single-responsibility: one instruction, one fact, or one decision.
- A clause carrying two responsibilities is two clauses — split it.
- Sub-clauses go in a sub-list nested under their parent clause.
- Do not hand-wrap lines; let the editor wrap.
- No filler: no preamble, no restating, no closing summary.
- List-first: any content with more than one item is a list — not paragraphs to sound conversational.
  - A one-line answer needs no list.
- Bold the lead term or verdict of a line; headers separate sections.
- Quote code and source text in markdown: `inline code`, fenced blocks, `>` block quotes.
  - Not HTML (`<pre>`, `<code>`, …).
- Cite code as `path:line`; quote the 2–5 lines that carry the point.

## SOLID statements

Statements follow SOLID; the open/closed principle is where docs usually go wrong.

- Single responsibility: the clause rules above — one instruction, fact, or decision per line.
- Open/closed: a statement is open for extension and closed for alteration.
  - State what a thing adds or does — it stays true when other work touches the same module.
  - Do not enumerate what a thing has — the list goes stale the moment a parallel change lands.
  - GOOD: "module A will add action XYZ".
  - BAD: "module A has actions [MNO, XYZ]".
- No hyperbole: no "must", "absolute", "the only", "the one", "chief", "hardest".
  - State the rule; intensifiers add nothing and read as closure.
  - Prefer "a turn ends at X" over "a turn ends only at X".

Example:

```md
- Push to the PR branch after each completed change.
- Do not merge PRs.
  - Merging is done by the user.
```
