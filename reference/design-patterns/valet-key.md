# Valet Key

Grant a client a time-limited, scoped token to access a resource directly without routing through the service.

**Applies to**: Distributed Systems and Microservice Architecture

---

**What it is**: The service generates a token (a signed URL, a short-lived credential) that grants the client direct, scoped access to a resource (e.g. a blob store, a queue). The client uses the token directly, bypassing the service for the data transfer.

**When to use**:
- Large file uploads or downloads should not be proxied through the service.
- Offloading data transfer to a storage service reduces service load.
- Fine-grained, time-limited access control is needed.

**Trade-offs**:
- Token revocation is difficult — the token is valid until it expires.
- The client must handle the direct resource access, increasing client complexity.
