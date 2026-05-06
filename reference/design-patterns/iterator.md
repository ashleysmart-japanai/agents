# Iterator

Provide sequential access to elements without exposing the underlying structure.

**Applies to**: Object-Oriented Design

---

**What it is**: Provides a way to access the elements of a collection sequentially without exposing its internal representation.

**When to use**:
- Access to a collection's contents without knowing its internal structure.
- Supporting multiple simultaneous traversals.
- Providing a uniform interface for traversing different collection types.

**Trade-offs**:
- Adds overhead for simple collections where direct access is fine.
- Stateful iterators can cause problems if the underlying collection is modified during traversal.
