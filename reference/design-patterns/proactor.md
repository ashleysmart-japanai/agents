# Proactor

Handle asynchronous operations by invoking completion handlers when operations finish.

**Applies to**: Concurrent and Parallel Systems

---

**What it is**: Operations are initiated asynchronously. When an operation completes, the OS or runtime notifies the proactor, which dispatches a completion handler. Unlike Reactor, the operation itself is async — the handler only runs after completion.

**When to use**:
- The platform supports async I/O (Windows IOCP, Linux io_uring).
- High-throughput I/O where waiting for completion in a thread is too expensive.

**Trade-offs**:
- More complex programming model than synchronous or reactor-based code.
- Platform support for true async I/O varies.
