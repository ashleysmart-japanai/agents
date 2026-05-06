# Facade

Provide a simplified interface over a complex subsystem.

**Applies to**: Object-Oriented Design

---

**What it is**: Defines a higher-level interface that makes a subsystem easier to use. The facade does not prevent direct access to subsystem classes when needed.

**When to use**:
- A subsystem is complex and clients only need a subset of its capabilities.
- You want to layer a subsystem and provide an entry point for each layer.
- Reducing dependencies between clients and subsystem internals.

**Trade-offs**:
- Can become a god object if it accumulates too much logic.
- May hide complexity that some clients legitimately need to access.
