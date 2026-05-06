# Thread Pool

Maintain a pool of worker threads that pick up tasks from a queue, avoiding per-task thread creation overhead.

**Applies to**: Concurrent and Parallel Systems

---

**What it is**: A fixed or bounded set of threads is created at startup. Work items are submitted to a queue; idle threads dequeue and execute them. Thread creation cost is paid once; tasks are processed without spawning a new thread each time.

**When to use**:
- Tasks are short-lived and frequent, making per-task thread creation expensive.
- The number of concurrent threads must be bounded to prevent resource exhaustion.

**Trade-offs**:
- Pool size must be tuned — too few threads underutilises the CPU; too many causes context-switching overhead.
- Long-running tasks block threads and starve shorter tasks unless priority queuing is used.
