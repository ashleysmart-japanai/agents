# Idempotent Consumer

Ensure processing a message more than once has the same effect as processing it once.

**Applies to**: Distributed Systems and Microservice Architecture

---

**What it is**: Each message carries a unique identifier. The consumer checks whether it has already processed that ID before acting. Duplicate messages are detected and discarded safely.

**When to use**:
- The messaging system guarantees at-least-once delivery (most do).
- The operation being performed is not naturally idempotent (e.g. inserting a row, sending an email).

**Trade-offs**:
- Requires a store of processed IDs (database, cache) that must be maintained and pruned.
- The ID store itself must be checked atomically with the operation to avoid race conditions.
