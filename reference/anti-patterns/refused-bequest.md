# Refused Bequest

A subclass inherits methods from a parent but does not use them, overrides them to throw, or returns dummy values.

**Applies to**: Object-Oriented Design

---

**What it is**: A subclass inherits methods from a parent but does not use them, overrides them to throw, or returns dummy values.

**Why not**: The subclass is not a true subtype — it violates LSP. The inheritance relationship is a lie. Prefer composition or redesign the hierarchy.
