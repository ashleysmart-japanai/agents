# Service Object

Encapsulate a single business operation in a stateless object with one public method.

**Applies to**: Software Architecture

---

**What it is**: A plain object with a single `call` or `execute` method that performs one business use case. It coordinates domain objects and infrastructure but contains no state of its own between calls.

**When to use**:
- A use case spans multiple domain objects and does not belong on any one of them.
- Controllers or handlers are accumulating business logic.
- The same operation needs to be reusable across different entry points.

**Trade-offs**:
- Can become a dumping ground for logic that should live in domain objects (anemic domain model risk).
- Naming becomes critical — the service must represent one cohesive operation.
