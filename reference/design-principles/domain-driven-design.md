## Domain-Driven Design (DDD)

Organise software around the business domain. The model in code should reflect the model the domain experts use to reason about the problem.

**Core concepts**:

| Concept | Meaning |
|---------|---------|
| **Entity** | An object with a distinct identity that persists over time (e.g. a `User` with an `id`) |
| **Value Object** | An object defined entirely by its attributes; no identity; immutable (e.g. a `Money` amount) |
| **Aggregate** | A cluster of entities and value objects treated as a single unit; one root entity controls access |
| **Aggregate Root** | The entry point to an aggregate; external code only holds references to the root |
| **Repository** | Abstracts persistence for an aggregate; the domain does not know about SQL or storage |
| **Domain Service** | Stateless logic that does not belong to a single entity or value object |
| **Domain Event** | A record that something meaningful happened in the domain; named in past tense |
| **Bounded Context** | An explicit boundary within which a model is defined and consistent; different contexts may use different models for the same concept |
| **Ubiquitous Language** | A shared vocabulary between engineers and domain experts; used in code, docs, and conversation |

**Rules**:
- Business rules live in the domain layer — not in controllers, not in
repositories, not in the framework.
- Aggregates are the consistency boundary. Only the aggregate root enforces
invariants across its members.
- Cross-aggregate references are by identity only — never hold a direct
object reference across an aggregate boundary.
- Each bounded context has its own model. Do not share entity classes
between contexts — map explicitly at the boundary.

---
