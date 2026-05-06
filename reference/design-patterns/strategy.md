# Strategy

Define a family of algorithms, encapsulate each, and make them interchangeable.

**Applies to**: Object-Oriented Design

---

**What it is**: Defines a set of algorithms, encapsulates each one, and makes them interchangeable. The algorithm varies independently from the clients that use it.

**When to use**:
- Multiple variants of an algorithm are needed.
- A class defines many behaviours that appear as conditional statements — replace them with strategies.
- Clients should be unaware of the algorithm implementation details.

**Trade-offs**:
- Clients must be aware that strategies exist and choose between them.
- Adds classes for simple cases where a function parameter would suffice.
