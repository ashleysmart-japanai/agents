# Monitor Object

Synchronise concurrent method execution so only one method runs at a time within an object.

**Applies to**: Concurrent and Parallel Systems

---

**What it is**: An object's methods are wrapped with a mutex. Any thread calling a method acquires the lock first; others wait. Condition variables allow threads to wait for state changes within the monitor.

**When to use**:
- An object's state is shared across threads and must be consistent.
- Multiple threads call methods on the same object concurrently.

**Trade-offs**:
- Can become a bottleneck if lock contention is high.
- Deadlock is possible if monitors acquire each other's locks.
