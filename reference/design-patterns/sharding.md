# Sharding

Partition data across multiple storage nodes by a shard key to distribute load and storage.

**Applies to**: Distributed Systems and Microservice Architecture

---

**What it is**: Data is divided into shards based on a shard key (e.g. user ID range, hash). Each shard is stored on a separate node. Queries are routed to the shard holding the relevant data.

**When to use**:
- A single storage node cannot hold all data or handle all load.
- Data access patterns are well-understood and a suitable shard key can be chosen.
- Horizontal scaling of the data layer is required.

**Trade-offs**:
- Cross-shard queries are expensive or impossible.
- Re-sharding (changing the key or adding nodes) is operationally complex.
- The shard key must be chosen carefully to avoid hot spots.
