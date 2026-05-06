# Anti-Corruption Layer

Translate between two different domain models at an integration boundary so neither corrupts the other.

**Applies to**: Software Architecture

---

**What it is**: A layer that isolates a system from external systems or legacy code by translating between their domain models. The internal domain model is never contaminated by external concepts.

**When to use**:
- Integrating with an external system or legacy codebase with a different domain model.
- You cannot change the external system's interface.
- The external model's concepts should not leak into your domain.

**Trade-offs**:
- Adds a translation layer that must be maintained as both models evolve.
- Can be expensive to build if the models are very different.
