# Wire Tap

Intercept messages on a channel for logging or monitoring without disrupting the primary flow.

**Applies to**: Enterprise Integration

---

**What it is**: Messages passing through a channel are also sent to a secondary channel (the wire tap) for inspection, logging, or auditing. The primary consumer is unaware of the interception.

**When to use**:
- Messages must be audited or logged without changing the processing pipeline.
- Debugging or monitoring a live message flow.

**Trade-offs**:
- The wire tap must not slow down the primary channel.
- The secondary channel must handle the full message volume.
