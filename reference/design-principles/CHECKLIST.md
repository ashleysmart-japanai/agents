# Design Principles Checklist

Use this as the short index for design reviews. Each item links to the full detail document.

- [ ] **DRY**: Keep each piece of knowledge in one authoritative place. [Details](dry.md)
- [ ] **KISS**: Prefer the simplest solution that meets the requirement. [Details](kiss.md)
- [ ] **YAGNI**: Do not build for hypothetical future use cases. [Details](yagni.md)
- [ ] **Separation of Concerns**: Split responsibilities so each concern changes independently. [Details](separation-of-concerns.md)
- [ ] **Composition over Inheritance**: Assemble behavior from components instead of deep class trees. [Details](composition-over-inheritance.md)
- [ ] **Toolkits vs Frameworks**: Choose control model intentionally around inversion of control. [Details](toolkits-vs-frameworks.md)
- [ ] **Law of Demeter**: Talk only to direct collaborators, not distant internals. [Details](law-of-demeter.md)
- [ ] **Principle of Least Astonishment**: Design behavior and naming to match user expectations. [Details](principle-of-least-astonishment.md)
- [ ] **Cohesion and Coupling**: Keep related logic together and dependencies minimal. [Details](cohesion-and-coupling.md)
- [ ] **Encapsulation**: Hide mutable internals behind stable public contracts. [Details](encapsulation.md)
- [ ] **Command Query Separation (CQS)**: Queries return data; commands change state, not both. [Details](command-query-separation.md)
- [ ] **Fail-Fast**: Detect invalid state early and stop with explicit errors. [Details](fail-fast.md)
- [ ] **Defensive Programming**: Validate boundaries and handle external failures explicitly. [Details](defensive-programming.md)
- [ ] **Domain-Driven Design (DDD)**: Model code around domain language, boundaries, and invariants. [Details](domain-driven-design.md)
- [ ] **SOLID**: Build extensible, testable components with clear contracts. [Details](solid.md)
- [ ] **Data Flow vs Class-Based Design**: Choose architecture intentionally based on workload and domain. [Details](data-flow-vs-class-based-design.md)
- [ ] **ACID Properties**: Understand transaction guarantees and isolation trade-offs. [Details](acid-properties.md)
- [ ] **Variable Semantic Classes**: Name variables by meaning and lifecycle, not just type. [Details](variable-semantic-classes.md)
