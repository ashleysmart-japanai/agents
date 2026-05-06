# Composite

Treat individual objects and compositions uniformly through a shared interface.

**Applies to**: Object-Oriented Design

---

**What it is**: Composes objects into tree structures to represent part-whole hierarchies. Clients treat individual objects and compositions identically.

**When to use**:
- You need to represent tree structures (file systems, UI widgets, scene graphs).
- Clients should ignore the difference between individual and composite objects.

**Trade-offs**:
- Can make the design overly general — it may be hard to restrict what can be added to a composite.
- Leaf nodes may implement methods that make no sense for them.
