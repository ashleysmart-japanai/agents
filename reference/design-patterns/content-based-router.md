# Content-Based Router

Route a message to a different channel based on its content.

**Applies to**: Enterprise Integration

---

**What it is**: A router inspects the content (headers, body fields) of each message and forwards it to the appropriate channel. The sender does not need to know which downstream will process the message.

**When to use**:
- Different message types or values require different processing paths.
- Routing logic should be centralised rather than embedded in the sender.

**Trade-offs**:
- The router must be updated when new message types or destinations are added.
- Routing logic in a central component can become complex and hard to test.
