---
name: diag
description: "Bug and incident diagnosis workflow. Use when investigating a failing test, local bug, or production alert. Creates a structured diagnostic record, gathers evidence from logs/errors/stack traces, and produces a diagnosis with action items."
---

# Diagnosis

Structured workflow for diagnosing bugs and incidents — whether a failing test on your machine, a bug report, or a production alert.

For cloud-specific log commands, see `tooling/TOOLING_GCP.md` / `tooling/TOOLING_AWS.md`.

---

## Scope — Read-Only Diagnosis

This skill is **strictly diagnostic**. It reads logs, reproduces errors, analyzes output, and writes a report.

**NEVER**:
- Apply a fix as part of diagnosis — document it in `## Action Items` instead
- Run commands that mutate production state
- Modify Terraform, Helm charts, or infrastructure

For **local bugs**, you may re-run tests or reproduce the error to gather evidence. For **production incidents**, stick to read-only commands (log queries, `git log`, `git blame`).

---

## When to Use

- A test is failing and the cause isn't obvious
- A bug report comes in and you need to find the root cause
- You receive a production alert (P0/P1/P2) from PagerDuty, Slack, or monitoring
- You want a persistent record of the diagnosis for handoff or postmortem

---

## Inputs

The user provides one of:

**Local bug / test failure:**
- Error message, stack trace, or test output
- Steps to reproduce (if known)
- What changed recently (branch, commit, PR)

**Production alert:**
- Severity: P0 (critical), P1 (error), P2 (warning)
- Service name
- Endpoint/description of what's failing
- Timestamp

---

## Session Management

When a new issue is handed to you:

1. **Focus on the new issue first.** Do not continue investigating prior issues.
2. **Compact the prior session.** If you were mid-diagnosis on something else, update that diag.md's Status field, then switch.
3. **Link back only after diagnosis.** Only after root-causing the new issue, check `<REPO_ROOT>/diag/` for related prior diagnoses. Never assume a link — confirm with evidence.

**Order of operations:**
1. Confirm the issue details (error, service/test, time/commit, severity)
2. Create the diag directory and diag.md
3. Gather evidence (logs, test output, reproduction)
4. Analyze the evidence
5. Write diagnosis
6. THEN check if it correlates with prior diagnoses

---

## Workflow

### Step 0: Check Prior Diagnoses

Scan `<REPO_ROOT>/diag/` for existing diagnosis directories. Check:
- Is this the same issue re-occurring? Update the existing diag.md.
- Is this a different symptom of an already-diagnosed root cause? Create a new directory but cross-reference.
- Is this a cascade? Link downstream to upstream root cause.

### Step 1: Create Diagnostic Directory

```
<REPO_ROOT>/diag/<YYYYMMDD>_<HHmmss>_<scope>_<short_label>/
```

- `scope` is the service name, test suite, or module (e.g., `api`, `auth_tests`, `frontend`)
- `short_label` is a snake_case summary (e.g., `login_500`, `db_timeout`, `null_pointer`)
- Keep the full directory name under 60 characters

**Labeling rules:**
- Use `scope` consistently so `ls <REPO_ROOT>/diag/ | grep api` finds all related issues
- For cascades, prefix with `cascade_` (e.g., `20260423_frontend_cascade_api`)
- For re-fires, don't create a new directory — append to the existing `diag.md`

### Step 2: Create diag.md

```markdown
# Diagnosis: <short description>

**Date**: YYYY-MM-DD
**Author**: <engineer name>
**Type**: local-bug | test-failure | production-alert
**Status**: investigating | root-caused | resolved | escalated

## Issue

<Paste the error message, alert, stack trace, or bug report verbatim.>

## Related Diagnoses

- `<prior_diag_dir>/` — <relationship>

## Summary

<One paragraph. Must be backed by evidence — no speculation.>

## Diagnosis

<Detailed root cause. Every claim must reference evidence.>

Format references as:
- **Log/output reference**: code-snip (`~/agents/style/CODE_SNIP.md`) — <what it shows>
- **Code reference**: quick-ref (`~/agents/style/QUICK_REF.md`) — <what it does>; code-snip (`~/agents/style/CODE_SNIP.md`) when the claim rests on the code
- **Diag reference**: `<diag_directory>/diag.md — <relationship>`
- **PR/commit reference**: `PR #<number> by <author> (merged <date>) — <what it changed>`

