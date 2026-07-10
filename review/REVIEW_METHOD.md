# Review Method

Evidence-based review methodology. Every finding must be provable from code, output, or trace.

This document is the methodology and the **finding grammar** — how to review, and how to express every finding in one unambiguous line. It is self-contained: you do not need any other file to list findings.

The persisted `review.md` store (the `~/reviews/<repo>-pr-<number>/` directory, its `# META`/`# SUMMARY`/`<ID>.md` files, and the rules for maintaining them) is a **separate concern**, specified in [ISSUE_TRACKING.md](ISSUE_TRACKING.md). Only the reviewer/orchestrator that owns a review directory reads that file.

## Finding Grammar

Every finding is expressed as one line. No prose adjectives — never say a finding is "present", "resolved", "done", or "handled". State is one of the tokens below, and only those tokens.

### Line format

```
- [<x| >] <ID> - <STATUS> [<SEVERITY>] - <title> `file:line`
```

- `[ ]` for a not-closed finding, `[x]` for a closed one.
- `<title>` is a short label with the location key(s) in backticks. Full detail is not needed to communicate the finding.

### Status tokens

- `OPEN` - must fix. No deferral. **A fix that is written but not yet verified is still `OPEN`** — do not upgrade to closed until verification evidence exists.
- `NEEDS_REVIEW:reviewer` - reviewer is uncertain about a finding and needs the user/human to decide.
- `NEEDS_REVIEW:coder` - coder is pushing back on a finding with evidence that the fix is problematic.
- `DEFERRED` - user has decided the issue is in scope but not needed now. Human-only — agents must never set this state.
- `CLOSED verified:<yyyy-mm-dd>` - the fix was applied **and verified** on that date (a passing reverify command, test, or trace). "Verified" is evidence-based; a fix merely present in the code is not verified.
- `WILL_NOT_FIX` - user has decided the issue is invalid, out of scope, or should be ignored. Human-only — agents must never set this state.

Not-closed = `OPEN`, `NEEDS_REVIEW:reviewer`, `NEEDS_REVIEW:coder`, `DEFERRED`. Closed = `CLOSED verified:<yyyy-mm-dd>`, `WILL_NOT_FIX`.

### Severity

`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`.

### ID prefixes

`B` BUG, `SEC` SECURITY, `I` ISSUE, `S` SCOPING_AUTH, `O` OPTIMIZATION, `D` DESIGN, `T` TEST, `M` MINOR. Sort by that prefix order, then by ID within each prefix.

### Example

```
- [x] S1 - CLOSED verified:2026-07-09 [HIGH] - scope resolved from row when expectedProviderName absent `resolver:71,100-103,127-128`
- [x] S2 - CLOSED verified:2026-07-09 [HIGH] - SHARED_ONLY denied in USER-scope branch before owner return `resolver:180-185`
- [ ] S3 - OPEN [HIGH] - assertUserScopeOwnership wired into update/reauthorize/delete; admin build unverified `base:342,355;credential-controller:256`
```

### Coder output

The coder **does not write to `review.md`** and does not touch the review directory. The coder lists findings to the user in chat as this flat checkbox list, using the grammar above. Persisting to the review store is the reviewer/orchestrator's job.

Never discard a potential finding. If in doubt, use `NEEDS_REVIEW:reviewer` instead of omitting it.

## Stage 0 — Read existing review state

Store step — for the reviewer/orchestrator persisting to a `review.md` directory. A coder reporting findings in chat skips Stage 0. The file mechanics referenced here (`review.md`, `# META`, `open:`, `<ID>.md`) are specified in [ISSUE_TRACKING.md](ISSUE_TRACKING.md).

Before making claims or editing the persisted review file:

