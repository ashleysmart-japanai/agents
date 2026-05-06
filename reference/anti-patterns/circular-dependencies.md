# Circular Dependencies

Module A imports module B, which imports module A.

**Applies to**: Software Design

---

**What it is**: Module A imports module B, which imports module A. The dependency graph contains a cycle.

**Why not**: Neither module can be understood, tested, or replaced independently. Build systems struggle with cycles. Extract a shared abstraction that both depend on and break the cycle.
