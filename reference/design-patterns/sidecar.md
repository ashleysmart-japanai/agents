# Sidecar

Deploy a helper process alongside the main service to handle cross-cutting concerns.

**Applies to**: Distributed Systems and Microservice Architecture

---

**What it is**: A separate process or container is deployed alongside the main service. The sidecar handles concerns like logging, monitoring, proxying, config management, and service mesh integration — leaving the main service focused on its business logic.

**When to use**:
- Cross-cutting infrastructure concerns should not require changes to the service's code.
- The service is written in a language or framework that lacks a needed capability.
- Consistent observability or networking behaviour is needed across heterogeneous services.

**Trade-offs**:
- Adds operational complexity — each service deployment now has two processes.
- Sidecar failures can affect the main service.
- Latency added for any communication that routes through the sidecar.