## Evidence

<The 1-3 pieces of evidence that pinpoint the root cause. Include raw output and explain what each proves.>

## Reproduction

<Steps to reproduce the issue, or the command that triggers the failing test.>

## Commands

<All commands used to gather evidence, with a one-line comment for each.>

## Action Items

- [ ] <immediate mitigation>
- [ ] <root cause fix>
- [ ] <follow-up items>
```

### Step 3: Gather Evidence

**For local bugs / test failures:**
1. Re-run the failing test or reproduce the error — capture full output
2. Check `git log` / `git diff` for recent changes to the affected code
3. Read the failing code path — trace from the error back to the root cause
4. Save relevant output to files in the diag directory

**For production alerts:**
1. Construct log query commands — see `tooling/TOOLING_GCP.md` or `tooling/TOOLING_AWS.md`
2. Time window: alert start minus 5 minutes to start plus 10 minutes, converted to UTC
3. Save log output to: `<diag_dir>/log_<scope>_<HH:MM-HH:MM>.txt`
4. If first query returns only access logs, broaden — see the cloud tooling doc for strategies

Record all commands in `## Commands`.

### Step 4: Analyze Evidence

1. **Parse each entry** — extract error messages, stack traces, input values, IDs
2. **Count and group** — how many of each error? Same input or different? Same code path?
3. **Identify the pattern**:
   - All same error = single root cause
   - Mixed errors = multiple issues or environmental
   - Single user/input = data-specific problem
   - All inputs = systemic issue
4. **Check for recent changes** — `git log`, `git show`, `git blame` on the affected code
5. **Cross-reference** — check `<REPO_ROOT>/diag/` for related issues

### Step 5: Write Diagnosis

Fill in `## Summary`, `## Diagnosis`, `## Evidence`, and `## Action Items`.

**No speculation.** Every statement must be backed by:
- A log entry or test output (cite file and line)
- A code location (cite file path and line)
- A git commit or PR (cite hash/number and author)
- A prior diagnosis (cite directory name)

If you cannot find evidence for a claim, say "unconfirmed" and explain what evidence would confirm it.

**Summary** — one paragraph a manager could read. Facts, not guesses.

**Diagnosis** — technical and specific:
- Name the exact error and cite the evidence
- Name the exact file/line/function and explain what it does
- Name the PR/commit that introduced the issue if identifiable
- For production: distinguish "the error" from "why it's a 5xx" (many alerts fire because a client error is incorrectly wrapped as a server error)

**Evidence** — the 1-3 most diagnostic pieces, not the noisy repetitions. Explain what each proves.

---

## Common Root Cause Patterns

| Pattern | Signature | Typical Cause |
|---------|-----------|---------------|
| Missing DB column | `column "X" does not exist` | Migration not applied |
| Missing config | `Config not found for X` | New resource without required config |
| Null bytes in Postgres | `\u0000 cannot be converted to text` | Binary file processed as text |
| 400 wrapped as 500 | `HTTP 400` inside `INTERNAL_SERVER_ERROR` | Client error incorrectly wrapped as server error |
| Record not found | `findUniqueOrThrow` / `RecordNotFound` | Async workflow failed or still running |
| Nil/null dereference | `nil pointer` / `Cannot read properties of undefined` | Missing null check on optional data |
| Import/dependency error | `ModuleNotFoundError` / `cannot find module` | Missing dependency or wrong version |
| Timeout | `context deadline exceeded` / `ETIMEDOUT` | Slow downstream or resource exhaustion |
| Race condition | Flaky test, intermittent failure | Shared mutable state without synchronization |
