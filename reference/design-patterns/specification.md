# Specification

Encapsulate a business rule as a composable predicate object; combine with and/or/not.

**Applies to**: Object-Oriented Design

---

**What it is**: A business rule is expressed as an object with a single `is_satisfied_by(candidate)` method. Specifications can be combined using logical operators to build complex rules from simple ones.

**When to use**:
- Business rules need to be combined, reused, or tested independently.
- Filtering, validation, or selection logic is scattered across the codebase.
- Rules change independently of the objects they apply to.

**Trade-offs**:
- Can produce many small classes for simple rule sets.
- Complex combinations of specifications can be hard to read.
