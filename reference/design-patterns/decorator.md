# Decorator

Add behaviour to an object at runtime by wrapping it; preserves the interface.

**Applies to**: Object-Oriented Design

---

**What it is**: Attaches additional responsibilities to an object dynamically. Decorators provide a flexible alternative to subclassing for extending functionality.

**When to use**:
- Adding responsibilities to individual objects without affecting others.
- Extension by subclassing is impractical (class explosion).
- Behaviour can be composed from small, independent pieces.

**Trade-offs**:
- Many small objects that differ only in how they are connected can be confusing.
- Removing a specific decorator from the middle of a chain is awkward.
