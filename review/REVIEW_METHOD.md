# Review Method

Evidence-based review methodology. Every finding must be provable from code, output, or trace.

## Issue States

Canonical persisted status tokens and the `# SUMMARY` prefix grammar are defined in [ISSUE_TRACKING.md](ISSUE_TRACKING.md). Use that file when writing or updating review records.

High-level states:

- `OPEN` - coder must fix. No deferral — if the issue is OPEN, the coder fixes it.
- `NEEDS_REVIEW:reviewer` - reviewer is uncertain about a finding and needs the user/human to decide.
- `NEEDS_REVIEW:coder` - coder is pushing back on a finding with evidence that the fix is problematic.
- `DEFERRED` - user has decided the issue is in scope but not needed now. Human-only — agents must never set this state.
- `CLOSED verified:<yyyy-mm-dd>` - coder has fixed the problem and the fix was verified on that date.
- `WILL_NOT_FIX` - user has decided the issue is invalid, out of scope, or should be ignored. Human-only — agents must never set this state.

Never discard a potential finding. If in doubt, use `NEEDS_REVIEW:reviewer` instead of omitting it.

## Stage 0 — Read existing review state

Before making claims or editing the persisted review file:

1. Read the current review index at `~/reviews/<repo>-pr-<number>/review.md` if it exists.
2. If only a legacy `~/reviews/<repo>-pr-<number>-review.md` exists, read it and migrate it to the review directory without losing history.
3. Process feedback using the procedure in [ISSUE_TRACKING.md § Feedback ingress](ISSUE_TRACKING.md#feedback-ingress).
4. Read every archived closed issue detail file linked from the index `# DETAILS` section.
5. Summarize to yourself:
   - what the current issue IDs are
   - which issues are not-closed vs closed according to `open:` in `# META`, `# SUMMARY` checkboxes and status tokens, and detail record statuses
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

4. **Check for regressions** — compare old vs new for each changed function/endpoint:
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

A full review must produce a **coverage evidence table** appended to the review output under `# FULL REVIEW EVIDENCE`. This table proves every file in scope was actually read and checked at the time of review. It is not a claim — it is a verifiable receipt.

For every file in the PR diff (from `git diff main...HEAD --name-only`), record it in the table. The table must be written to `review.md` after `# DETAILS`.

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
- Do not invent ad hoc review sections if the existing review tracking format already has a place for the information.
- If the user says "find the list", inspect the actual review file structure first — the primary state list is the flat checkbox list under `# SUMMARY`.
- If you add a new issue ID, also add its detailed issue body inline under `# DETAILS`.
- If you change severity or wording in a summary list item, reflect the same change in the detailed issue entry.

## Done Criteria

A review update is only complete when all of the following are true:

- the review conclusions came from your own code review of the actual codebase
- the persisted review directory follows the output format and issue tracking contract in [ISSUE_TRACKING.md](ISSUE_TRACKING.md)
- the `open:` line in `# META` matches `# SUMMARY` checkboxes/status tokens and detail statuses
- any state changes are visible in the existing tracker and detailed entries
- no issue body was moved except for an allowed closed-issue archive or reopened-issue unarchive
- no freeform addendum was used where the existing review structure already covered the need
