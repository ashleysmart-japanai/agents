# Code Review Skill

> **Path resolution**: All file references in this document (e.g. `review/CHECKLIST.md`, `tooling/TOOLING.md`) are relative to the directory containing this file, not the project being reviewed. If this file is at `/foo/agents/REVIEWER.md`, then `review/CHECKLIST.md` means `/foo/agents/review/CHECKLIST.md`. Project-specific files like `TESTING.md` should be looked for in the project's own root.

## Stage 1 — Gather & Analyze

1. **Gather context** — run these in parallel:
   - `git diff main...HEAD --stat` (scope)
   - `git diff main...HEAD` (full diff)
   - `git log --oneline main..HEAD` (commit history)

2. **Run checks** — detect language from changed files, run in parallel. See `tooling/TOOLING.md` / `tooling/TOOLING_<lang>.md` for per-language commands.
   - Lint, Format, Typecheck, Test
   - Fix all lint and format errors before proceeding
   - Ignore pre-existing typecheck errors in untouched files
   - If the project has a `TESTING.md` in its root, read it for project-specific test requirements

3. **Analyze the diff** — read every changed file. For each:
   - Does it do what the spec/task asked?
   - Does it break existing behavior?
   - Are imports used? Are exports consumed?
   - Are types correct (`any` usage, missing generics, wrong shapes)?
   - Are values passed correctly between layers (endpoint -> service -> data layer)?

4. **Check for regressions** — compare old vs new for each changed function/endpoint:
   - What did the old function return? What shape/type?
   - What does the new function return? Same contract?
   - Did the old code have filters or guards? Are they preserved?
   - Are callers updated to match any signature changes?

---

## Stage 2 — Check Groups

Run each check group against the diff. Every group produces a PASS / FAIL / N/A.

### Code quality & best practices
- Does the code follow the language's idiomatic style and conventions?
- Are naming, structure, and patterns consistent with the rest of the codebase?
- Is the code readable and maintainable?
- Is the function size limited? Is the code logically divided (SRP)?

### Bugs & edge cases
- Are there potential bugs or unhandled edge cases?
- Are error paths handled (null/empty, overflow, missing data, exceptions)?
- Does the API leave the system in a half state on failure, or does it recover correctly?

### Performance & efficiency
- Are there unnecessary loops, repeated work, or redundant allocations?
- Are there N+1 queries, unnecessary re-renders, or blocking calls?
- Does the code use fail-early/preflight checks to reduce wasted CPU and memory?
- Could verbose logic be replaced with a clearer standard library call or idiom?

### Readability & complexity
- Is the code easy to follow, or is it overly complex (deep nesting, spaghetti)?
- Are there premature abstractions or over-engineered patterns that add indirection without value?
- Could overly complex code be simplified?

### Security
- Any hardcoded keys, secrets, or "test" passwords left in?
- Does the API validate and clean inputs?
- Any new attack surface (injection, XSS, CSRF)?

### Optimizations & simplification
- Is there overly complex code that could be reduced?
- Could any section be simplified without losing correctness?
- Are there opportunities to reuse existing code instead of duplicating?

### Test quality
- Do test inputs match the actual function signatures?
- Do assertions match the actual return types and shapes?
- Are mocks/stubs compatible with real implementations?

### Checklist
- Read `review/CHECKLIST.md` and walk through every item against the diff.
- For each checklist category, note PASS / FAIL / N/A.
- List any failures with `file:line` references.

---

## Output Format

Begin with a brief summary of the overall code quality. Line numbers start at 1. If no issues are found, briefly state that the code meets best practices.

