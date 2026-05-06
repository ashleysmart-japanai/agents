# Chain of Responsibility

Pass a request along a chain of handlers; each handler decides to process or forward.

**Applies to**: Object-Oriented Design

---

**What it is**: Decouples senders and receivers by giving multiple objects a chance to handle a request. The request travels along a chain until a handler processes it or the chain ends.

**When to use**:
- More than one object may handle a request, and the handler is not known a priori.
- You want to issue a request to one of several objects without specifying the receiver explicitly.
- The set of objects that can handle a request should be specified dynamically.

**Trade-offs**:
- No guarantee a request will be handled if the chain is not configured correctly.
- Can be hard to trace which handler processed a given request.
