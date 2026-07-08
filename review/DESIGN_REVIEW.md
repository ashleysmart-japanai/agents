# Design Review Check Groups

> **Method**: Follow the review methodology in [REVIEW_METHOD.md](REVIEW_METHOD.md) before running these check groups.

Use this checklist when designing, implementing, or reviewing code. For each item: state whether it applies, how it is satisfied, and why.

See [reference/design-principles/CHECKLIST.md](../reference/design-principles/CHECKLIST.md) for the corresponding design checklists.

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
- [ ] Are any parameters derivable from other parameters? If A implies B, requiring both is overspecification — it creates false invariants, splits validation across call sites, and masks bugs when the values disagree.

### Separation of Concerns
- [ ] Does each module have a single, nameable concern?
- [ ] Are business rules free of HTTP, SQL, and framework types?
- [ ] Are cross-cutting concerns (logging, auth, caching) handled at the boundary, not woven through logic?
- [ ] Does changing the storage layer require touching the domain layer?
- [ ] Are data and metadata carried separately? Metadata/control fields must not be smuggled into user rows or DTOs via reserved prefixes; use an explicit envelope such as `{ data, meta }`.
- [ ] Are HTTP-layer error types (e.g., NestJS `HttpException`, Express `HttpError`) confined to controllers and error filters — never thrown inside service/domain/data layers? Throwing HTTP exceptions deep in the stack causes: (1) framework class dependencies in business logic, (2) broken `$transaction` / unit-of-work patterns when bundlers (webpack) destroy the class hierarchy, (3) premature formatting of errors before the system is ready to produce an HTTP response. Services should throw plain domain errors (e.g., `OntologyValidationError` with an error code); the controller or error filter maps them to HTTP status codes at the boundary.

### MVC / Layer Discipline
- [ ] Are views/templates free of business logic? Conditionals like `if (status == "approved")` or `if (type == "abc")` in UI components are controller/service logic that leaked into the view — extract to a computed property, helper, or the model layer.
- [ ] Are controllers thin? Controllers should map requests to service calls and service results to responses. Branching on domain values, computing derived state, or orchestrating multi-step workflows belongs in the service/domain layer.
- [ ] Is formatting and display logic confined to the view layer? The model and controller should not produce HTML, CSS classes, or user-facing strings — the view maps model state to presentation.
- [ ] Are data transformations (filtering, sorting, aggregation) in the service/model layer, not repeated across multiple views or controllers?
- [ ] Do views bind to model properties or computed values, not raw API response shapes? If the view destructures an API payload directly, a backend change breaks the UI with no compile-time or type-level safety net.
- [ ] Does the API drive view configuration through capabilities (flags, schemas, feature toggles) rather than the view inspecting domain values? The view should ask "can the user do X?" via a capability flag, not `if (role == "admin")` or `if (type == "premium")`. The controller/API declares what is enabled; the view renders accordingly. This keeps domain knowledge server-side, makes the UI data-driven, and avoids scattering magic strings across components.

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
- [ ] Does any implementor widen a parameter type beyond what the interface declares (e.g., `context: InterfaceType & { extraField }`)? This is a star-alias antipattern — the extra field should be on the interface or a separate parameter, not smuggled through an intersection type.

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
- [ ] Does any in-process state (Map, cache, singleton) need to survive across multiple instances? Cloud Run, ECS, and k8s scale horizontally — in-memory state is per-instance. Multi-step flows (OAuth authorize→callback, upload→process) must use shared storage (cookie, Redis, DB) or be stateless.
- [ ] If a flow spans two HTTP requests (redirect, callback, webhook), will both requests hit the same process? If not, any state from request 1 must be externalized before the response.

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

### Scalability

#### Query-level scoping (prefer check-in-the-query over fetch-then-check)

When code must enforce access rules (ownership, visibility, tenancy), encode
the full access predicate in the database query so that only authorized rows
are returned. Do not fetch a superset and filter in application code.

**Fetch-then-check** (avoid):
```
row = db.findFirst({ id, orgId })   // coarse filter — may return unauthorized rows
if !canAccess(row, caller) → deny   // real decision in app code, after data is in memory
```

**Check-in-the-query** (prefer):
```
row = db.findFirst({ id, orgId, ...accessPredicates })  // query IS the gate
// if a row comes back, it is authorized by construction
```

- [ ] Are access rules (ownership, visibility, placement) encoded in the query WHERE clause, not applied as post-fetch filters?
- [ ] Does the query return only rows the caller is authorized to see — or does it fetch a superset and discard in application code?
- [ ] For list/search endpoints: are visibility filters (user-private vs shared vs org-wide) part of the query, not a post-query `.filter()`?
- [ ] If a post-fetch gate exists as a defense-in-depth layer, is the query still the primary authority? (A post-fetch check is acceptable as a second layer, not as the only layer.)
- [ ] Does the query-level scoping cover all access dimensions (org, project, user ownership, placement/visibility enum)?
- [ ] Are unknown or unrecognized access values (e.g., new placement enum variants) excluded by the query rather than passed through and checked later?

Why this matters:
- **Scales**: the database does the filtering; application code does not scan and discard.
- **No information leakage**: rows the caller cannot access are never loaded into memory, never logged, never risk appearing in error messages.
- **Single source of truth**: the query defines authorization; there is no second code path to drift out of sync.
- **Auditable**: the query is inspectable — `EXPLAIN` shows exactly what rows are considered.

#### Cursor pagination

- [ ] Do all paginated endpoints use cursor-based pagination keyed on a stable record ID — not offset/page-number?
- [ ] Is the response shape `{ items, nextCursor, hasMore }` with no `page`, `totalPages`, or `offset` fields?
- [ ] Does the underlying query use `WHERE id > :cursor ORDER BY id LIMIT :size` (or equivalent) — not `OFFSET`?
- [ ] If the UI needs page numbers, does the frontend synthesise them from cursor state rather than the API exposing offset semantics?

---

- See [reference/design-patterns.md](../reference/design-patterns.md) for the full design-pattern catalogue.
- See [reference/anti-patterns.md](../reference/anti-patterns.md) for the full anti-pattern catalogue.
- See [reference/design-principles/CHECKLIST.md](../reference/design-principles/CHECKLIST.md) for the design-principles checklist and detail links.
- See [reference/anti-patterns/CHECKLIST.md](../reference/anti-patterns/CHECKLIST.md) for the anti-pattern checklist.
