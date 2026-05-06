# Design Reviewer

Use this checklist when designing, implementing, or reviewing code. For each item: state whether it applies, how it is satisfied, and why.

See [reference/design-principles/CHECKLIST.md](reference/design-principles/CHECKLIST.md) for the corresponding design checklists.

---

### DRY
- [ ] Is every piece of logic or knowledge expressed exactly once?
- [ ] Are there any copy-pasted blocks that should be extracted?
- [ ] Do multiple modules define the same constant or validation rule?
- [ ] If two things look the same — do they change for the same reason? (If not, do not merge them.)

### KISS
- [ ] Is this the simplest solution that satisfies the requirement?
- [ ] Is every abstraction layer earning its place?
- [ ] Can a new reader understand this in one sitting?
- [ ] Is there any cleverness that could be replaced with obviousness?

### YAGNI
- [ ] Is every class, method, and parameter required by a current acceptance criterion?
- [ ] Are there any extension points, hooks, or config options with no present consumer?
- [ ] Is any dead code present? If so, delete it.

### Separation of Concerns
- [ ] Does each module have a single, nameable concern?
- [ ] Are business rules free of HTTP, SQL, and framework types?
- [ ] Are cross-cutting concerns (logging, auth, caching) handled at the boundary, not woven through logic?
- [ ] Does changing the storage layer require touching the domain layer?

### Principle of Least Astonishment
- [ ] Does every function do exactly what its name says?
- [ ] Do any getters or queries mutate state?
- [ ] Are there boolean parameters that obscure intent at the call site?
- [ ] Are there implicit ordering requirements between functions?
- [ ] Is the naming consistent with the rest of the codebase?
- [ ] Would a code smell in the table below apply here?

### SOLID — SRP
- [ ] Does each class/module have exactly one reason to change?
- [ ] Can you name the single responsibility in one phrase?
- [ ] Would a change to persistence force a change to presentation logic (or vice versa)?

### SOLID — OCP
- [ ] Can new behaviour be added without editing existing classes?
- [ ] Are extension points defined as interfaces or strategy slots?

### SOLID — LSP
- [ ] Can every subtype be substituted for its base without changing observable behaviour?
- [ ] Does any subtype throw where the base does not, or return a narrower type?

### SOLID — ISP
- [ ] Does any implementor define methods it does not use?
- [ ] Can the interface be split into narrower ones that serve specific clients?

### SOLID — DIP
- [ ] Do high-level modules depend on abstractions, not concrete implementations?
- [ ] Are concrete types constructed at the composition root, not inside business logic?

### Law of Demeter
- [ ] Are there method chains of more than one dot deep on objects you do not own?
- [ ] Does any method navigate through an object's internals to reach what it needs?
- [ ] Can the immediate collaborator be asked to do the work instead?

### Cohesion and Coupling
- [ ] Do the elements inside each module share a purpose and operate on the same data?
- [ ] Does the module name contain "and", "util", or "manager"? (Signal to split.)
- [ ] Does a change to one module cascade into many others?
- [ ] Are there circular imports?

### Encapsulation
- [ ] Are fields private unless there is a concrete reason to expose them?
- [ ] Does any external code extract data from an object and act on it rather than asking the object to act?
- [ ] Are internal collections returned by reference, allowing external mutation?

### Command Query Separation
- [ ] Does every function either mutate state or return data — not both?
- [ ] Can every query be called multiple times safely with the same result?
- [ ] Is every command's side effect named and obvious?

### Composition over Inheritance
- [ ] Is inheritance used only for genuine is-a relationships with LSP honoured?
- [ ] Is the hierarchy shallow (two levels or fewer)?
- [ ] Could the shared behaviour be achieved by injecting a collaborator instead?

### Toolkits vs Frameworks
- [ ] Is the default choice a toolkit unless there is a concrete reason otherwise?
- [ ] Is domain logic free of framework base classes and framework types?
- [ ] Can the domain layer be tested without bootstrapping the framework?
- [ ] If fighting the framework, is replacing it with toolkits on the table?

### Fail-Fast
- [ ] Are inputs validated at the system boundary before being passed inward?
- [ ] Does any invalid state propagate silently rather than raising immediately?

### Defensive Programming
- [ ] Are all external inputs (API, user, file, network) treated as untrusted and validated?
- [ ] Are remote call failures, timeouts, and malformed responses handled explicitly?
- [ ] Are defensive checks concentrated at the boundary, not duplicated throughout internals?

### Domain-Driven Design
- [ ] Do class and method names use the domain's ubiquitous language?
- [ ] Do business rules live in the domain layer, not in controllers or repositories?
- [ ] Are aggregates accessed only through their root?
- [ ] Are cross-aggregate references by identity only, not direct object references?
- [ ] Does each bounded context own its own model?

### Data Flow vs Class-Based Design
- [ ] Has the choice between data flow and class-based design been made explicitly — not by default?
- [ ] If class-based: does the domain have distinct entities, identity, and value semantics that justify it?
- [ ] If data flow: is the system processing high-volume uniform data where throughput and cache efficiency are the constraint?
- [ ] In a mixed system: is the boundary between the two models explicit, with a defined interface between them?
- [ ] Is the object model being applied to a hot data path where it will cause cache misses or block vectorisation?
- [ ] Is data flow being applied to a rich domain where logic will become scattered and unownable?

---

- See [reference/design-patterns.md](reference/design-patterns.md) for the full design-pattern catalogue.
- See [reference/anti-patterns.md](reference/anti-patterns.md) for the full anti-pattern catalogue.
- See [reference/design-principles/CHECKLIST.md](reference/design-principles/CHECKLIST.md) for the design-principles checklist and detail links.
- See [reference/anti-patterns/CHECKLIST.md](reference/anti-patterns/CHECKLIST.md) for the anti-pattern checklist.