1. Read the current review index at `~/reviews/<repo>-pr-<number>/review.md` if it exists.
2. If only a legacy `~/reviews/<repo>-pr-<number>-review.md` exists, read it and migrate it to the review directory without losing history.
3. Process feedback using the procedure in [ISSUE_TRACKING.md § Feedback ingress](ISSUE_TRACKING.md#feedback-ingress).
4. Read the `<ID>.md` detail files for not-closed issues listed in `open:`.
5. Summarize to yourself:
   - what the current issue IDs are
   - which issues are not-closed vs closed according to `open:` in `# META`, `# SUMMARY` checkboxes and status tokens, and `<ID>.md` statuses
   - which entries include cross-PR parent/child context in `pr:`

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

4. **CODER.md §4 compliance** — for every changed file, verify these are not violated:
   - **Enums for closed sets**: no raw strings where a const enum or union type exists. Grep for string literals passed to typed parameters.
   - **Booleans over string arrays**: fixed permission/flag sets use `{ key: boolean }` records, not `string[]`.
   - **Fail-closed defaults**: filters, permission checks, and gates deny on empty or absent input unless a documented legacy exception exists. Present-but-empty is always deny.
   - **No metadata in data namespaces**: system fields are under a reserved envelope key, not mixed into user data objects.
   - **No compat shims for internal code**: no re-exports, adapter wrappers, or renaming shims for internal callers. Internal interface changes update all callers directly.
   - **Cursor pagination**: all paginated endpoints use cursor-based pagination keyed on a record ID, not offset/page-number. Response shape is `{ items, nextCursor, hasMore }` — no `page`, `totalPages`, or `offset`.
   - **No `any`**: no new `any` types without a disable comment explaining why.

5. **Check for regressions** — compare old vs new for each changed function/endpoint:
   - What did the old function return? What shape/type?
   - What does the new function return? Same contract?
   - Did the old code have filters or guards? Are they preserved?
   - Are callers updated to match any signature changes?
   - If a validation or guard was weakened/removed, do all paths behind it still have equivalent protection?
   - Does the fix introduce a worse failure mode than the original bug on any path? (e.g., silent data corruption replacing a safe 400 error)

## Stage 2 — Check Groups

Run each check group against the diff. Every group produces a PASS / FAIL / N/A.

Load the applicable review type files from `review/*_REVIEW.md` for the check groups relevant to this review. At minimum, load `review/CODE_REVIEW.md` for code PRs.

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

Store step — applies when persisting to a `review.md` directory (see [ISSUE_TRACKING.md](ISSUE_TRACKING.md)). A coder reporting in chat presents the same coverage as a plain table in its message.

A full review must produce a **coverage evidence table** under `# FULL REVIEW EVIDENCE`. This table proves every file in scope was actually read and checked at the time of review. It is not a claim — it is a verifiable receipt.

For every file in the PR diff (from `git diff main...HEAD --name-only`), record it in the table. When persisting, the table is written to `review.md` after `# SUMMARY`.

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

---

## Rules

- Be concise and direct. Lead with facts, not praise.
- Every finding must include evidence: the actual code snippet or command output that proves the issue. Never open an issue without evidence.
- Use `file:line` references for every finding.
- Distinguish bugs (will break) from issues (might break) from minor (won't break).
- Never discard a potential finding. If you think something might not be important, log it as NEEDS_REVIEW with evidence — let the human decide. The agent does not get to silently drop findings.
- Never flag pre-existing issues in files not touched by the PR.
- Never flag style preferences unless they violate repo conventions.
- All check groups and the checklist pass are mandatory — do not skip any.
- Run format check alongside lint — they are separate CI steps.
- Verify data flow end-to-end: endpoint -> service -> data layer -> response.
- For any refactored data-fetching: verify the old filters, mappings, and return types are all preserved.
- The review document contract (output format, issue tracking) is separate from the review judgment. The codebase is the source of truth for findings, not this file.
- When persisting to a `review.md` store, follow [ISSUE_TRACKING.md](ISSUE_TRACKING.md) for all file mechanics (`<ID>.md` detail files, `# SUMMARY`, keeping titles and detail in sync). Those rules do not apply to in-chat finding reports.

## Acceptance Gate Verification

Before accepting a PR as review-complete, verify the acceptance gates from
CODER.md §5. Each gate requires an artifact — no artifact means the gate
was not run.

### Process gates (verify artifacts exist)

- [ ] **P1 Spec-with-matrix**: if the PR adds filters, permissions, gates, or
  fallbacks — the spec contains the input-state × behavior table with absent
  and present-but-empty as separate rows. No TBD cells. If absent, open as a
  finding.
- [ ] **P2 Executable ACs**: every acceptance criterion names a test. Check
  that the named tests exist and pass. Prose-only ACs are a finding.
- [ ] **P3 Anti-pattern catalog check**: the spec or PR description includes a
  pass/fail/N-A list against `anti-patterns/CHECKLIST.md`. If absent, run the
  check yourself and open findings for any hits.

### Code gates (verify in the diff)

- [ ] **C1 Fail-closed posture**: every gate in the diff has its posture
  documented. `grep` for filter/permission/guard logic and verify absent →
  deny (or documented compat), empty → deny.
- [ ] **C2 No raw strings for closed sets**: `grep` new fields for bare
  `string` types where a union/enum exists. Any hit is a finding.
- [ ] **C3 Invalid states unrepresentable**: flags use booleans not string
  arrays; domain values use named types not primitives.
- [ ] **C4 No metadata in data namespace**: system fields are under a reserved
  envelope key, not mixed into user data. Run smuggler checklist against diff.
- [ ] **C5 One owner per contract**: types crossing boundaries are declared
  once and imported, or carry `KEEP-IN-SYNC` references with a shape-pinning
  test.
- [ ] **C6 Only functional code**: every new symbol has a caller in the diff.
  No speculative fields, params, shims, or fallbacks without a current
  consumer named in the spec.
- [ ] **Cursor pagination**: any new paginated endpoint uses cursor-based
  pagination keyed on record ID, not offset/page-number.

### Truth gates (verify claims match code)

- [ ] **T1 No reviewer bait**: scan the diff for comments, docblocks, test
  names, and log messages that describe behavior the code does not implement.
  Each hit is a finding.
- [ ] **T2 Failures reported verbatim**: check that test output, skipped
  steps, and unverified paths are stated plainly — not editorialised.

### Submission gates (verify before marking review complete)

- [ ] **S1 Checklists executed with artifacts**: `REVIEW_METHOD.md` checklist
  was run (this file). `SECURITY_REVIEW.md` check groups ran if the diff
  touches APIs/auth/credentials. `anti-patterns/CHECKLIST.md` ran against the
  diff. Each has a filled item → pass/fail/N-A → `file:line` record.
- [ ] **S2 Findings classified before fixes**: every finding is tagged
  on-objective / robustness-layer / out-of-scope. Robustness layers default to
  rejected pending user decision.
- [ ] **S3 Fresh state**: review ran against current HEAD after `git fetch`.
  HEAD SHA is recorded.

## Done Criteria

A review is only complete when:

- the review conclusions came from your own code review of the actual codebase
- every finding is expressed in the finding grammar above, with `file:line` evidence
- no potential finding was silently dropped

### Store done criteria (when persisting to `review.md`)

When the review is persisted to a `review.md` directory, additionally verify — full mechanics in [ISSUE_TRACKING.md](ISSUE_TRACKING.md):

- the persisted review directory follows the output format and issue tracking contract in [ISSUE_TRACKING.md](ISSUE_TRACKING.md)
- the `open:` line in `# META` matches `# SUMMARY` checkboxes/status tokens and detail statuses
- any state changes are visible in the existing tracker and detailed entries
- no issue body was moved except for an allowed closed-issue archive or reopened-issue unarchive
- no freeform addendum was used where the existing review structure already covered the need
