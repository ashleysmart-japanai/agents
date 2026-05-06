# Design Principles

Canonical index for design principles used by `DESIGNER.md` and `DESIGN_REVIEWER.md`.

| Principle | Summary |
|---|---|
| [Checklist](design-principles/CHECKLIST.md) | Short review checklist that links to each detailed principle document. |
| [Data Flow vs Class-Based Design](design-principles/data-flow-vs-class-based-design.md) | Choose architecture intentionally based on workload shape and domain behavior. |
| [DRY — Don't Repeat Yourself](design-principles/dry.md) | Keep each piece of knowledge in one authoritative place. |
| [KISS — Keep It Simple](design-principles/kiss.md) | Prefer the simplest solution that satisfies the current requirement. |
| [YAGNI — You Aren't Gonna Need It](design-principles/yagni.md) | Do not implement speculative features before a concrete need exists. |
| [Separation of Concerns](design-principles/separation-of-concerns.md) | Split responsibilities so each concern can evolve independently. |
| [Composition over Inheritance](design-principles/composition-over-inheritance.md) | Build behavior from collaborators instead of deep class hierarchies. |
| [Toolkits vs Frameworks](design-principles/toolkits-vs-frameworks.md) | Choose inversion-of-control style deliberately for long-term flexibility. |
| [Law of Demeter](design-principles/law-of-demeter.md) | Limit interaction to direct collaborators to reduce structural coupling. |
| [Principle of Least Astonishment](design-principles/principle-of-least-astonishment.md) | Make naming and behavior match reader expectations. |
| [Cohesion and Coupling](design-principles/cohesion-and-coupling.md) | Keep related logic together and dependencies narrow. |
| [Encapsulation](design-principles/encapsulation.md) | Hide mutable internals behind stable, intention-revealing interfaces. |
| [Command Query Separation (CQS)](design-principles/command-query-separation.md) | Separate state-changing operations from read-only queries. |
| [Fail-Fast](design-principles/fail-fast.md) | Detect invalid state early and stop with explicit errors. |
| [Defensive Programming](design-principles/defensive-programming.md) | Validate external inputs and handle integration failures explicitly. |
| [Domain-Driven Design (DDD)](design-principles/domain-driven-design.md) | Organize code around domain language, boundaries, and invariants. |
| [SOLID Principles](design-principles/solid.md) | Use clear responsibilities and abstraction boundaries for maintainability. |
| [ACID Properties](design-principles/acid-properties.md) | Understand transactional guarantees and isolation trade-offs in persistence. |
| [Variable Semantic Classes](design-principles/variable-semantic-classes.md) | Name variables by semantic role and lifecycle rather than raw type alone. |
