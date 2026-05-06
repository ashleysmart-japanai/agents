# Ambassador

Proxy network calls from the main service through a helper that handles retries, circuit breaking, and observability.

**Applies to**: Distributed Systems and Microservice Architecture

---

**What it is**: A specialised sidecar that acts as an out-of-process proxy for all outbound network calls. The main service talks to localhost; the ambassador handles retries, circuit breaking, telemetry, and routing.

**When to use**:
- Network resilience logic (retry, circuit break, timeout) should be consistent and not duplicated in each service.
- The service team should not own network infrastructure concerns.

**Trade-offs**:
- Same operational complexity as the sidecar pattern.
- Configuration of the ambassador must be coordinated with service deployments.
