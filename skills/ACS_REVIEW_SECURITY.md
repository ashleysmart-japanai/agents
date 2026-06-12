---
name: acs-review-security
description: Slash command /acs-review-security. Run a security review using the security review check groups. Loads the review method, security check groups, and issue tracking contract, then performs the review against the current PR branch.
---

# ACS Review — Security

Run a security-focused review covering auth, tenant isolation, credentials, OAuth, SSRF, injection, input validation, error exposure, and logging.

## Workflow

1. Load the review method and security review type:
   - Read `review/REVIEW_METHOD.md`
   - Read `review/SECURITY_REVIEW.md`
   - Read `review/ISSUE_TRACKING.md`

2. Follow the review method stages in order:
   - **Stage 0** — Read existing review state if a review file exists
   - **Stage 1** — Gather & Analyze (diff, log, trace callers, find parallel paths, check regressions)
   - **Stage 2** — Run Step 0 (trace security model end-to-end) then all security check groups from SECURITY_REVIEW

3. Record findings following the issue tracking contract in `review/ISSUE_TRACKING.md`.

4. Verify done criteria from `review/REVIEW_METHOD.md`.
