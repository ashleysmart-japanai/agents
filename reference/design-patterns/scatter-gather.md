# Scatter-Gather

Broadcast a request to multiple recipients and aggregate their replies into a single response.

**Applies to**: Enterprise Integration

---

**What it is**: A message is sent to multiple recipients simultaneously (scatter). Each recipient processes the request independently. An aggregator collects all replies and combines them into a single response (gather).

**When to use**:
- The same request must be sent to multiple providers and results compared or merged (e.g. price comparison, parallel queries).
- Responses from multiple services must be combined before returning to the caller.

**Trade-offs**:
- The slowest responder determines the total latency unless a timeout cuts off late responses.
- Partial results must be handled if some recipients do not respond.
