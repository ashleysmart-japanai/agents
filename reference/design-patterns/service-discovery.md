# Service Discovery

Services register their network location; clients query a registry to find them rather than using hard-coded addresses.

**Applies to**: Distributed Systems and Microservice Architecture

---

**What it is**: Each service instance registers itself with a discovery registry on startup and deregisters on shutdown. Clients (or a load balancer) query the registry to find available instances. Two variants: client-side discovery (client queries registry and load-balances) and server-side discovery (load balancer queries registry).

**When to use**:
- Services run in dynamic environments where IP addresses and ports change (containers, auto-scaling).
- The number of service instances varies at runtime.

**Trade-offs**:
- The registry is a critical dependency — its failure affects the whole system.
- Stale registrations must be detected and removed (health checks, TTLs).
