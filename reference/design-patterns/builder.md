# Builder

Construct a complex object step-by-step; separate construction from representation.

**Applies to**: Object-Oriented Design

---

**What it is**: Separates the construction of a complex object from its final representation. A director drives the steps; a builder implements each step. The same director can produce different representations by swapping builders.

**When to use**:
- An object requires many optional or ordered construction steps.
- The same construction process should produce different representations.
- Constructors with many parameters are hard to read at call sites.

**Trade-offs**:
- Increases the number of classes.
- The builder must be kept in sync with the object it builds.
