---
name: acs-review
description: Slash command /acs-review. Run a full code review using all review types (code, security, design). Loads the review method, all check groups, and issue tracking contract, then performs the review against the current PR branch.
---

# ACS Review (All)

Run a complete review covering code, security, and design check groups.

## Workflow

1. Load the review method and all review types:
   - Read `review/REVIEW_METHOD.md`
   - Read `review/CODE_REVIEW.md`
   - Read `review/SECURITY_REVIEW.md`
   - Read `review/DESIGN_REVIEW.md`
   - Read `review/ISSUE_TRACKING.md`
   - Read `review/CHECKLIST.md`

2. Follow the review method stages in order:
   - **Stage 0** — Read existing review state if a review file exists
   - **Stage 1** — Gather & Analyze (diff, log, lint, format, typecheck, tests, trace callers, find parallel paths, check regressions)
   - **Stage 2** — Run all check groups from CODE_REVIEW, SECURITY_REVIEW, and DESIGN_REVIEW

3. Record findings following the issue tracking contract in `review/ISSUE_TRACKING.md`.

4. Verify done criteria from `review/REVIEW_METHOD.md`.
