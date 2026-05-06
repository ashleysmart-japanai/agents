# Choreography

Services react to events with no central coordinator; each service knows what to do when it receives an event.

**Applies to**: Distributed Systems and Microservice Architecture

---

**What it is**: Each service subscribes to events and publishes its own events in response. There is no orchestrator — the workflow emerges from the interactions between services.

**When to use**:
- Loose coupling between services is the priority.
- The workflow is simple enough that tracing across events remains manageable.
- Services should be deployable and scalable independently.

**Trade-offs**:
- End-to-end workflow is implicit — hard to visualise and debug.
- Cyclic dependencies between event producers and consumers can emerge.
- Monitoring must aggregate across services to observe a complete flow.
