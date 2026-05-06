# Proxy

Control access to an object — for lazy init, access control, or caching.

**Applies to**: Object-Oriented Design

---

**What it is**: Provides a surrogate or placeholder for another object to control access to it. Common proxy types: virtual (lazy init), protection (access control), remote (network), caching.

**When to use**:
- Lazy initialisation of a heavyweight object.
- Access control — only authorised clients should reach the real subject.
- Caching results of expensive operations.
- Logging or auditing calls to the real subject.

**Trade-offs**:
- Adds an indirection layer that can slow response time.
- The proxy must stay in sync with the real subject's interface.
