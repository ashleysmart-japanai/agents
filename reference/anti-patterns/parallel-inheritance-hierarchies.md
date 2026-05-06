# Parallel Inheritance Hierarchies

Adding a subclass in one hierarchy always requires adding a corresponding subclass in another hierarchy.

**Applies to**: Object-Oriented Design

---

**What it is**: Adding a subclass in one hierarchy always requires adding a corresponding subclass in another hierarchy.

**Why not**: The two hierarchies are secretly one concept. Every extension doubles the work and the coupling. Collapse or compose the hierarchies.
