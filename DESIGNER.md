# Designer

Software design knowledge required of all agents operating in a design or architecture capacity.

> Spec authoring guide: `@design/SPECS.md`

---

## Data Flow Design vs Class-Based Design

These are two fundamentally different ways to organise a system. Neither is the default. The wrong choice for the problem produces unnecessary complexity and poor performance.

---

### Class-Based Design

Organises the system around objects that encapsulate state and behaviour. Objects hold their own data and expose operations on it. The design reflects the value semantics of the domain — what things *are* and what they *do*.

**Use when**:
- The system models a domain with distinct entities, identity, and
relationships (users, orders, accounts, rules).
- Behaviour varies by type — polymorphism and strategy patterns are natural.
- State is long-lived, mutable, and owned by individual entities.
- The number of distinct object types is large relative to the volume of
data items.
- Correctness and expressiveness matter more than raw throughput.

**Characteristics**:
- Objects are the unit of encapsulation and change.
- Data and the logic that operates on it live together.
- Interactions are modelled as method calls between objects.
- Memory layout is determined by object structure, not by access pattern.

**Examples**: business logic engines, rule systems, domain models, APIs, game entity/behaviour systems, configuration systems.

---

### Data Flow Design

Organises the system around the movement and transformation of data through a pipeline or graph of operations. Data is separated from the operations that process it. The design reflects *how data moves and is transformed*, not what objects own it.

**Use when**:
- The system processes a large volume of uniform, repeating data items.
- Throughput and cache efficiency are primary constraints.
- The same transformation is applied to many items of the same shape.
- Processing maps naturally to a pipeline: ingest → transform → output.
- The target is a GPU, vectorised CPU, database engine, or stream processor
where data layout in memory directly determines performance.

**Characteristics**:
- Data is stored in flat, contiguous structures (arrays, columns, buffers)
— not scattered across heap-allocated objects.
- Operations are functions applied across a collection, not methods on
individual objects.
- The pipeline is explicit — each stage has defined inputs and outputs.
- State is minimised between stages; stages are ideally pure functions.
- Memory access patterns are predictable and cache-friendly.

**Examples**: database query engines, GPU shaders, signal processing, image pipelines, physics simulations, columnar analytics, stream processors, neural network inference.

---

### Choosing Between Them

Do not default. Ask:

| Question | Points toward |
|----------|--------------|
| Am I modelling entities with identity and varied behaviour? | Class-based |
| Am I processing many uniform items at high throughput? | Data flow |
| Does correctness depend on encapsulating state per entity? | Class-based |
| Is cache efficiency or vectorisation a hard requirement? | Data flow |
| Does the domain have rich value semantics (rules, roles, types)? | Class-based |
| Is the problem a pipeline: ingest → transform → emit? | Data flow |
| Is the target a GPU, columnar store, or stream processor? | Data flow |
| Do objects interact with each other in complex, domain-specific ways? | Class-based |

**Mixed systems**: many real systems use both. A database engine uses data flow internally (columnar storage, vectorised execution) but exposes a class-based API to application code. A game may use class-based design for game logic and data flow (ECS) for the physics and rendering hot path. The boundary between the two should be explicit and intentional — data crosses it via a defined interface, not by leaking either model into the other.

**The wrong default**:
- Applying class-based design to a high-throughput data pipeline produces
heap fragmentation, cache misses, and poor vectorisation — the object model gets in the way of the hardware.
- Applying data flow design to a rich domain model produces anemic data
structures with logic scattered across pipeline stages — the domain becomes impossible to reason about.

---

See [reference/design-principles/CHECKLIST.md](reference/design-principles/CHECKLIST.md) for the per-principle design checklist.

---


## Design Principles

Design-principle details are maintained in the reference docs, not inlined here.

- [Design Principles Index](reference/design-principles.md)
- [Design Principles Checklist](reference/design-principles/CHECKLIST.md)


## Software Design Patterns

Pattern details are maintained in the reference docs, not inlined here.

- [Design Patterns Catalogue](reference/design-patterns.md)
- [Anti-Patterns Catalogue](reference/anti-patterns.md)
- [Design Principles Checklist](reference/design-principles/CHECKLIST.md)
- [Security Principles Index](reference/security-principles.md)
