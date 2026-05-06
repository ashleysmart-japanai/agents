# Microservices

Decompose an application into small, independently deployable services, each owning its data and business capability.

**Applies to**: Software Architecture

---

**What it is**: Each service is a small, focused application with its own codebase, data store, and deployment pipeline. Services communicate over the network (HTTP, gRPC, messaging). Teams own services end-to-end.

**When to use**:
- Different parts of the system have different scaling, deployment, or technology requirements.
- Teams must be able to deploy independently without coordinating with other teams.
- The domain is large enough that a monolith creates bottlenecks.

**Trade-offs**:
- Significant operational complexity — service discovery, distributed tracing, inter-service auth.
- Distributed transactions and consistency are hard.
- Network latency replaces in-process calls.
- Not appropriate for small teams or early-stage products.
