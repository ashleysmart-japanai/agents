# Middle Man

A class that does nothing but delegate every method call to another class, adding no logic of its own.

**Applies to**: Object-Oriented Design

---

**What it is**: A class that does nothing but delegate every method call to another class, adding no logic of its own.

**Why not**: Dead indirection. The caller should interact with the real object directly. If a boundary is needed, it must add something — access control, transformation, or abstraction — not just forwarding.
