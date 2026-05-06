## ACID Properties

Properties that guarantee validity of database transactions.

| Property | Guarantee |
|----------|-----------|
| **Atomicity** | A transaction either completes fully or has no effect — no partial writes |
| **Consistency** | A transaction moves the database from one valid state to another |
| **Isolation** | Concurrent transactions produce the same result as if run serially |
| **Durability** | A committed transaction survives system failure |

### Isolation Levels

Isolation levels trade consistency for concurrency. From weakest to strongest:

| Level | Dirty Read | Non-repeatable Read | Phantom Read |
|-------|-----------|---------------------|--------------|
| Read Uncommitted | ✅ possible | ✅ possible | ✅ possible |
| Read Committed | ❌ prevented | ✅ possible | ✅ possible |
| Repeatable Read | ❌ prevented | ❌ prevented | ✅ possible |
| Serializable | ❌ prevented | ❌ prevented | ❌ prevented |

### Read / Write Phenomena

**Dirty read** — a transaction reads data written by another transaction that has not yet committed. If the writer rolls back, the reader has seen data that never existed.

**Non-repeatable read** — a transaction reads the same row twice and gets different values because another transaction committed a change between the two reads.

**Phantom read** — a transaction re-runs a query and sees a different set of rows because another transaction inserted or deleted rows that match the query predicate.

**Read before commit** — a pattern that requires a value to be read in the same transaction before it can be safely overwritten, ensuring the write is based on current state and not a stale snapshot.

**Lost update** — two transactions read the same value, both compute an update, and the second write silently overwrites the first. Prevented by pessimistic locking or compare-and-swap.

**Write skew** — two transactions each read an overlapping data set, make decisions based on what they read, and write to non-overlapping rows — producing a result that neither transaction would have allowed had it seen the other's write.

---
