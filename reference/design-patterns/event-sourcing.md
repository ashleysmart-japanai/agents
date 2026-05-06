# Event Sourcing

Store state as an append-only sequence of events; current state is derived by replaying them.

**Applies to**: Distributed Systems and Microservice Architecture

---

**What it is**: Instead of storing current state, every state change is stored as an event. Current state is derived by replaying events from the beginning (or from a snapshot). Events are immutable and the log is the source of truth.

**When to use**:
- A complete audit trail is required.
- Temporal queries (what was the state at time T?) are needed.
- Debugging complex state by replaying events is valuable.
- Combined with CQRS.

**Trade-offs**:
- Replaying a large event log is slow — snapshots are required.
- Schema evolution of events is difficult — old events must still be replayable.
- Conceptual complexity — current state is never stored directly.
