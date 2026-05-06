# Health Endpoint Monitoring

Expose a dedicated endpoint that reports service health; consumed by load balancers and orchestrators.

**Applies to**: Distributed Systems and Microservice Architecture

---

**What it is**: Each service exposes a `/health` or `/ready` endpoint. The endpoint checks the service's dependencies (database connectivity, downstream services) and returns a structured response. Load balancers and orchestrators use this to route traffic and restart unhealthy instances.

**When to use**:
- Services run in an orchestrated environment (Kubernetes, ECS) that performs health checks.
- Load balancers need to remove unhealthy instances from rotation.
- Monitoring systems need a standard way to check service availability.

**Trade-offs**:
- Health checks themselves consume resources and must be lightweight.
- A health check that is too strict may cause false restarts; too lenient masks real problems.
