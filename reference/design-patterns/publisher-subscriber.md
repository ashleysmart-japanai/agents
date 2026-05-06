# Publisher-Subscriber

Producers publish to topics; consumers subscribe independently; producers and consumers are fully decoupled.

**Applies to**: Distributed Systems and Microservice Architecture

---

**What it is**: Publishers send messages to a topic without knowledge of subscribers. Each subscriber receives its own copy of each message. Adding or removing subscribers requires no changes to publishers.

**When to use**:
- Multiple independent consumers need to react to the same event.
- Producers and consumers should be deployable independently.
- Broadcasting state changes across services.

**Trade-offs**:
- No delivery guarantee to a specific consumer unless the broker provides it.
- Message ordering across subscribers may differ.
- Consumers that fall behind can accumulate large message backlogs.
