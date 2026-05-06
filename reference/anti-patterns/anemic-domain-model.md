# Anemic Domain Model

Domain objects are pure data bags with no behaviour.

**Applies to**: Object-Oriented Design

---

**What it is**: Domain objects are pure data bags with no behaviour. All logic lives in service classes that operate on passive structs.

**Why not**: Breaks encapsulation. Invariants are not enforced at the object level, so invalid state can be constructed anywhere. The domain model communicates nothing about what operations are valid.
