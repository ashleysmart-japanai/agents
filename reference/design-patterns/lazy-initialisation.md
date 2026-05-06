# Lazy Initialisation

Delay creation of an object or computation of a value until the first time it is needed.

**Applies to**: Object-Oriented Design

---

**What it is**: The object is not created in the constructor or at startup. The first access triggers creation; subsequent accesses reuse the cached result.

**When to use**:
- The object is expensive to create and may not always be needed.
- Startup time must be minimised.
- The creation has side effects that should not happen until the object is actually used.

**Trade-offs**:
- First access is slower — can be surprising in latency-sensitive paths.
- Thread safety must be handled explicitly in concurrent code.
