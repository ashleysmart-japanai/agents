# Space-Based Architecture

Eliminate the database as a bottleneck by storing all shared state in an in-memory data grid distributed across processing units.

**Applies to**: Software Architecture

---

**What it is**: Processing units each hold a copy of all data in memory using a tuple space or distributed cache. Work is distributed across units via the space. There is no central database in the hot path — persistence happens asynchronously.

**When to use**:
- Extremely high write throughput that a relational database cannot sustain.
- Session-heavy applications (large numbers of concurrent users with session state).

**Trade-offs**:
- In-memory data is expensive and limits total data set size.
- Eventual consistency between the space and the persistent store.
- Complex failure and recovery scenarios.
