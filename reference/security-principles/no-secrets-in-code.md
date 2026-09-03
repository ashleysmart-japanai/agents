## No Secrets in Code

Credentials, API keys, tokens, and private keys never appear in source, config committed to the repo, logs, or error messages. Secrets are injected at runtime from a secret store or environment.

**Rules**:
- No secret literal in source or committed config — inject from env or a secret manager at runtime.
- Never log a secret, a full credential, or a token; redact before logging.
- Secrets never appear in error messages, stack traces, or responses returned to callers.
- A leaked secret is rotated, not just deleted from the diff — history retains it.
- Scan the diff for hardcoded secrets before every commit.

**Why**:
- Anything committed is effectively public forever — repo history, forks, and backups all retain it.
- Logs and error surfaces are widely readable and long-lived; a secret there is a secret disclosed.

---
