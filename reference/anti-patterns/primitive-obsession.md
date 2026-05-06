# Primitive Obsession

Using raw primitives in place of small domain types (e.g.

**Applies to**: Object-Oriented Design

---

**What it is**: Using raw primitives in place of small domain types (e.g. `str` for an email address, `int` for a currency amount).

**Why not**: Validation and behaviour that belong to the concept are scattered at every use site. Two values of the same primitive type can be swapped silently. A domain type makes invalid states unrepresentable.
