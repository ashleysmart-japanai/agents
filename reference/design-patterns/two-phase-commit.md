# Two-Phase Commit (2PC)

Coordinate an atomic commit across multiple participants using a prepare phase followed by a commit or abort.

**Applies to**: Distributed Systems and Microservice Architecture

---

**What it is**: A coordinator asks all participants to prepare (vote yes/no). If all vote yes, the coordinator sends commit to all. If any vote no, the coordinator sends abort to all. Guarantees atomicity across distributed participants.

**When to use**:
- Strict atomicity across multiple independent data stores is required.
- All participants support the 2PC protocol.

**Trade-offs**:
- Blocking protocol — if the coordinator fails after prepare, participants are locked until recovery.
- High latency — two round trips across all participants.
- Does not scale well with many participants.
- Prefer sagas or outbox for long-running or loosely coupled transactions.
