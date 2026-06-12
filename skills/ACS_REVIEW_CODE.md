---
name: acs-review-code
description: Slash command /acs-review-code. Run a code review using the code review check groups only. Loads the review method, code check groups, and issue tracking contract, then performs the review against the current PR branch.
---

# ACS Review — Code

Run a code-focused review covering code quality, bugs, performance, readability, security basics, shims, optimizations, test quality, and checklist.

## Workflow

1. Load the review method and code review type:
   - Read `review/REVIEW_METHOD.md`
   - Read `review/CODE_REVIEW.md`
   - Read `review/ISSUE_TRACKING.md`
   - Read `review/CHECKLIST.md`

2. Follow the review method stages in order:
   - **Stage 0** — Read existing review state if a review file exists
   - **Stage 1** — Gather & Analyze (diff, log, lint, format, typecheck, tests, trace callers, find parallel paths, check regressions)
   - **Stage 2** — Run all check groups from CODE_REVIEW

3. Record findings following the issue tracking contract in `review/ISSUE_TRACKING.md`.

4. Verify done criteria from `review/REVIEW_METHOD.md`.
