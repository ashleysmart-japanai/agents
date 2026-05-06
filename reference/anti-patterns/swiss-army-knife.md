# Swiss Army Knife

A class or interface that does many unrelated things — the opposite of SRP at the API surface level.

**Applies to**: Software Design

---

**What it is**: A class or interface that does many unrelated things — the opposite of SRP at the API surface level.

**Why not**: Callers must understand the entire surface to use any part of it. The interface cannot be implemented or mocked simply. Split into focused interfaces (ISP).
