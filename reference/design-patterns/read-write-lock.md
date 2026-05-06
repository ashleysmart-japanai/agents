# Read-Write Lock

Allow multiple concurrent readers or one exclusive writer; readers never block each other.

**Applies to**: Concurrent and Parallel Systems

---

**What it is**: A lock with two acquisition modes: shared (read) and exclusive (write). Any number of readers may hold the lock simultaneously. A writer must wait for all readers to release; readers must wait if a writer holds the lock.

**When to use**:
- Reads are frequent and writes are rare.
- Read operations are safe to run concurrently (no mutation).

**Trade-offs**:
- Writers can be starved if there is a continuous stream of readers.
- More complex than a simple mutex; implementation must handle promotion (read → write) carefully.
