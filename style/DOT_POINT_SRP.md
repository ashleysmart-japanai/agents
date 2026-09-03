# Dot-Point SRP Style

The writing style for guideline docs, specs, `task.md`, status reports, and chat responses.

- Use `-` dot points.
- One clause per line.
- Each clause is terse, to the point, and single-responsibility: one instruction, one fact, or one decision.
- A clause carrying two responsibilities is two clauses — split it.
- Sub-clauses go in a sub-list nested under their parent clause.
- Do not hand-wrap lines; let the editor wrap.
- No filler: no preamble, no restating, no closing summary.
- List-first: any content with more than one item is a list — never paragraphs to sound conversational.
  - A one-line answer needs no list.
- Bold only the lead term or verdict of a line; headers only to separate sections.
- Quote code and source text in markdown only: `inline code`, fenced blocks, `>` block quotes.
  - Never HTML: no `<pre>`, `<code>`, `<blockquote>`.
- Cite code as `path:line`; quote the 2–5 lines that carry the point.

Example:

```md
- Push to the PR branch after each completed change.
- Do not merge PRs.
  - Merging is done by the user.
```
