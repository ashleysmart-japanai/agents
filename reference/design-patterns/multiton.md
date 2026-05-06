# Multiton

Like Singleton but keyed — one instance per named key, managed by the class itself.

**Applies to**: Object-Oriented Design

---

**What it is**: Extends the Singleton concept to a map of named instances. Each key maps to exactly one instance; the class manages the registry internally.

**When to use**:
- You need one instance per configuration variant, tenant, or named resource.

**Trade-offs**:
- Same testability and hidden-dependency problems as Singleton.
- The registry itself becomes global state. Prefer explicit injection where possible.
