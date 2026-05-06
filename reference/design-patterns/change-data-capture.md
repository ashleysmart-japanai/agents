# Change Data Capture (CDC)

Capture row-level changes from a database and publish them as events to downstream consumers.

**Applies to**: Distributed Systems and Microservice Architecture

---

**What it is**: Rather than polling for changes or adding application-level event publishing, CDC reads the database's replication log (e.g. PostgreSQL WAL, MySQL binlog) and produces a stream of insert/update/delete events. Downstream systems consume this stream.

**When to use**:
- Events must be published for every database change without modifying application code.
- Keeping derived data stores (search indexes, caches, read models) in sync with the primary database.
- Replacing polling with event-driven integration.

**Trade-offs**:
- Tightly coupled to the database's internal log format.
- Schema changes in the database must be handled in the CDC pipeline.
