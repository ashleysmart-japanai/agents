# Abstract Factory

Create families of related objects without specifying their concrete classes.

**Applies to**: Object-Oriented Design

---

**What it is**: Provides an interface for creating a suite of related objects. All products from one factory are compatible with each other. Swap the factory to swap the entire product family.

**When to use**:
- A system must be independent of how its products are created.
- You need to enforce that products from one family are used together.
- You want to switch between product families at runtime or configuration time.

**Trade-offs**:
- Adding a new product type requires changing every factory interface and all implementations.
- Can become complex when the product family is large.
