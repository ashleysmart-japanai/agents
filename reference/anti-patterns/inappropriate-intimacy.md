# Inappropriate Intimacy

Two classes are too deeply coupled to each other's internal details — each reaches into the other's private parts.

**Applies to**: Object-Oriented Design

---

**What it is**: Two classes are too deeply coupled to each other's internal details — each reaches into the other's private parts.

**Why not**: Changes to either class break the other. Testing one requires understanding both. Extract a well-defined interface and enforce the boundary.
