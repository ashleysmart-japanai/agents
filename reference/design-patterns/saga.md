# Saga

Coordinate a long-running transaction across services using local transactions with compensating actions on failure.

**Applies to**: Distributed Systems and Microservice Architecture

---

**What it is**: A sequence of local transactions, each publishing an event or message that triggers the next step. On failure, compensating transactions undo completed steps. Two variants: orchestration (a central coordinator) and choreography (each service reacts to events).

**When to use**:
- A business transaction spans multiple services and cannot use a distributed lock.
- Each step must be committed locally and the overall transaction can take seconds or minutes.

**Trade-offs**:
- Compensating transactions must be designed for every step.
- Eventual consistency — the system may be temporarily inconsistent between steps.
- Debugging a failed saga across services is complex.
