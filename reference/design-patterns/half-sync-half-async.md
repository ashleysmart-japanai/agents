# Half-Sync/Half-Async

Separate synchronous and asynchronous processing layers with a queue between them.

**Applies to**: Concurrent and Parallel Systems

---

**What it is**: The async layer handles I/O events and queues work items. The sync layer consists of worker threads that dequeue and process items synchronously. A queue decouples the two layers.

**When to use**:
- I/O handling must be non-blocking but processing logic is easier to write synchronously.
- Thread management should be separated from business logic.

**Trade-offs**:
- Queue becomes a point of contention and potential backlog.
- Matching throughput between the async and sync layers requires tuning.
