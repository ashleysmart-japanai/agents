## Validate at the Boundary

All external input is validated and normalized at the moment it enters the system — the API edge, the message consumer, the file parser. Internal code trusts already-validated data; it does not re-check or, worse, assume.

**Rules**:
- Validate shape, type, range, and allowed values at the entry point, before the data reaches business logic.
- Reject invalid input with a clear error at the boundary; do not carry it inward with a sentinel.
- Parse into typed domain values at the edge so internal code cannot receive a malformed primitive.
- Strip or reject reserved/system fields from user input at the boundary (see [no-metadata-in-data-namespaces](../anti-patterns/smuggler.md)).
- Treat every external source as untrusted: user requests, third-party APIs, queues, files, env.

**Why**:
- One validated choke point is auditable; validation scattered through business logic drifts and leaves gaps.
- Typed-at-the-edge data makes whole classes of injection and type-confusion bugs unrepresentable downstream.

---
