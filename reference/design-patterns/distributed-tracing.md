# Distributed Tracing

Attach a trace ID to a request and collect timing spans from every service it touches to reconstruct the full execution path.

**Applies to**: Distributed Systems and Microservice Architecture

---

**What it is**: A trace ID is generated at the entry point and propagated in headers across all service calls. Each service records a span (start time, duration, service name, operation) and reports it to a tracing backend. The backend assembles spans into a trace showing the complete request path and timing.

**When to use**:
- Latency problems must be diagnosed across service boundaries.
- Understanding which service in a chain caused a failure or slowdown.

**Trade-offs**:
- Instrumentation must be added to every service and every outbound call.
- High-cardinality tracing data is expensive to store and query at scale.
