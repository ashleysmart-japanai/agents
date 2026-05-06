# Retry with Backoff

Re-attempt a failed operation with increasing delays; cap total attempts.

**Applies to**: Distributed Systems and Microservice Architecture

---

**What it is**: On transient failure, wait and retry. The delay grows exponentially (or linearly) between attempts. A jitter component is added to avoid thundering-herd when many clients retry simultaneously.

**When to use**:
- Failures are expected to be transient (network blip, rate limit, momentary overload).
- The operation is idempotent — retrying produces the same result as a single call.

**Trade-offs**:
- Must not retry on non-transient errors (bad request, auth failure).
- Without a cap on attempts, a persistent failure becomes an infinite loop.
- Combine with circuit breaker to avoid retrying into a broken service.
