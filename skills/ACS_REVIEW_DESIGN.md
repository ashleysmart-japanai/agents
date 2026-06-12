---
name: acs-review-design
description: Slash command /acs-review-design. Run a design review using the design review check groups. Loads the review method, design check groups, and issue tracking contract, then performs the review against the current PR branch.
---

# ACS Review — Design

Run a design-focused review covering DRY, KISS, YAGNI, SOLID, separation of concerns, cohesion, encapsulation, composition, fail-fast, defensive programming, and domain-driven design.

## Workflow

1. Load the review method and design review type:
   - Read `review/REVIEW_METHOD.md`
   - Read `review/DESIGN_REVIEW.md`
   - Read `review/ISSUE_TRACKING.md`

2. Follow the review method stages in order:
   - **Stage 0** — Read existing review state if a review file exists
   - **Stage 1** — Gather & Analyze (diff, log, trace callers, find parallel paths, check regressions)
   - **Stage 2** — Run all design check groups from DESIGN_REVIEW

3. Record findings following the issue tracking contract in `review/ISSUE_TRACKING.md`.

4. Verify done criteria from `review/REVIEW_METHOD.md`.
