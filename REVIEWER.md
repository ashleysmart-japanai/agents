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
   - **Trace callers**: who calls the changed function? Do upstream preconditions contradict the new logic?
   - **Find parallel paths**: are there other code paths that perform the same operation? Does the fix apply to all of them?

4. **Check for regressions** — compare old vs new for each changed function/endpoint:
   - What did the old function return? What shape/type?
   - What does the new function return? Same contract?
   - Did the old code have filters or guards? Are they preserved?
   - Are callers updated to match any signature changes?
   - If a validation or guard was weakened/removed, do all paths behind it still have equivalent protection?
   - Does the fix introduce a worse failure mode than the original bug on any path? (e.g., silent data corruption replacing a safe 400 error)

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
- When new data fetches are added, is the same data already available from a previous step in the call chain?

### Readability & complexity
- Is the code easy to follow, or is it overly complex (deep nesting, spaghetti)?
- Are there premature abstractions or over-engineered patterns that add indirection without value?
- Could overly complex code be simplified?

### Security
- Any hardcoded keys, secrets, or "test" passwords left in?
- Does the API validate and clean inputs?
- Any new attack surface (injection, XSS, CSRF)?

### Route safety (Next.js / file-based routers)
- Do new static route files sit alongside a `[param].ts` dynamic route in the same directory? If so, the dynamic route may shadow the static file — move static routes into a subdirectory (e.g. `actions/`) to avoid ambiguity.
- Are all fetch paths in frontend code consistent with the actual route file locations?

### Shims & dead indirection
- Are there re-export shims (file A just re-exports from file B) left behind after refactors? Consumers should import directly.
- Are there pass-through wrappers that add no logic — functions/classes that only delegate to another with the same signature?
- Are there barrel exports (`index.ts`) still exporting symbols that were moved or deleted? Remove stale entries.
- Are there empty interfaces, abstract classes, or type aliases that exist only for "backwards compatibility" with no remaining consumers?

### Optimizations & simplification
- Is there overly complex code that could be reduced?
- Could any section be simplified without losing correctness?
- Are there opportunities to reuse existing code instead of duplicating?

### Test quality
- Do test inputs match the actual function signatures?
- Do assertions match the actual return types and shapes?
- Are mocks/stubs compatible with real implementations?
- Can the test scenario actually be constructed? Trace `.unwrap()` / `.expect()` in setup through production validation — will setup steps succeed?
- Does the asserted error/value have a producer in the current codebase?

### Checklist
- Read `review/CHECKLIST.md` and walk through every item against the diff.
- For each checklist category, note PASS / FAIL / N/A.
- List any failures with `file:line` references.

---

## Issue States

- OPEN - issue is not fixed yet
- DEFERED - issue is known about but we will fix later
- CLOSED - issue is fix now
- WILL_NOT_FIX - issue is an annoyance or over-engineering - it has been decided by user to never fix. There will often be documentation to help the REVIEWER know why

## Output Format

Review output is persisted under `<working-directory>/reviews/<repo>-pr-<number>/` (relative to where the reviewer agent is running, not the agents directory). The required index file is `review.md`.

The `review.md` index must start with the exact warning line `** WARNING do not delete review entries ever **`, then use exactly three top-level sections: `# META`, `# SUMMARY`, and `# DETAILS`. Line numbers start at 1. The `# SUMMARY` section must stay in `review.md` and must list every issue ID, including archived closed issues. Archived closed issues must include a grepable `archive:<ID>.md` marker in their `# SUMMARY` item. If no issues have ever been recorded for the review, set `open:none` and write `- none` under both `# SUMMARY` and `# DETAILS`.

Open issue details must stay inline under `# DETAILS`. If the review tracks more than 15 issue IDs, verified-closed issue details may be archived into sibling files named `<ID>.md` in the same review directory and linked from `# DETAILS`. Do not archive open issues, do not archive any issue while the review tracks 15 or fewer issue IDs, and do not duplicate the same issue detail both inline and in a file.

````md
** WARNING do not delete review entries ever **

