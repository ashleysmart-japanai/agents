# Event-Driven Architecture

Components communicate exclusively through events; producers and consumers are fully decoupled.

**Applies to**: Software Architecture

---

**What it is**: Components emit events when something notable happens. Other components subscribe to events they care about and react. No component calls another directly. The event bus or broker is the only shared infrastructure.

**When to use**:
- High decoupling between components is more important than simplicity.
- New consumers should be addable without changing producers.
- Audit trails, replay, and event sourcing are required.

**Trade-offs**:
- End-to-end flow is implicit — hard to understand and debug.
- Eventual consistency between components.
- Event schema evolution must be managed carefully.
