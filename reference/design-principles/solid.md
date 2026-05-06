## SOLID Principles

| Abbr | Full name | One-line rule |
|------|-----------|---------------|
| **SRP** | Single Responsibility | One reason to change per module, class, or function |
| **OCP** | Open / Closed | Open for extension, closed for modification |
| **LSP** | Liskov Substitution | Subtypes must be drop-in replacements for their base type |
| **ISP** | Interface Segregation | Many narrow interfaces over one wide one |
| **DIP** | Dependency Inversion | Depend on abstractions, not concretions |

### SRP — Single Responsibility

A module has exactly one reason to change. When a unit does two things — parsing *and* persisting, validating *and* formatting — split it. The name of each unit must make its single responsibility obvious without reading the body.

### OCP — Open / Closed

New behaviour is added by extending, not by editing existing code. Achieve this through composition, strategy objects, and well-defined extension points. A change request that requires editing an existing class body is a signal the abstraction boundary is in the wrong place.

### LSP — Liskov Substitution

Every subtype must honour the full contract of its base type. A caller holding a reference to the base type must observe identical behaviour regardless of which concrete subtype it receives. Violations: a subtype that throws where the parent does not, returns a narrower type, or silently ignores a method.

### ISP — Interface Segregation

No implementor should be forced to define methods it does not use. Split wide interfaces into focused ones. Clients depend only on the slice of the interface they actually call.

### DIP — Dependency Inversion

High-level policy modules do not import low-level detail modules. Both depend on a shared abstraction. Concrete implementations are injected at the composition root — never constructed inside business logic.

---
