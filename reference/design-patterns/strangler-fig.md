# Strangler Fig

Incrementally replace a legacy system by routing requests to new implementation; retire the old gradually.

**Applies to**: Software Architecture

---

**What it is**: New functionality is built alongside the old system. A facade or router intercepts calls and directs them to the new implementation as each piece is replaced. The legacy system is retired piece by piece.

**When to use**:
- A legacy system must be replaced without a risky big-bang rewrite.
- The system can be decomposed into independently replaceable pieces.
- Continuous delivery must be maintained during the migration.

**Trade-offs**:
- The facade adds complexity and must be maintained during the transition.
- Running two systems in parallel increases operational cost.
- Requires discipline to actually retire the old code rather than leaving it indefinitely.
