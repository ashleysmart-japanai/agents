# Callback Hell

Deeply nested callbacks where each step is defined inside the handler of the previous step, forming a pyramid of indented code.

**Applies to**: Asynchronous Programming

---

**What it is**: Deeply nested callbacks where each step is defined inside the handler of the previous step, forming a pyramid of indented code.

**Why not**: Control flow is impossible to trace. Error handling is duplicated or omitted at every level. Refactor to promises, async/await, or explicit continuation objects.
