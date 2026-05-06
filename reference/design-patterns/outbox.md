# Outbox

Write events to a local outbox table in the same transaction as the domain write; a relay process forwards them to the broker.

**Applies to**: Distributed Systems and Microservice Architecture

---

**What it is**: Instead of publishing directly to a message broker (which can fail independently of the database write), events are written to an `outbox` table atomically with the domain change. A separate relay process reads the outbox and publishes to the broker, ensuring at-least-once delivery.

**When to use**:
- You need guaranteed event publication when a database write succeeds.
- Dual-write consistency between a database and a message broker is required.

**Trade-offs**:
- Requires the relay process to be reliable and monitored.
- Outbox table must be polled or tailed — adds latency vs. in-process publish.
- At-least-once delivery — consumers must be idempotent.
