# Hexagonal Architecture (Ports and Adapters)

Isolate the domain from all external concerns behind ports; adapters implement the ports for specific technologies.

**Applies to**: Software Architecture

---

**What it is**: The application core (domain + use cases) communicates with the outside world only through defined ports (interfaces). Adapters implement those ports for specific technologies (HTTP, SQL, message queues). The core has no dependency on any adapter.

**When to use**:
- The domain must be testable without any external infrastructure.
- Multiple delivery mechanisms (HTTP API, CLI, message queue) need to drive the same use cases.
- Infrastructure must be replaceable without touching the domain.

**Trade-offs**:
- More upfront structure to define ports and adapters explicitly.
- Can feel heavy for simple CRUD applications.
