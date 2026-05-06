# Claim Check

Store a large message payload externally and pass only a reference (claim check) in the message.

**Applies to**: Enterprise Integration

---

**What it is**: When a message payload is too large for the messaging infrastructure, the sender stores it in a shared store (blob storage, database) and puts a reference token in the message. The receiver uses the token to retrieve the payload.

**When to use**:
- Messages exceed size limits of the broker.
- Large payloads would slow down the message bus for all consumers.
- The payload is only needed by some consumers.

**Trade-offs**:
- Adds a round-trip to retrieve the payload.
- The external store becomes a dependency; payload must be retained until all consumers have processed it.
