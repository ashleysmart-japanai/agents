# Splitter

Split a composite message into individual messages for separate downstream processing.

**Applies to**: Enterprise Integration

---

**What it is**: A message containing multiple items (e.g. an order with many line items) is split into individual messages, one per item. Each is processed independently and can be routed to different channels.

**When to use**:
- Processing must happen at the item level, not the batch level.
- Downstream processors cannot handle composite messages.

**Trade-offs**:
- Results of split messages may need to be re-aggregated (use with Aggregator).
- Maintaining correlation between split messages and the original composite requires a correlation ID.
