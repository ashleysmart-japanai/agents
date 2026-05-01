# Postmortem Skill

Run this after completing any non-trivial task to measure agent performance,
catch failure modes, and feed learnings into `postmortem_reports/BEST_PRACTICES.md`.

---

## When to run

- After every task that produced code changes (feat, fix, refactor).
- After any failed attempt — a failed postmortem is often more valuable than a success one.
- Skip for docs-only or config-only changes unless the agent struggled.

---

## Step 1 — Collect metrics

Run these in parallel and record the results:

### Diff quality

```bash
git diff main...HEAD --stat
git diff main...HEAD --numstat
git diff main...HEAD -- '*.test.*' '*.spec.*' --stat   # test file changes
```

Record:
- Files changed (count)
- Lines added / removed
- Test lines added / removed
- Files changed outside the stated task scope (scope creep flag)

### Build & test gate

Detect language from changed files, then run per `tooling/TOOLING.md`:
- **Build** — does it compile / bundle without errors?
- **Tests** — full suite pass rate, any tests deleted or weakened?
- **Lint** — new violations introduced vs. baseline?
- **Typecheck** — new type errors introduced?

Record pass/fail and counts for each.

### Import & dependency check

- Verify every new import resolves to a real file or installed package.
- Check for new dependencies added — were they justified?
- Flag any removed dependencies that are still imported elsewhere.

### Security scan

- Check for hardcoded secrets, API keys, or credentials in the diff.
- Run project security scanner if available (e.g., `semgrep`, `npm audit`, `bandit`).
- Flag any new `eval()`, `dangerouslySetInnerHTML`, raw SQL, or shell injection vectors.

---

## Step 2 — Evaluate quality

Score each dimension on a 1-5 scale:

| Dimension | What to evaluate |
|---|---|
| **Correctness** | Does the code do what the task/spec asked for? All acceptance criteria met? |
| **Scope discipline** | Were changes limited to what was asked? Any unnecessary refactors, renames, or "improvements"? |
| **Test coverage** | Were new behaviours tested? Were edge cases covered? Any tests deleted? |
| **Code quality** | Does it follow project conventions (review/CHECKLIST.md, CONVENTIONS.md)? SOLID? Clean naming? |
| **Diff cleanliness** | Is the diff minimal and reviewable? Formatting-only changes in unrelated files? |
| **Error handling** | Are failure modes handled? Does it fail early? Clean error messages? |
| **Security** | Any new attack surface? Inputs validated at boundaries? |
| **Efficiency** | Unnecessary loops, repeated work, blocking calls? |

### Failure mode checklist

- [ ] Hallucinated imports or files that don't exist
- [ ] Broken build after changes
- [ ] Tests that pass but don't actually assert the new behaviour
- [ ] Scope creep — changes beyond what was asked
- [ ] Deleted or weakened existing tests
- [ ] Hardcoded values, magic numbers, or secrets
- [ ] Dead code or "TODO/WIP" blocks left behind
- [ ] Missing error handling on new code paths
- [ ] Stale comments or docs that no longer match the code

---

## Step 3 — Write the report

Create a report at:

```
postmortem_reports/<YYYYMMDD>_<short-task-slug>.md
```

Use this template:

```markdown
---
date: YYYY-MM-DD
task: <one-line description of the task>
outcome: <success | partial | failed>
---

# Postmortem: <task name>

## Task summary
<What was asked, what was delivered>

## Metrics

| Metric | Value |
|---|---|
| Files changed | N |
| Lines added | N |
| Lines removed | N |
| Test lines added | N |
| Build | pass/fail |
| Tests | N passed, N failed, N skipped |
| Lint errors introduced | N |
| Type errors introduced | N |
| Scope creep files | N (list if any) |

## Quality scores

| Dimension | Score (1-5) | Notes |
|---|---|---|
| Correctness | | |
| Scope discipline | | |
| Test coverage | | |
| Code quality | | |
| Diff cleanliness | | |
| Error handling | | |
| Security | | |
| Efficiency | | |

**Overall: N/5**

## Failure modes detected
<List any checked items from the failure mode checklist, or "None">

## What went well
<Bullet points>

## What went wrong
<Bullet points, or "Nothing notable">

## Lessons learned
<Actionable takeaways that should inform future work>

## Action items
- [ ] <Concrete follow-up tasks, if any>
```

---

## Step 4 — Update best practices

Read `postmortem_reports/BEST_PRACTICES.md` and update it:

1. If a lesson learned is new — add it under the appropriate category.
2. If a lesson reinforces an existing entry — increment its occurrence count.
3. If a previous best practice was contradicted — note the exception and context.
4. Keep the file sorted by occurrence count (most common lessons first within each category).

---

## Rules

- Be honest in scoring — inflated scores defeat the purpose.
- A "partial" outcome is not a failure. Record what worked and what didn't.
- Failed postmortems are blameless — the goal is learning, not punishment.
- Do not skip the postmortem because "everything worked fine." Success patterns are worth recording too.
- The report is append-only: never edit or delete a past report.
- BEST_PRACTICES.md is a living document: always update it, never let it go stale.
