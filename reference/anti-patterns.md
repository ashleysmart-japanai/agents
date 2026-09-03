# Anti-Patterns

| Anti-Pattern | Summary |
|---|---|
| [Abstraction Inversion](anti-patterns/abstraction-inversion.md) | A high-level abstraction hides low-level primitives that users need, forcing them to re-implement those primitives on top of the abstraction |
| [Anemic Domain Model](anti-patterns/anemic-domain-model.md) | Domain objects are pure data bags with no behaviour. All logic lives in service classes that operate on passive structs |
| [Big Ball of Mud](anti-patterns/big-ball-of-mud.md) | A system with no discernible architecture. Everything depends on everything. Structure grew organically through patches and shortcuts until none remains |
| [Big Design Up Front (BDUF)](anti-patterns/big-design-up-front.md) | Designing the entire system in detail before any code is written, assuming all requirements are known and stable |
| [Boat Anchor](anti-patterns/boat-anchor.md) | A component, library, or abstraction kept in the codebase because it might be useful later, even though it serves no current purpose |
| [Callback Hell](anti-patterns/callback-hell.md) | Deeply nested callbacks where each step is defined inside the handler of the previous step, forming a pyramid of indented code |
| [Cargo Cult](anti-patterns/cargo-cult.md) | Copying a pattern or practice without understanding why it works — following the form without the function |
| [Circular Dependencies](anti-patterns/circular-dependencies.md) | Module A imports module B, which imports module A. The dependency graph contains a cycle |
| [Copy-Paste Programming](anti-patterns/copy-paste-programming.md) | Duplicating code rather than abstracting a shared implementation. The logic exists in many places, each slightly different |
| [Data Clumps](anti-patterns/data-clumps.md) | The same group of data items (e.g. `street`, `city`, `postcode`) appear together repeatedly across parameters, fields, and returns but are never encapsulated into a single type |
| [Dependency Hell](anti-patterns/dependency-hell.md) | A web of transitive dependencies with conflicting version requirements that cannot all be satisfied simultaneously |
| [Distributed Monolith](anti-patterns/distributed-monolith.md) | A system split into multiple services that are so tightly coupled — shared databases, synchronous call chains, coordinated deploys — that they cannot be developed or deployed independently |
| [Exception Swallowing](anti-patterns/exception-swallowing.md) | Catching an exception and doing nothing with it — silently ignoring a failure |
| [Feature Envy](anti-patterns/feature-envy.md) | A method that operates primarily on data from another class rather than its own |
| [God Object](anti-patterns/god-object.md) | A single class or module that knows too much and does too much — accumulates state and logic that belongs elsewhere |
| [Gold Plating](anti-patterns/gold-plating.md) | Over-engineering: durability, abstraction, or protection added far beyond the requirement — e.g. temporary scaffolding for a seconds-long deploy gap whose build/track/remove cost exceeds the gap; a genuine zero-downtime need is a deliberate two-PR expand/contract instead |
| [Golden Hammer](anti-patterns/golden-hammer.md) | Applying a familiar tool or pattern to every problem regardless of fit ("if all you have is a hammer…") |
| [Inappropriate Intimacy](anti-patterns/inappropriate-intimacy.md) | Two classes are too deeply coupled to each other's internal details — each reaches into the other's private parts |
| [Lava Flow](anti-patterns/lava-flow.md) | Dead or unknown code that remains because nobody dares remove it. Often accompanied by comments like "do not touch" |
| [Leaky Abstraction](anti-patterns/leaky-abstraction.md) | An abstraction that exposes details of what it is hiding, forcing callers to understand the underlying implementation to use it correctly |
| [Long Parameter List](anti-patterns/long-parameter-list.md) | A function or constructor takes so many parameters that callers cannot reason about what each one does |
| [Magic Numbers / Strings](anti-patterns/magic-numbers-strings.md) | Literal values embedded directly in logic with no name or explanation |
| [Middle Man](anti-patterns/middle-man.md) | A class that does nothing but delegate every method call to another class, adding no logic of its own |
| [N+1 Query Problem](anti-patterns/n-plus-1-query.md) | Fetching a list of N items and then making one additional database query per item — N+1 queries total instead of one or two |
| [Not Invented Here (NIH)](anti-patterns/not-invented-here.md) | Refusing to use existing, well-tested solutions and re-implementing them internally out of preference for home-grown code |
| [Object Orgy](anti-patterns/object-orgy.md) | Objects expose their internal state freely, allowing any caller to read and mutate it without restriction |
| [Parallel Inheritance Hierarchies](anti-patterns/parallel-inheritance-hierarchies.md) | Adding a subclass in one hierarchy always requires adding a corresponding subclass in another hierarchy |
| [Poltergeist](anti-patterns/poltergeist.md) | A class that exists solely to pass data through to another class, with no logic or responsibility of its own |
| [Premature Optimisation](anti-patterns/premature-optimisation.md) | Optimising code before profiling confirms where the bottleneck is |
| [Primitive Obsession](anti-patterns/primitive-obsession.md) | Using raw primitives in place of small domain types (e.g. `str` for an email address, `int` for a currency amount) |
| [Refused Bequest](anti-patterns/refused-bequest.md) | A subclass inherits methods from a parent but does not use them, overrides them to throw, or returns dummy values |
| [Reinventing the Wheel](anti-patterns/reinventing-the-wheel.md) | Implementing something that already exists as a well-tested, maintained library or standard library module |
| [Service Locator](anti-patterns/service-locator.md) | A global registry used to look up dependencies at runtime rather than injecting them at construction |
| [Shared Mutable State](anti-patterns/shared-mutable-state.md) | Multiple components reading and writing the same in-memory state without synchronisation |
| [Shotgun Surgery](anti-patterns/shotgun-surgery.md) | A single logical change requires edits scattered across many unrelated files and classes |
| [Singleton Overuse](anti-patterns/singleton-overuse.md) | Using Singleton as a back door for global state — any code can reach the instance at any time, creating hidden dependencies throughout the system |
| [Smuggler](anti-patterns/smuggler.md) | Metadata or control data is hidden inside user data instead of carried in a separate envelope, creating collisions and projection bypasses |
| [Soft Coding](anti-patterns/soft-coding.md) | Making every decision configurable to avoid committing to anything — the opposite of magic numbers but equally harmful. Business logic is pushed into configuration files or databases |
| [Spaghetti Code](anti-patterns/spaghetti-code.md) | Control flow jumps arbitrarily across functions and modules with no clear structure or layering |
| [Swiss Army Knife](anti-patterns/swiss-army-knife.md) | A class or interface that does many unrelated things — the opposite of SRP at the API surface level |
| [Temporal Coupling](anti-patterns/temporal-coupling.md) | Functions or methods that must be called in a specific order, with no enforcement of that order by the type system or constructor |
| [Star-Alias](anti-patterns/star-alias.md) | A single variable, parameter, or column holds distinct pieces of data, is reused for a different purpose, or widens a type beyond what the interface declares |
| [Yo-yo Problem](anti-patterns/yo-yo-problem.md) | A deep inheritance hierarchy where understanding a method requires jumping up and down through many ancestor classes |
