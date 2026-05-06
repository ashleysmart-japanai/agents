## Principle of Least Astonishment

Code should behave exactly as a knowledgeable reader would expect. If a reader has to stop and ask "why does it do that?", the design has failed.

**Rules**:
- Functions do what their name says, nothing more.
- A function named `get_` or `find_` returns data — it does not mutate state.
- A function named `save_`, `update_`, or `delete_` mutates state — it does
not silently return computed data as a side effect.
- Errors are surfaced, not swallowed. Silent failures are maximally
astonishing.
- Boolean parameters are avoided — `process(True)` tells the reader nothing.
Use named arguments or separate functions.
- Consistent conventions are more important than local cleverness. If the
codebase names things one way, follow it.

**Code smells** — signals that surprise is likely:

| Smell | Why it astonishes |
|-------|------------------|
| Long method | Reader cannot hold the whole thing in mind |
| Deep nesting | Control flow is hard to trace |
| Flag argument | A single function doing two different things |
| Inconsistent naming | Same concept named differently in different places |
| Surprise side effect | A getter that writes, a query that deletes |
| Implicit ordering | Functions that must be called in a specific order with no enforcement |
| Returned `None` as sentinel | Caller cannot distinguish "not found" from "error" |
| Boolean blindness | Raw `true`/`false` with no semantic label at the call site |

When a smell is found: rename, extract, or restructure until the code reads as the simplest possible expression of its intent.

---
