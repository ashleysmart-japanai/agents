# Exception Swallowing

Catching an exception and doing nothing with it — silently ignoring a failure.

**Applies to**: Software Design

---

**What it is**: Catching an exception and doing nothing with it — silently ignoring a failure.

**Why not**: The error disappears. The system continues in an invalid or unexpected state. Failures become invisible and untraceable. At minimum, log and re-raise; at best, handle the error explicitly.
