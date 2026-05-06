# Temporal Coupling

Functions or methods that must be called in a specific order, with no enforcement of that order by the type system or constructor.

**Applies to**: Software Design

---

**What it is**: Functions or methods that must be called in a specific order, with no enforcement of that order by the type system or constructor.

**Why not**: The constraint is invisible. Callers discover it only when something breaks at runtime. Objects should be fully usable after construction — no two-phase init.