# META
repo:<repo>
pr:<number>
branch:<branch>
base:<base-branch>
head:<head-sha>
reviewed:<yyyy-mm-dd>
open:<ID>,<ID> or open:none

# SUMMARY
- [ ] B1 BUG [HIGH] - One-line summary and some key `path/file.ts:10`
- [ ] SEC-1 SECURITY [HIGH] - One-line summary and some key `path/file.ts:20`
- [ ] I1 ISSUE [MEDIUM] - One-line summary and some key `path/file.ts:30`
- [ ] S1 SCOPING_AUTH [MEDIUM] - One-line summary and some key `path/file.ts:40`
- [ ] O1 OPTIMIZATION [LOW] - One-line summary and some key `path/file.ts:50`
- [ ] D1 DESIGN [MEDIUM] - One-line summary and some key `path/file.ts:55`
- [ ] T1 TEST [MEDIUM] - One-line summary and some key `path/file.ts:58`
- [ ] M1 MINOR [LOW] - One-line summary and some key `path/file.ts:60`

# DETAILS
## B1
ID:B1
type:BUG|SECURITY|ISSUE|SCOPING_AUTH|OPTIMIZATION|DESIGN|TEST|MINOR
severity:CRITICAL|HIGH|MEDIUM|LOW
summary:<one-line summary>
file:`path/to/file.ts:123`
pr:`#<number>` or `parent #<number> -> child #<number>`
status:OPEN

description:
<description>

evidence:
```evidence
<proof snippet or command output>
```

fix:<what needs to change>
reverify:<exact grep/read/test command or file:line to check>
````

When the review tracks more than 15 issue IDs, a verified-closed issue detail may be archived like this in `review.md`. The matching `# SUMMARY` item remains in `review.md` and includes `archive:B2.md`.

```md
# SUMMARY
- [x] B2 BUG [MEDIUM] - Closed issue summary and some key `path/file.ts:18` archive:B2.md

# DETAILS
- [B2](B2.md)
```

Example archived closed issue detail file at `<working-directory>/reviews/<repo>-pr-<number>/B2.md`:

The archive file must contain the full original issue detail record. Do not replace it with a metadata-only stub.

````md
## B2
ID:B2
type:BUG
severity:MEDIUM
summary:<one-line summary>
file:`path/to/file.ts:123`
pr:`#<number>` or `parent #<number> -> child #<number>`
status:CLOSED verified:<yyyy-mm-dd>
commit:`<short sha>` or `squash to <sha>`

description:
<original description>

evidence:
```evidence
<original proof snippet or command output>
```

fix:<original fix guidance>
reverify:<exact grep/read/test command or file:line to check>
fixed:<one-line description of the change>
````

## Issue Tracking

See `review/ISSUE_TRACKING.md` for how to open, close, archive, and re-verify issues across re-checks.

---

## Full Review

When asked for a "full review", run every stage and check group end-to-end with zero shortcuts. No skipping. No deferment. 100% checks.

### Requirements

1. **No skipping** — every check group runs in full, every checklist item is evaluated. No "N/A because it looks fine" — prove it's N/A with evidence.
2. **No deferment** — do not defer findings to follow-up PRs. Every finding is tracked in the current review.
3. **100% endpoint coverage** — enumerate every route handler / API endpoint touched or added by the PR. For each one, verify:
   - Authentication: is the caller authenticated?
   - Authorization: is project-level IAM enforced when projectId is present?
   - Input validation: are all parameters validated?
   - Error handling: are errors caught and surfaced correctly?
   Do not verify only the endpoints that were explicitly changed. Verify **all** endpoints in the affected controllers/modules — missing checks on unchanged endpoints are the most common gap.
4. **Systematic sweep** — after any security or IAM hardening round, grep for all route handlers (`@Get`, `@Post`, `@Delete`, `@Patch`, `@Put`, or framework equivalent) and verify each one against the access control pattern. Do not rely on the coder's commit message to tell you which endpoints were fixed — check them all.
5. **Cross-path consistency** — for every access control check added, verify:
   - The same check exists on all parallel paths that access the same data
   - Edge cases are covered (e.g., parameter A without parameter B, null vs empty string)
   - Error messages match the actual rejection reason
