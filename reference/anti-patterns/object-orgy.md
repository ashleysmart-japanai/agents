# Object Orgy

Objects expose their internal state freely, allowing any caller to read and mutate it without restriction.

**Applies to**: Object-Oriented Design

---

**What it is**: Objects expose their internal state freely, allowing any caller to read and mutate it without restriction.

**Why not**: Encapsulation is broken. Invariants cannot be enforced. Changes to internal representation cascade across all callers. Violates the core promise of encapsulation.
