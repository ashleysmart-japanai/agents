# Object Pool

Reuse a fixed set of expensive objects rather than creating and destroying them per use.

**Applies to**: Object-Oriented Design

---

**What it is**: Maintains a pool of initialised objects ready for use. Clients borrow an object from the pool, use it, and return it rather than allocating a new one each time.

**When to use**:
- Object creation is expensive (database connections, threads, sockets).
- Objects are needed frequently for short durations.
- The number of concurrently active objects is bounded.

**Trade-offs**:
- Returned objects must be reset to a clean state — stale state is a common bug.
- Pool size must be tuned; too small causes contention, too large wastes memory.
