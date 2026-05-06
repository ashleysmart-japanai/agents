# Layered Architecture

Organise code into horizontal layers with dependencies flowing downward only.

**Applies to**: Software Architecture

---

**What it is**: The system is divided into layers (presentation, application, domain, infrastructure). Each layer depends only on the layer below it. Upper layers orchestrate; lower layers implement.

**When to use**:
- A clear separation between UI, business logic, and data access is needed.
- The team is organised around functional layers.

**Trade-offs**:
- Strict layering can lead to unnecessary pass-through code.
- Changes that span layers (e.g. adding a field) touch many files.
- Can produce an anemic domain model if business logic accumulates in the application layer.
