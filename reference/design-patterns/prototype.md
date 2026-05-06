# Prototype

Clone an existing object rather than constructing from scratch.

**Applies to**: Object-Oriented Design

---

**What it is**: Specifies the kinds of objects to create using a prototypical instance and creates new objects by copying that prototype.

**When to use**:
- Object creation is expensive and a similar object already exists.
- Classes to instantiate are specified at runtime.
- You need copies of objects with slight variations.

**Trade-offs**:
- Cloning objects with circular references is complex.
- Deep vs shallow copy semantics must be explicitly defined.
