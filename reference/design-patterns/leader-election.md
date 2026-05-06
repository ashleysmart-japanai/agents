# Leader Election

Designate one node as coordinator for a task; remaining nodes stand by and take over on failure.

**Applies to**: Distributed Systems and Microservice Architecture

---

**What it is**: Among a set of competing nodes, exactly one is elected leader at any time. The leader performs a coordinating task (scheduled job, cache invalidation, lock management). On leader failure, a new election is held.

**When to use**:
- A task must be performed by exactly one node at a time.
- Distributed consensus on who is in charge is needed.

**Trade-offs**:
- Split-brain scenarios (two nodes believe they are leader) must be prevented by the consensus algorithm.
- Election adds latency after a leader failure.
- Complexity of consensus protocols (Raft, Paxos, ZooKeeper) is significant.
