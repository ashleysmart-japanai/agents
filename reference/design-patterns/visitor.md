# Visitor

Add operations to an object structure without modifying the classes of its elements.

**Applies to**: Object-Oriented Design

---

**What it is**: Represents an operation to be performed on the elements of an object structure. Visitor lets you define a new operation without changing the classes of the elements on which it operates.

**When to use**:
- Many distinct and unrelated operations need to be performed on an object structure.
- The object structure's classes change rarely, but new operations are added frequently.
- An operation needs to work across several different class hierarchies.

**Trade-offs**:
- Adding new element types requires updating every visitor.
- Breaks encapsulation — visitor must access the internal state of elements.
