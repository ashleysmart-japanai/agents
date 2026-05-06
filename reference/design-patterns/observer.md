# Observer

Notify dependents automatically when an object's state changes.

**Applies to**: Object-Oriented Design

---

**What it is**: Defines a one-to-many dependency between objects so that when one object changes state, all its dependents are notified and updated automatically.

**When to use**:
- A change to one object requires changing others, and you do not know how many.
- An object should be able to notify others without making assumptions about who they are.
- Event-driven architectures.

**Trade-offs**:
- Observers may be notified in an unexpected order.
- Cascading updates between observers can produce cycles or unexpected side effects.
- Memory leaks if observers are not unregistered.
