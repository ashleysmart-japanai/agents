# State

Allow an object to alter its behaviour when its internal state changes.

**Applies to**: Object-Oriented Design

---

**What it is**: The object appears to change its class when its state changes. Each state is represented as a separate class; the object delegates behaviour to the current state object.

**When to use**:
- An object's behaviour depends on its state and must change at runtime.
- Operations contain large conditional statements based on the object's state.

**Trade-offs**:
- Increases the number of classes — one per state.
- State transitions must be managed carefully to avoid illegal states.
