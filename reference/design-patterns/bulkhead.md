# Bulkhead

Isolate components into pools so a failure in one pool does not exhaust resources for others.

**Applies to**: Distributed Systems and Microservice Architecture

---

**What it is**: Partitions resources (thread pools, connection pools, processes) so that a failure or overload in one partition cannot consume resources needed by others. Named after the watertight compartments in a ship's hull.

**When to use**:
- Multiple consumers share a limited resource (a connection pool, a thread pool).
- A slow or failing downstream should not starve calls to other downstreams.
- Critical paths must be protected from degraded non-critical paths.

**Trade-offs**:
- Resources must be pre-partitioned — sizing each pool requires load knowledge.
- Under-utilisation in one pool cannot be lent to another without redesign.
