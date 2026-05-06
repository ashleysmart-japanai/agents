# God Object

A single class or module that knows too much and does too much — accumulates state and logic that belongs elsewhere.

**Applies to**: Object-Oriented Design

---

**What it is**: A single class or module that knows too much and does too much — accumulates state and logic that belongs elsewhere.

**Why not**: Violates SRP. Every change touches the same file, causing merge conflicts and regression risk. Testing requires constructing the entire object even for small behaviours.
