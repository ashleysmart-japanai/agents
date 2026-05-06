# Process Manager

Maintain state and coordinate a multi-step workflow across multiple channels and services.

**Applies to**: Enterprise Integration

---

**What it is**: A stateful component that tracks the progress of a long-running workflow. It receives events, determines the next step, and sends commands to the appropriate services. Unlike choreography, there is a single coordinator that knows the complete workflow.

**When to use**:
- A workflow spans many steps and services and the overall flow must be explicitly managed.
- Error handling and compensating actions require knowledge of the workflow state.

**Trade-offs**:
- The process manager becomes a centralised dependency.
- State must be persisted durably in case of failure.
