# Pipe and Filter

Process data through a sequence of independent processing steps (filters) connected by channels (pipes).

**Applies to**: Software Architecture

---

**What it is**: Each filter reads input from a pipe, transforms it, and writes output to the next pipe. Filters are independent — they share no state and can be reordered, added, or removed without changing other filters. The pipeline is composed from filters at configuration time.

**When to use**:
- Data transformation can be broken into independent, reusable steps.
- The processing sequence may vary per deployment or configuration.
- Filters should be independently testable and composable.

**Trade-offs**:
- Passing data through many pipes adds serialisation and copying overhead.
- Debugging requires tracing data through every filter in the chain.