```
## Summary
2-3 sentences on what the PR does and whether the approach is sound.

## Checks
| Check | Result |
|-------|--------|
| Lint | PASS/FAIL |
| Format | PASS/FAIL |
| Typecheck | PASS/FAIL (note pre-existing errors) |
| Tests | PASS/FAIL (X tests) |

## Check Groups

### Code quality & best practices
| Check | Result |
|-------|--------|
| Follows language idioms and conventions | ✅/❌/N/A |
| Naming, structure consistent with codebase | ✅/❌/N/A |
| Readable and maintainable | ✅/❌/N/A |
| Function size limited, logically divided (SRP) | ✅/❌/N/A |

### Bugs & edge cases
| Check | Result |
|-------|--------|
| No potential bugs | ✅/❌/N/A |
| Error paths handled (null/empty, overflow, missing data) | ✅/❌/N/A |
| API recovers correctly on failure (no half-state) | ✅/❌/N/A |

### Performance & efficiency
| Check | Result |
|-------|--------|
| No unnecessary loops or repeated work | ✅/❌/N/A |
| No N+1 queries, unnecessary re-renders, or blocking calls | ✅/❌/N/A |
| Fail-early/preflight checks used | ✅/❌/N/A |
| Uses clear stdlib calls / idioms where possible | ✅/❌/N/A |

### Readability & complexity
| Check | Result |
|-------|--------|
| Code easy to follow (no deep nesting / spaghetti) | ✅/❌/N/A |
| No premature abstractions or over-engineering | ✅/❌/N/A |
| Overly complex code simplified where possible | ✅/❌/N/A |

### Security
| Check | Result |
|-------|--------|
| No hardcoded keys, secrets, or test passwords | ✅/❌/N/A |
| API validates and cleans inputs | ✅/❌/N/A |
| No new attack surface (injection, XSS, CSRF) | ✅/❌/N/A |

### Optimizations & simplification
| Check | Result |
|-------|--------|
| No overly complex code that could be reduced | ✅/❌/N/A |
| Sections simplified without losing correctness | ✅/❌/N/A |
| Reuses existing code instead of duplicating | ✅/❌/N/A |

### Test quality
| Check | Result |
|-------|--------|
| Test inputs match actual function signatures | ✅/❌/N/A |
| Assertions match actual return types and shapes | ✅/❌/N/A |
| Mocks/stubs compatible with real implementations | ✅/❌/N/A |

## Checklist
| Item | Result |
|------|--------|
| Big file checkins | PASS/FAIL/N/A |
| Hard coding | PASS/FAIL/N/A |
| Logic Check | PASS/FAIL/N/A |
| No Breakage | PASS/FAIL/N/A |
| Clean Naming | PASS/FAIL/N/A |
| Security | PASS/FAIL/N/A |
| Error Handling | PASS/FAIL/N/A |
| Readability | PASS/FAIL/N/A |
| Design (SOLID) | PASS/FAIL/N/A |
| Reuse | PASS/FAIL/N/A |
| Performance | PASS/FAIL/N/A |
| Thread safety & blocking | PASS/FAIL/N/A |
| UI sanity | PASS/FAIL/N/A |
| Comments | PASS/FAIL/N/A |
| Ready to Ship | PASS/FAIL/N/A |
| Dead code | PASS/FAIL/N/A |
| Dependency Audit | PASS/FAIL/N/A |
| Logging & Observability | PASS/FAIL/N/A |
| State Management | PASS/FAIL/N/A |
| Idempotency | PASS/FAIL/N/A |
| Local files | PASS/FAIL/N/A |
| Type Safety | PASS/FAIL/N/A |

## Findings

### Bugs (will break in production)
1. file:line — description

### Issues (functional risk)
1. file:line — description

### Optimizations (can be improved)
1. file:line — description

### Minor (style, consistency, docs)
1. file:line — description

## Verdict: LGTM / Needs Changes
One sentence on what blocks merge, if anything.
```

## Rules

- Be concise and direct. Lead with facts, not praise.
- Use `file:line` references for every finding.
- Distinguish bugs (will break) from issues (might break) from minor (won't break).
- Never flag pre-existing issues in files not touched by the PR.
- Never flag style preferences unless they violate repo conventions.
- All check groups and the checklist pass are mandatory — do not skip any.
- Run format check alongside lint — they are separate CI steps.
- Verify data flow end-to-end: endpoint -> service -> data layer -> response.
- For any refactored data-fetching: verify the old filters, mappings, and return types are all preserved.
