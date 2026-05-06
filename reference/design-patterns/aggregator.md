# Aggregator

Collect related messages and combine them into a single message once a completion condition is met.

**Applies to**: Enterprise Integration

---

**What it is**: Collects messages that belong to the same group (identified by a correlation ID), stores them until a completion condition is satisfied (all expected messages received, timeout, first N), then emits a combined message.

**When to use**:
- A downstream needs a complete picture assembled from multiple partial messages.
- Used as the counterpart to Splitter or Scatter-Gather.

**Trade-offs**:
- State must be maintained per group until completion — can be large.
- Completion conditions must handle missing or late messages (timeouts, partial completion).
