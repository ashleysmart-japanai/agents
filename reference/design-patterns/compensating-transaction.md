# Compensating Transaction

Undo a completed step in a distributed workflow by applying a semantically inverse operation.

**Applies to**: Distributed Systems and Microservice Architecture

---

**What it is**: Since distributed transactions cannot be rolled back atomically, each step in a saga must have a compensating transaction that reverses its effect. On failure, compensations are applied in reverse order for all completed steps.

**When to use**:
- Used within the Saga pattern when a step fails after previous steps have committed.
- Any workflow where partial completion must be undone.

**Trade-offs**:
- Compensations must be designed for every step — adds significant design work.
- Compensations may themselves fail — the system must handle compensation failures.
- The system is temporarily in an inconsistent state while compensations are applied.
