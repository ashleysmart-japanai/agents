## Defensive Programming

Assume misuse and guard against it at system boundaries.

**Where to apply it**:
- Public APIs — validate every input before acting on it.
- User input — treat as untrusted; validate type, range, and format.
- File and network IO — handle missing files, timeouts, and malformed data
explicitly.
- Inter-service calls — assume the remote can fail, return unexpected data,
or be slow.

**Where not to apply it**:
- Inside a module's own private functions — once data has passed the
boundary and been validated, internal functions can trust it. Defensive checks on every internal call add noise without safety.

Fail-fast and defensive programming work together: defensive programming defines the boundary; fail-fast ensures violations are surfaced immediately rather than silently tolerated.

---
