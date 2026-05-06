# Competing Consumers

Multiple consumer instances read from the same queue; each message processed by exactly one consumer.

**Applies to**: Distributed Systems and Microservice Architecture

---

**What it is**: Multiple consumers listen on a single queue. The broker delivers each message to exactly one consumer. Adding consumers scales throughput; removing consumers reduces it. Consumers are interchangeable.

**When to use**:
- Processing throughput must scale horizontally.
- Work items are independent and order does not matter globally.
- Consumers can be added or removed without coordination.

**Trade-offs**:
- Message ordering is not guaranteed across consumers.
- Consumers must be idempotent if at-least-once delivery is used.
