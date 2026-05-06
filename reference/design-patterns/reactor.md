# Reactor

Handle service requests dispatched concurrently by demultiplexing events and dispatching to registered handlers.

**Applies to**: Concurrent and Parallel Systems

---

**What it is**: An event loop waits for events on a set of handles (sockets, file descriptors). When an event arrives, the reactor dispatches it to the registered handler. All handlers run in the same thread — no concurrency within handlers.

**When to use**:
- A server handles many concurrent connections with relatively cheap per-request processing.
- Single-threaded event-driven architectures (Node.js style).

**Trade-offs**:
- Long-running handlers block the event loop and starve other connections.
- Does not exploit multi-core hardware without additional design (multiple reactors, worker threads).
