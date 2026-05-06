# CQRS

Separate read and write models; reads use a denormalised projection, writes go through a command handler.

**Applies to**: Distributed Systems and Microservice Architecture

---

**What it is**: Command Query Responsibility Segregation. The write side accepts commands that change state. The read side exposes queries against a read-optimised projection. The two sides may use different data stores.

**When to use**:
- Read and write workloads have very different performance and scaling requirements.
- The domain model is complex enough that a separate, simplified read model improves query performance significantly.
- Combined with Event Sourcing.

**Trade-offs**:
- Significant complexity — two models to maintain and keep in sync.
- Eventual consistency between write and read sides.
- Overkill for simple CRUD applications.
