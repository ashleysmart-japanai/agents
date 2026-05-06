# Module

Group related functions, types, and state behind a single cohesive interface; hide internals.

**Applies to**: Object-Oriented Design

---

**What it is**: Organises code into a self-contained unit with a public surface and a private interior. The public surface is the only contract; internals can change freely.

**When to use**:
- Grouping related functionality that belongs together.
- Hiding implementation details that should not leak to callers.
- Providing a namespace to avoid naming collisions.

**Trade-offs**:
- Boundaries must be chosen carefully — too large and the module becomes a god object.
- Over-modularisation creates excessive indirection.
