## Composition over Inheritance

Prefer assembling behaviour from small, focused components rather than deriving it through class hierarchies.

**Why inheritance fails at scale**:
- A deep hierarchy couples a subclass to every ancestor's implementation.
A change in a base class ripples unpredictably downward.
- Inherited behaviour cannot be selectively replaced — you take all of it
or none of it.
- Multiple inheritance (or mixing in many base classes) creates ambiguity
and fragility.
- The hierarchy encodes assumptions about relationships that often stop
being true as requirements change.

**Composition**:
- An object holds references to collaborators and delegates to them.
- Behaviour is swapped at runtime or at construction by injecting a
different collaborator (Strategy pattern).
- Each collaborator is independently testable and reusable.
- The object's interface stays stable even when its internals change.

**When inheritance is appropriate**:
- A genuine is-a relationship exists and the subtype truly honours the
base contract (LSP).
- The hierarchy is shallow (one or two levels) and unlikely to deepen.
- Abstract base classes used purely to define an interface — no shared
mutable state, minimal shared logic.
