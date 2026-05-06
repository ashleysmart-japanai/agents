# Scheduler

Control the order in which threads access shared resources based on a defined policy.

**Applies to**: Concurrent and Parallel Systems

---

**What it is**: A scheduler mediates access to a resource among competing threads. It enforces an access policy (FIFO, priority, fair) without the resource or callers needing to implement the policy themselves.

**When to use**:
- Access to a resource must be ordered or prioritised.
- The scheduling policy needs to be independently configurable.

**Trade-offs**:
- The scheduler itself becomes a contention point.
- Complex policies can add latency or starvation for low-priority threads.
