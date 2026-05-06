## YAGNI — You Aren't Gonna Need It

Do not build something until it is required by a current, concrete requirement. Speculative features and abstractions add complexity today for a benefit that may never arrive.

**Rules**:
- If no acceptance criterion requires it, do not build it.
- Do not add extension points, plugin hooks, or configurability unless a
real consumer exists right now.
- Do not generalise from one use case. Wait for the second real use case
before extracting an abstraction — the right shape rarely reveals itself from one example.
- "We might need this later" is not a requirement.

**When to delete code**: Code that no longer serves a current requirement is a liability. Delete it. Version control is the safety net — the code is not lost, it is just not in the way.

Specifically, delete when:
- A feature is removed and its implementation is no longer on any code
path.
- A function or class has no callers.
- A configuration key is no longer read.
- An abstraction was built speculatively and no second use case arrived.
- Dead branches survive inside a function (`if False`, unreachable `else`).
- A migration or one-time script has run and will never run again.

Do not leave dead code with a comment explaining why it was kept. If there is a legitimate reason to resurrect it later, the git history and the PR description are the record — not a comment in the source.

---
