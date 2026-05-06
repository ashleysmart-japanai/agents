# Correlation Identifier

Attach a unique ID to a request so that replies can be matched back to the original request.

**Applies to**: Enterprise Integration

---

**What it is**: The sender generates a unique correlation ID and attaches it to the message. The receiver includes the same ID in its reply. The original sender uses the ID to match the reply to the pending request.

**When to use**:
- Request-reply messaging over async channels where replies may arrive out of order.
- Tracing a request across multiple hops in a distributed system.

**Trade-offs**:
- The sender must maintain state (a map of correlation ID → pending request) until the reply arrives.
- IDs must be unique and carry enough information to route replies correctly.
