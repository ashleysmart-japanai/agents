## Cohesion and Coupling

**High cohesion** — the elements inside a module belong together. They share a purpose, operate on the same data, and change for the same reason. A module with low cohesion is doing unrelated things and should be split.

**Low coupling** — modules depend on as little of each other as possible. A change inside one module should not force changes in others.

These two goals reinforce each other: when a module has high cohesion, its interface is naturally narrow, which reduces the surface other modules must couple to.

**Signals of low cohesion**: a module name that contains "and", "or", "util", or "manager"; methods that share no data with each other; a module that is edited for many unrelated reasons.

**Signals of high coupling**: a change to one module requires edits in many others; tests for module A require constructing module B and C; circular imports.

---
