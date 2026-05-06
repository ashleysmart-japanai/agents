# API Gateway

Single entry point for all clients that routes to backend services, handles auth, and aggregates responses.

**Applies to**: Distributed Systems and Microservice Architecture

---

**What it is**: A server that acts as the front door for all clients. It handles cross-cutting concerns (authentication, rate limiting, SSL termination, request routing, response aggregation) so individual services do not need to.

**When to use**:
- Multiple client types (web, mobile, third-party) need to access multiple backend services.
- Cross-cutting concerns should not be duplicated across services.
- You want to evolve the backend topology without changing client contracts.

**Trade-offs**:
- Single point of failure if not deployed with redundancy.
- Can become a bottleneck or a dumping ground for logic that belongs in services.
- Adds a network hop to every request.
