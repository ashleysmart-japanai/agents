# Factory Method

Delegate instantiation to a subclass or factory function; callers depend on the interface, not the concrete type.

**Applies to**: Object-Oriented Design

---

**What it is**: Defines an interface for creating an object but lets subclasses or registered factories decide which class to instantiate. The caller never uses `new` directly.

**When to use**:
- The exact type to create is determined at runtime.
- You want to decouple the caller from the concrete class it creates.
- Subclasses should be able to extend what gets created without changing the caller.

**Trade-offs**:
- Adds an indirection layer — trace the factory to understand what gets built.
- Can proliferate factory subclasses if not managed carefully.
