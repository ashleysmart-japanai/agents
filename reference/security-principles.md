# Security Principles

Canonical index for security principles. These are **instructive** — how to build access control, data handling, and secrets right from the start. Consumed by `CODER.md` / `DESIGNER.md`.

The detective counterpart — how to *spot* violations of these in a diff — is `review/SECURITY_REVIEW.md`. Review docs reference these principles; they do not re-copy them.

| Principle | Summary |
|---|---|
| [Secure by Query](security-principles/secure-by-query.md) | Encode the access predicate in the query; only authorized rows return. Never fetch-and-filter. |
| [Fail-Closed](security-principles/fail-closed.md) | Filters and gates default to deny; absent and present-but-empty both mean deny. |
| [Least Privilege](security-principles/least-privilege.md) | Grant the minimum scope needed — narrowest role, tightest credential, shortest lifetime. |
| [Validate at the Boundary](security-principles/validate-at-boundary.md) | Validate and type all external input at the entry point; internal code trusts validated data. |
| [No Secrets in Code](security-principles/no-secrets-in-code.md) | Credentials never in source, config, logs, or errors — injected at runtime, rotated when leaked. |
| [Defense in Depth](security-principles/defense-in-depth.md) | Independent layers back each other up; a backup layer never weakens the primary gate. |
