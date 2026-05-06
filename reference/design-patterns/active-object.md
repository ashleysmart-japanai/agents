# Active Object

Decouple method invocation from execution; calls are queued and executed asynchronously in the object's own thread.

**Applies to**: Concurrent and Parallel Systems

---

**What it is**: Each method call on an active object becomes a request object placed on a queue. The object's private thread picks up requests and executes them sequentially, returning results via futures.

**When to use**:
- An object should run in its own thread without exposing threading to its callers.
- Methods should return immediately while work happens asynchronously.

**Trade-offs**:
- Adds overhead of queuing and thread management for every call.
- Debugging async execution and ordering is harder than synchronous code.
