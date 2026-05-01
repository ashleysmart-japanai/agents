# Best Practices — Learned from Postmortems

This document is automatically maintained by the postmortem skill.
Each entry is derived from real postmortem reports in this directory.
Entries are sorted by occurrence count within each category.

---

## Code quality

| # | Practice | Occurrences | First seen |
|---|---|---|---|
| 1 | Run build + test + lint + typecheck before declaring done | 0 | — |
| 2 | Verify every new import resolves to a real file or package | 0 | — |
| 3 | Check for dead code, ghost imports, and TODO blocks before commit | 0 | — |

## Scope discipline

| # | Practice | Occurrences | First seen |
|---|---|---|---|
| 1 | Only modify files directly related to the task | 0 | — |
| 2 | Do not add formatting-only changes in unrelated files | 0 | — |
| 3 | Resist "while I'm here" refactors — file a separate task | 0 | — |

## Testing

| # | Practice | Occurrences | First seen |
|---|---|---|---|
| 1 | New behaviour must have new tests — no exceptions | 0 | — |
| 2 | Never delete or weaken existing tests to make the suite pass | 0 | — |
| 3 | Tests must assert the actual new behaviour, not just "no error" | 0 | — |

## Error handling

| # | Practice | Occurrences | First seen |
|---|---|---|---|
| 1 | Every new code path needs explicit error handling | 0 | — |
| 2 | Fail early with clear messages rather than propagating bad state | 0 | — |

## Security

| # | Practice | Occurrences | First seen |
|---|---|---|---|
| 1 | Scan diff for hardcoded secrets before commit | 0 | — |
| 2 | Validate inputs at system boundaries | 0 | — |

## Diff hygiene

| # | Practice | Occurrences | First seen |
|---|---|---|---|
| 1 | Keep diffs minimal and reviewable — one concern per commit | 0 | — |
| 2 | Avoid large auto-format diffs mixed with logic changes | 0 | — |

## Agent workflow

| # | Practice | Occurrences | First seen |
|---|---|---|---|
| 1 | Read existing code before writing — context prevents hallucination | 0 | — |
| 2 | Run the full check suite after every significant change, not just at the end | 0 | — |
| 3 | When a build fails, diagnose root cause before retrying — don't loop blindly | 0 | — |

---

*Last updated: —*
*Total reports analyzed: 0*
