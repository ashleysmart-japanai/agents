# Service Layer

Define an application's boundary with a layer of services that establishes available operations and coordinates responses.

**Applies to**: Software Architecture

---

**What it is**: A layer of service classes sits between the presentation layer and the domain model. Each service method corresponds to a use case. Services coordinate domain objects, repositories, and infrastructure, but contain no domain logic themselves.

**When to use**:
- Multiple entry points (HTTP, CLI, messaging) must invoke the same use cases.
- Transactional boundaries should be managed at the use-case level.
- The domain model is rich and should not be exposed directly to the presentation layer.

**Trade-offs**:
- Can become an anemic pass-through layer if domain logic leaks into services.
- Adds a layer of indirection for simple CRUD operations.
