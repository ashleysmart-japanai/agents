# Service Locator

A global registry used to look up dependencies at runtime rather than injecting them at construction.

**Applies to**: Software Design

---

**What it is**: A global registry used to look up dependencies at runtime rather than injecting them at construction.

**Why not**: Dependencies are hidden — the caller's requirements are not visible from its interface. Makes testing hard because the locator must be configured before each test. Violates DIP.
