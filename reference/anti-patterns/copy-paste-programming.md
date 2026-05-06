# Copy-Paste Programming

Duplicating code rather than abstracting a shared implementation.

**Applies to**: Software Design

---

**What it is**: Duplicating code rather than abstracting a shared implementation. The logic exists in many places, each slightly different.

**Why not**: When the logic must change, every copy must be found and updated. Miss one and the system is inconsistent. Violates DRY at the most basic level.
