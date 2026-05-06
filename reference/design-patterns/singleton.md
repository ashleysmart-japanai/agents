# Singleton

Ensure a class has exactly one instance; prefer dependency injection over global access.

**Applies to**: Object-Oriented Design

---

**What it is**: Restricts a class to one instance and provides a global access point to it. In practice, a single instance is almost always better achieved through dependency injection than through the Singleton class pattern.

**When to use**:
- Exactly one object is needed to coordinate across the system (e.g. a connection pool, a logger).
- Prefer injecting the single instance over making the class enforce its own uniqueness.

**Trade-offs**:
- Global access makes dependencies invisible and testing hard — state leaks between tests.
- Violates SRP (the class manages both its responsibility and its own lifecycle).
- Prefer dependency injection; treat Singleton as a last resort.
