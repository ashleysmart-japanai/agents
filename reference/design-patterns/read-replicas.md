# Read Replicas

Route read queries to replicas of the primary to offload read load and improve throughput.

**Applies to**: Distributed Systems and Microservice Architecture

---

**What it is**: The primary database handles all writes. One or more replicas receive a copy of all writes asynchronously and serve read queries. The application routes reads to replicas and writes to the primary.

**When to use**:
- Read traffic significantly exceeds write traffic.
- Reads can tolerate slight staleness (replication lag).
- Reporting or analytics queries should not impact the primary.

**Trade-offs**:
- Replication lag means reads may see stale data.
- Read-your-own-write consistency requires routing the read back to the primary or waiting for replication.
