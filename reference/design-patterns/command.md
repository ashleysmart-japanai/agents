# Command

Encapsulate a request as an object; enables undo, queuing, and logging.

**Applies to**: Object-Oriented Design

---

**What it is**: Turns a request into a stand-alone object that contains the request and all its parameters. Commands can be stored, passed, queued, logged, and reversed.

**When to use**:
- Undo/redo support is required.
- Operations need to be queued, scheduled, or executed remotely.
- You want to log, audit, or replay operations.

**Trade-offs**:
- Increases the number of classes — one per distinct command type.
- Can be overkill for simple request dispatch.
