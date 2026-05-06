# Broker

Decouple clients from servers through an intermediary that locates servers, routes requests, and forwards results.

**Applies to**: Software Architecture

---

**What it is**: A broker component handles all communication between clients and servers. Clients send requests to the broker; the broker locates an appropriate server, forwards the request, and returns the result. Clients and servers have no direct knowledge of each other.

**When to use**:
- Clients must be decoupled from the location and identity of servers.
- Load balancing, service discovery, and protocol translation should be centralised.
- Common in middleware systems and service buses.

**Trade-offs**:
- The broker is a single point of failure and a performance bottleneck.
- Adds latency for every request.
