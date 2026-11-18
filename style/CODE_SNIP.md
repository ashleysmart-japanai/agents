# code-snip

A **code-snip** proves a claim. Use it as evidence, where a reader must see the code to check the point.

- The evidence form for terse-srp-dot-point docs (`style/DOT_POINT_SRP.md`); the pointing form is quick-ref (`style/QUICK_REF.md`).
- Form: a quick-ref (`style/QUICK_REF.md`) followed by a fenced block holding the 2–5 lines that carry the point.
- Quote the lines verbatim from current HEAD. Never paraphrase, retype, or reformat them.
- 2–5 lines, not the whole function: the lines the claim turns on, plus only the context needed to read them.
- Longer than 5 lines → the claim covers too much; split it, or name the steps as quick-refs and snip only the one that fails.
- No line numbers in or around the block — the quoted text is the locator, and `grep` finds it.
- The snippet is the evidence; the prose says what is wrong with it, not what it says.

## Where it is used

- `<ID>.md` evidence sections in the review store (`review/ISSUE_TRACKING.md`).
- Failed checklist items (`review/CODE_REVIEW.md`, `review/REVIEW_METHOD.md`).
- Root-cause claims in a diagnosis (`DIAG.md`).
- Any review finding stating that code is wrong.

## Example

```
`src/auth/gate.ts` `checkAccess()`

    if (!perms.length) return ALLOW;

Empty permission set returns ALLOW — present-but-empty must deny (CODER.md § Fail-closed defaults).
```

## Chat exception

- A chat reply to the user may cite `path:line` alongside the snippet — it is clickable, and the reply is read once, while it is fresh.
- Anything written to a file uses the code-snip form alone.
