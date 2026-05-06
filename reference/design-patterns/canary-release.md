# Canary Release

Route a small percentage of traffic to a new version of a service; monitor before rolling out fully.

**Applies to**: Distributed Systems and Microservice Architecture

---

**What it is**: A new version is deployed alongside the current version. A small fraction of traffic (the canary) is routed to the new version. If metrics (error rate, latency, business KPIs) remain healthy, the rollout continues incrementally to 100%. If not, traffic shifts back.

**When to use**:
- Validating a new version in production with real traffic before full rollout.
- Reducing blast radius of a bad deployment.

**Trade-offs**:
- Both versions run simultaneously — they must be compatible (API, database schema).
- Requires traffic-splitting infrastructure and per-version monitoring.
