# Request-Reply

Send a message and receive a reply on a known reply channel, achieving synchronous semantics over async messaging.

**Applies to**: Enterprise Integration

---

**What it is**: The sender includes a reply-to address in the message. The receiver processes the request and sends its response to that address. The sender waits (blocking or async) for the reply.

**When to use**:
- The caller needs a result before proceeding.
- The underlying transport is async but the calling code expects a response.

**Trade-offs**:
- The sender blocks or holds state until the reply arrives — reintroduces coupling.
- Timeouts must be handled; a reply may never come.
