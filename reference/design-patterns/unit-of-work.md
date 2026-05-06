# Unit of Work

Track all changes made during a transaction and write them out as a single atomic operation.

**Applies to**: Software Architecture

---

**What it is**: Maintains a list of objects affected by a business transaction. Coordinates writing out changes and resolves concurrency problems. Commits all changes in one go or rolls them all back.

**When to use**:
- Multiple domain objects change within a single business operation that must be atomic.
- You want to batch database writes for efficiency.
- Tracking which objects are dirty, new, or deleted.

**Trade-offs**:
- Adds complexity — the unit of work must track all registered objects.
- Long units of work hold transactions open longer, increasing contention.
