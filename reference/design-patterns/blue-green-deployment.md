# Blue-Green Deployment

Maintain two identical environments; switch all traffic between them for zero-downtime deployments and instant rollback.

**Applies to**: Distributed Systems and Microservice Architecture

---

**What it is**: Blue is the live environment; green is the idle environment. A new version is deployed to green. After validation, the load balancer switches all traffic from blue to green. Blue becomes the idle environment for the next deployment. Rollback is an instant traffic switch back to blue.

**When to use**:
- Zero-downtime deployments are required.
- Instant rollback capability is needed.

**Trade-offs**:
- Requires double the infrastructure at all times.
- Database schema changes that are not backward-compatible break both environments.
