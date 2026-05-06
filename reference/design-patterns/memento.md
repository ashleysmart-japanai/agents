# Memento

Capture and restore an object's state without violating encapsulation.

**Applies to**: Object-Oriented Design

---

**What it is**: Captures an object's internal state in a memento object so it can be restored later, without exposing the object's internal structure to the outside.

**When to use**:
- Undo/redo support.
- Snapshots of an object's state that can be restored on failure.
- The state to save is complex but must remain private.

**Trade-offs**:
- Storing many mementos can consume significant memory.
- Caretakers must manage the lifecycle of mementos without knowing their contents.
