# Routing Slip

Attach a list of processing steps to a message; each processor removes itself from the slip and forwards to the next.

**Applies to**: Enterprise Integration

---

**What it is**: A sequence of processing steps is encoded in the message itself as a routing slip. Each processor inspects the slip, performs its work, removes its entry, and forwards the message to the next step on the slip. The pipeline is data-driven, not hard-coded.

**When to use**:
- Different messages require different sequences of processing steps.
- The processing sequence is not known at design time.

**Trade-offs**:
- The message becomes larger as the slip grows.
- Debugging requires tracing the slip across all processors.
