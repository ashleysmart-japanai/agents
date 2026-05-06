## Separation of Concerns

A system is divided into distinct sections, each responsible for one concern. A concern is any piece of information or behaviour that affects the program — business logic, persistence, presentation, authentication, logging, and so on.

**Rules**:
- A module that handles HTTP routing does not contain SQL. A module that
contains SQL does not format output. Each layer knows only about the layer directly below it.
- Cross-cutting concerns (logging, auth, caching) are handled at the
boundary — via middleware, decorators, or interceptors — not woven through business logic.
- When a change to one concern (e.g. switching databases) forces changes
in another (e.g. formatting), the boundary is in the wrong place.

**Layers** (typical):
- **Presentation** — format and deliver output; knows nothing about storage.
- **Application / Use case** — orchestrates domain logic; knows nothing
about HTTP or SQL.
- **Domain** — core business rules and entities; has no external
dependencies.
- **Infrastructure** — databases, queues, external APIs; implements
interfaces defined by the domain.

**Relation to other principles**: SoC is the motivation behind SRP, DRY, and layered architecture. If two things change for different reasons, they are different concerns and should be separated.

---
