# Circuit Breaker

Stop calling a failing service after a threshold; reset after a cool-down period.

**Applies to**: Distributed Systems and Microservice Architecture

---

**What it is**: Wraps a remote call with a state machine: closed (calls pass through), open (calls fail immediately), half-open (a probe call tests if the service has recovered). Prevents cascading failures.

**When to use**:
- Calling external services that may fail or become slow.
- You want to fail fast rather than exhaust threads waiting for a broken downstream.
- Self-healing behaviour after a downstream recovers.

**Trade-offs**:
- Threshold and timeout values must be tuned per dependency.
- Half-open state logic must be carefully designed to avoid flapping.