6. **No reactive-only verification** — do not just verify what the coder changed. Actively search for what they missed.

A full review that skips endpoints, defers findings, or only checks the happy path is not a full review. If you cannot complete a full review in one pass, split into parallel sub-agents by concern area (security, design, tests) but each sub-agent must complete its area fully.

### Evidence of completion

A full review must produce a **coverage evidence table** appended to the review output under `# FULL REVIEW EVIDENCE`. This table proves every file in scope was actually read and checked at the time of review. It is not a claim — it is a verifiable receipt.

For every file in the PR diff (from `git diff main...HEAD --name-only`), and record it in the table. The table must be written to `review.md` after `# DETAILS`.

Format:

```md
# FULL REVIEW EVIDENCE
head:<commit-sha>
date:<yyyy-mm-dd>

| File | commit | Auth | Input | Errors | Notes |
|---|---|---|---|---|---|
| apps/foo/controller.ts | a1b2c3d4... | ✅ | ✅ | ✅ | 3 routes checked |
| apps/foo/service.ts | e5f6a7b8... | N/A | ✅ | ✅ | no routes |
| libs/bar/client.ts | c9d0e1f2... | N/A | ✅ | ⚠️ B48 | json parse before ok |
```

Column definitions:

- **File** — path from repo root
- **commit** — commit hash. 
- **Auth** — authentication/authorization checks verified (✅ pass, ⚠️ finding, N/A no routes)
- **Input** — input validation verified
- **Errors** — error handling verified
- **Notes** — endpoint count, findings, or why N/A

Rules:

- Every file in the diff must appear in the table. No omissions.
- If a file was deleted in the PR, record as `deleted`.
- If a file is binary (images, etc.), record commit but mark checks as N/A.
- The `head:` line must match the `head:` in `# META`. If they differ, the evidence is stale.
- When re-running a full review after new commits, regenerate the entire table — do not carry forward old hashes.

### Review log

A persistent append-only log file `log.md` is kept alongside `review.md` in the review directory. It records what was checked at each commit. 
This file is **append-only** — never delete, overwrite, or rewrite entries. Each entry is a permanent record.

Append a new entry every time the reviewer checks the code (pull and check, full review, incremental re-check, or fix verification). Each file checked is one line:

```
<datetime> - <git-hash> - <bug>:<bug_status> - <path> - <summary of check>
```

Example `log.md`:

```md
2026-06-05-09:00:20 - df9fc5386 - B10:open - libs/domain/src/box/client.ts - refreshInFlight dedup verified, text-first json parse verified
2026-06-05-09:00:20 - df9fc5386 - B11:close - apps/acme-api/src/modules/resource/resource.service.ts - projectId ?? "" removed
2026-06-05 09:00:20 - df9fc5386 - B12:open - apps/acme-api/src/modules/resource/resource-credential.controller.ts - projectId ?? "" removed
```

Rules:

- **Append only** — never delete, edit, or reorder existing entries. New entries go at the bottom.
- Every pull-and-check cycle gets an entry, even if nothing changed (note "no new commits").
- One line per file checked. Only files actually read/verified in that pass, not all files in the diff.
- The log provides a complete audit trail. If a finding is missed, the log shows whether the file was checked and what was looked at.

---

## Rules

- Be concise and direct. Lead with facts, not praise.
- Every finding must include evidence: the actual code snippet or command output that proves the issue. Never open an issue without evidence.
- Use `file:line` references for every finding.
- Distinguish bugs (will break) from issues (might break) from minor (won't break).
- Never flag pre-existing issues in files not touched by the PR.
- Never flag style preferences unless they violate repo conventions.
- All check groups and the checklist pass are mandatory — do not skip any.
- Run format check alongside lint — they are separate CI steps.
- Verify data flow end-to-end: endpoint -> service -> data layer -> response.
- For any refactored data-fetching: verify the old filters, mappings, and return types are all preserved.
