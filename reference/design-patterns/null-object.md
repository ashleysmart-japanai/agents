# Null Object

Provide a do-nothing implementation of an interface to eliminate null checks at call sites.

**Applies to**: Object-Oriented Design

---

**What it is**: Instead of returning null, return an object that implements the expected interface with do-nothing or default behaviour. Callers never need to check for null.

**When to use**:
- Null checks are scattered throughout the codebase for an optional collaborator.
- Default behaviour (do nothing, return empty) is a valid and meaningful case.

**Trade-offs**:
- Can hide bugs — a missing collaborator may need to be an error, not a silent no-op.
- The null object must faithfully implement the interface or callers may be surprised by silent behaviour.
