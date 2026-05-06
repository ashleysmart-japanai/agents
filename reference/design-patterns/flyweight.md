# Flyweight

Share fine-grained objects to reduce memory when many instances share state.

**Applies to**: Object-Oriented Design

---

**What it is**: Uses sharing to support a large number of fine-grained objects efficiently. Separates intrinsic state (shared) from extrinsic state (passed in by the caller).

**When to use**:
- A large number of objects consume too much memory.
- Most object state can be made extrinsic (computed or passed in).
- Many groups of objects may be replaced by a small number of shared objects once extrinsic state is removed.

**Trade-offs**:
- Adds complexity in identifying and separating intrinsic vs extrinsic state.
- Extrinsic state must be managed by the caller, increasing caller complexity.
