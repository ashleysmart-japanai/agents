# quick-ref

A **quick-ref** points at code. Use it to name a location, not to prove a claim.

- The pointing form for terse-srp-dot-point docs (`style/DOT_POINT_SRP.md`); the evidence form is code-snip (`style/CODE_SNIP.md`).
- Form: `` `path/to/file.ts` `symbolName()` `` — the full repo path plus the class or function name.
- The symbol is the locator: it survives edits above it, and `grep` finds it.
- No line numbers — they go stale the moment anything above the symbol changes.
- Use the symbol's real name. Never coin a label for it.
- No symbol at the location (config, data, markdown) → `` `path/to/file.yaml` `` plus the key or heading.
- Several locations → one quick-ref each, on its own line.

## Where it is used

- Review store summary lines and `reverify:` targets (`review/ISSUE_TRACKING.md`).
- Spec and tasking-file references (`design/HUMAN_SPECS.md`, `design/AGENT_TASKING.md`).
- Checklist artifact items that passed (`review/REVIEW_METHOD.md`).

## Example

```
`src/auth/gate.ts` `checkAccess()`
`config/limits.yaml` `maxRetries`
```

## Chat exception

- A chat reply to the user may cite `path:line` instead — it is clickable, and the reply is read once, while it is fresh.
- Anything written to a file uses the quick-ref form.
