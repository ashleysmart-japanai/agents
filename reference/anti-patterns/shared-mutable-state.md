# Shared Mutable State

Multiple components reading and writing the same in-memory state without synchronisation.

**Applies to**: Concurrent and Parallel Systems

---

**What it is**: Multiple components reading and writing the same in-memory state without synchronisation.

**Why not**: Produces data races, lost updates, and non-deterministic behaviour. Either isolate state behind a single owner or use immutable values.
