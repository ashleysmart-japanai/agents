# Throttling

Limit the rate at which a consumer can use a resource; shed excess load gracefully.

**Applies to**: Distributed Systems and Microservice Architecture

---

**What it is**: Controls the rate of requests or operations allowed over a time window. Excess requests are queued, delayed, or rejected. Protects downstream services from being overwhelmed.

**When to use**:
- A downstream service or resource has a known capacity limit.
- Tenants or clients must be limited to fair usage.
- Protecting a service from spikes that exceed sustainable throughput.

**Trade-offs**:
- Rejected or delayed requests must be handled gracefully by callers.
- Rate limits must be tuned — too tight causes unnecessary rejections; too loose provides no protection.
