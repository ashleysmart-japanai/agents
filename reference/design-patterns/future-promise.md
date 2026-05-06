# Future / Promise

A proxy for a result not yet computed; the computation proceeds concurrently while the caller may continue or block when the result is needed.

**Applies to**: Concurrent and Parallel Systems

---

**What it is**: A future represents the eventual result of an asynchronous computation. The caller receives the future immediately and can retrieve the result later (blocking if not yet ready). A promise is the write side — the producer fulfils the promise, resolving the future.

**When to use**:
- A computation can proceed concurrently with the caller's work.
- Results of async operations need to be composed or awaited.

**Trade-offs**:
- Composing many futures can produce complex chains that are hard to reason about.
- Error propagation through future chains must be explicitly handled.
