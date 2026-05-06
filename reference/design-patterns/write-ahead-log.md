# Write-Ahead Log (WAL)

Write changes to a durable log before applying them to the data structure; enables crash recovery and replication.

**Applies to**: Distributed Systems and Microservice Architecture

---

**What it is**: Before any change is made to the database or data structure, the change is appended to an append-only log on durable storage. On crash, the system replays the log to recover to a consistent state. The log is also used for replication.

**When to use**:
- Durability and crash recovery are required.
- Changes must be replicated to other nodes.
- The log serves as the source of truth for Change Data Capture.

**Trade-offs**:
- Log must be compacted or truncated periodically to prevent unbounded growth.
- Replay time grows with log size — snapshots are needed to bound recovery time.
