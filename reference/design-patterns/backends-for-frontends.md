# Backends for Frontends (BFF)

Separate backend API surface per client type to serve each client's specific needs.

**Applies to**: Distributed Systems and Microservice Architecture

---

**What it is**: Instead of one general-purpose API gateway, each client type (web, mobile, third-party) gets its own backend. Each BFF is optimised for the needs and payload shapes of its specific client.

**When to use**:
- Different clients have substantially different data needs from the same backend services.
- Mobile clients need smaller payloads or different aggregations than web clients.
- Teams are aligned by client type and want independent deployment.

**Trade-offs**:
- Duplicates some logic across BFFs.
- More services to deploy, monitor, and maintain.
