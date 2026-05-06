# Adapter

Wrap an incompatible interface so it matches the one a client expects.

**Applies to**: Object-Oriented Design

---

**What it is**: Converts the interface of a class into another interface that clients expect. Allows classes to work together that otherwise could not because of incompatible interfaces.

**When to use**:
- Integrating a third-party library or legacy component whose interface cannot be changed.
- You want to reuse existing classes without modifying them.

**Trade-offs**:
- Adds an indirection layer.
- If the adapted interface changes, the adapter must change too.
