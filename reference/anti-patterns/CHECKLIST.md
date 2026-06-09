# Anti-Pattern Checklist

Verify none of the following exist in the code under review. See [anti-patterns.md](../anti-patterns.md) for the full description of each.

---

#### God Object
- [ ] No single class or module accumulates state and logic that belongs elsewhere.
- [ ] No class has methods that operate on unrelated data or concerns.
- [ ] No class requires constructing the entire system just to test one behaviour.

#### Spaghetti Code
- [ ] Control flow does not jump arbitrarily across functions and modules.
- [ ] Every function has a clear entry point, purpose, and exit.
- [ ] No function can only be understood by tracing execution across five other files.

#### Lava Flow
- [ ] No dead or commented-out code is present.
- [ ] No "do not touch" comments exist — if the code is dangerous, it is understood and fixed or deleted.
- [ ] No unreachable branches or unused parameters remain.

#### Golden Hammer
- [ ] The tools and patterns used are chosen for the problem, not out of habit.
- [ ] No pattern is applied where it does not fit just because it is familiar.

#### Premature Optimisation
- [ ] No complex optimisation exists without a profiling result that justifies it.
- [ ] No readability has been sacrificed for a performance gain that has not been measured.

#### Shotgun Surgery
- [ ] A single logical change does not require edits scattered across many unrelated files.
- [ ] Concepts that change together live together.

#### Cargo Cult
- [ ] Every pattern or convention in use is understood — not just copied from another codebase.
- [ ] No boilerplate is present that nobody can explain.

#### Distributed Monolith
- [ ] Services are not so tightly coupled that they cannot be deployed independently.
- [ ] No shared database tables span service boundaries.
- [ ] No synchronous call chains cross every service before completing a request.

#### Shared Mutable State
- [ ] No in-memory state is written by more than one component without explicit synchronisation.
- [ ] No global variables are mutated across module boundaries.

#### Magic Numbers / Strings
- [ ] No unexplained numeric or string literals are embedded in logic.
- [ ] Every constant has a name that communicates its intent.

#### Anemic Domain Model
- [ ] Domain objects are not pure data bags with no behaviour.
- [ ] Business logic is not scattered across service classes operating on passive structs.
- [ ] Each domain object enforces its own invariants.

#### Leaky Abstraction
- [ ] No abstraction exposes details of what it is hiding.
- [ ] Callers do not need to know the underlying implementation to use the interface correctly.
- [ ] Error messages and exceptions do not expose internal implementation details to callers.

#### Service Locator
- [ ] No global registry or locator is used to look up dependencies at runtime.
- [ ] Dependencies are injected at the composition root, not fetched inside business logic.

#### Poltergeist
- [ ] No class exists solely to pass data through to another class with no logic of its own.
- [ ] Every class has a responsibility that cannot be trivially inlined into its caller.

#### Yo-yo Problem
- [ ] No inheritance hierarchy is so deep that understanding a method requires jumping up and down more than two levels.
- [ ] Behaviour is not split across many ancestor classes in a way that obscures what a subclass actually does.

#### Feature Envy
- [ ] No method operates primarily on data from another class rather than its own.
- [ ] Logic that belongs to a class lives in that class, not in a neighbour that reaches in for its data.

#### Primitive Obsession
- [ ] Raw primitives are not used in place of small domain types (e.g. `str` for an email, `int` for a currency amount).
- [ ] Concepts that have validation rules or behaviour have their own type.

#### Temporal Coupling
- [ ] No functions must be called in a specific order without that order being enforced by the type system or constructor.
- [ ] Objects are fully initialised after construction — no two-phase init patterns.

#### Reinventing the Wheel
- [ ] No bespoke implementation exists for something already provided by a well-tested standard library or dependency.
- [ ] The justification for any custom implementation is documented.

#### Middle Man
- [ ] No class delegates every method call to another class without adding any logic.
- [ ] If a class only wraps another, the wrapper is justified by a clear abstraction boundary.

#### Big Ball of Mud
- [ ] The system has a discernible, intentional architecture.
- [ ] No module depends on an arbitrary set of unrelated others.

#### Boat Anchor
- [ ] No component, library, or abstraction is kept solely because it might be useful later.
- [ ] Every dependency has a current, concrete consumer.

#### Copy-Paste Programming
- [ ] No block of logic exists in more than one place with minor variations.
- [ ] Shared logic is extracted to a single authoritative location.

#### Abstraction Inversion
- [ ] No abstraction hides primitives that its users must re-implement on top of it.
- [ ] The abstraction adds value; users are not fighting it.

#### Object Orgy
- [ ] No object exposes internal state freely for external mutation.
- [ ] All invariants are enforced at the object boundary, not by callers.

#### Parallel Inheritance Hierarchies
- [ ] Adding a subclass in one hierarchy does not require adding one in another.
- [ ] Hierarchies that always change together are collapsed or composed.

#### Refused Bequest
- [ ] No subclass overrides inherited methods to throw or return dummy values.
- [ ] Every subclass uses the behaviour it inherits (LSP holds).

#### Inappropriate Intimacy
- [ ] No two classes reach into each other's private internals.
- [ ] Cross-class dependencies cross a defined interface.

#### Data Clumps
- [ ] Groups of data items that always appear together are encapsulated in a type.
- [ ] No function takes three or more parameters that always travel together.

#### Long Parameter List
- [ ] No function or constructor takes more parameters than can be held in working memory (typically four or fewer).
- [ ] Parameter groups that belong together are encapsulated in an object.

#### Callback Hell
- [ ] Asynchronous code does not form a deeply nested pyramid of callbacks.
- [ ] Async flow is expressed via promises, async/await, or named continuation objects.

#### N+1 Query Problem
- [ ] No code fetches a list and then queries the database once per item.
- [ ] Bulk operations use joins, eager loading, or batched queries.

#### Not Invented Here (NIH)
- [ ] No bespoke implementation exists for a problem already solved by a well-tested library.
- [ ] The decision to write custom code over using an existing solution is documented.

#### Soft Coding
- [ ] Business logic lives in code, not in configuration files or database rows.
- [ ] Configuration is limited to values that genuinely vary per deployment.

#### Exception Swallowing
- [ ] No catch block is empty or logs without re-raising.
- [ ] Every caught exception is either handled explicitly or re-raised with context.

#### Circular Dependencies
- [ ] The dependency graph contains no cycles.
- [ ] No module imports another that imports it back.

#### Dependency Hell
- [ ] All dependency versions are pinned.
- [ ] No two dependencies require conflicting versions of the same transitive dependency.

#### Big Design Up Front (BDUF)
- [ ] Design is incremental — just enough for the current iteration.
- [ ] No significant design work has been done for features without current acceptance criteria.

#### Swiss Army Knife
- [ ] No class or interface combines unrelated responsibilities.
- [ ] Each interface can be implemented independently without implementing unrelated methods.

#### Singleton Overuse
- [ ] No singleton is accessed as global state throughout the codebase.
- [ ] Dependencies that happen to be single instances are injected, not fetched globally.

#### Star-Alias
- [ ] No implementation widens interface parameter types via intersection (`Type & { extra }`).
- [ ] Implementation method signatures match the interface exactly.
- [ ] No variable or column holds two distinct pieces of data (e.g. `"userId:orgId"`).
- [ ] No variable is reused for a different purpose than its name suggests.
- [ ] One variable, one meaning. One column, one value.
