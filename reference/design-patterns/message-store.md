# Message Store

Persist messages to a central store for auditing, replay, and debugging without disrupting the primary flow.

**Applies to**: Enterprise Integration

---

**What it is**: All messages passing through the system are written to a durable store. The store can be queried for audit trails, replayed to reconstruct state, or used for debugging failed flows.

**When to use**:
- A complete audit trail of all inter-service communication is required.
- Messages may need to be replayed for debugging or recovery.

**Trade-offs**:
- The store grows indefinitely — retention policies and archiving must be managed.
- Writing to the store adds latency unless done asynchronously.
