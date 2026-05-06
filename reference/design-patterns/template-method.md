# Template Method

Define the skeleton of an algorithm in a base class; let subclasses fill in steps.

**Applies to**: Object-Oriented Design

---

**What it is**: Defines the structure of an algorithm in a base class, deferring some steps to subclasses. Subclasses can redefine certain steps without changing the algorithm's structure.

**When to use**:
- The invariant parts of an algorithm should be implemented once; variant parts left to subclasses.
- Common behaviour across subclasses should be factored into a shared class.

**Trade-offs**:
- Limits flexibility — subclasses are constrained to the structure defined by the base class.
- Can violate LSP if subclasses override steps in unexpected ways.
