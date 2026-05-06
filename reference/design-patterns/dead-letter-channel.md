# Dead Letter Channel

Move unprocessable messages to a holding channel for investigation rather than discarding them.

**Applies to**: Enterprise Integration

---

**What it is**: When a message cannot be processed (invalid format, repeated failure, expired), it is routed to a dead letter channel instead of being lost. Operations teams can inspect, correct, and replay dead letters.

**When to use**:
- Messages must not be silently dropped on processing failure.
- Failed messages need to be inspected and potentially replayed.

**Trade-offs**:
- Dead letter queues can grow unbounded if not monitored and drained.
- Re-processing dead letters requires tooling and careful handling to avoid reprocessing side effects.
