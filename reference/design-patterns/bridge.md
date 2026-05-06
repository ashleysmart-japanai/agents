# Bridge

Decouple an abstraction from its implementation so both can vary independently.

**Applies to**: Object-Oriented Design

---

**What it is**: Splits a large class or set of related classes into two hierarchies — abstraction and implementation — that can be developed independently.

**When to use**:
- You want to avoid a permanent binding between abstraction and implementation.
- Both the abstraction and its implementation should be extensible via subclassing.
- Changes in the implementation should not impact the client.

**Trade-offs**:
- Increases complexity by introducing additional classes.
- The split can be unclear when the abstraction and implementation are tightly related.
