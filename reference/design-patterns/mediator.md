# Mediator

Centralise communication between objects to reduce direct dependencies.

**Applies to**: Object-Oriented Design

---

**What it is**: Defines an object that encapsulates how a set of objects interact. Objects no longer refer to each other directly — they communicate through the mediator.

**When to use**:
- Many objects communicate in complex, well-defined ways creating tight coupling.
- Reusing an object is difficult because it refers to many others.
- Behaviour distributed across several classes should be customisable without subclassing.

**Trade-offs**:
- The mediator itself can become a god object if it accumulates too much coordination logic.
