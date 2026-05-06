# Inbox

Store incoming messages in a local inbox table and process them exactly once, even if the same message is delivered multiple times.

**Applies to**: Distributed Systems and Microservice Architecture

---

**What it is**: The dual of the Outbox pattern. Incoming messages are written to a local inbox table as they arrive. A processor reads from the inbox and marks messages as processed. Duplicate deliveries are detected by checking the inbox before processing.

**When to use**:
- The messaging system delivers messages at least once and the operation is not naturally idempotent.
- Exactly-once processing semantics are required.

**Trade-offs**:
- The inbox table must be pruned to prevent unbounded growth.
- Checking and writing to the inbox must be atomic with message processing.
