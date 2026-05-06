# Design Patterns

## Creational
| Pattern | Summary |
|---|---|
| [Abstract Factory](design-patterns/abstract-factory.md) | Create families of related objects without specifying their concrete classes |
| [Builder](design-patterns/builder.md) | Construct a complex object step-by-step; separate construction from representation |
| [Factory Method](design-patterns/factory-method.md) | Delegate instantiation to a subclass or factory function; callers depend on the interface, not the concrete type |
| [Lazy Initialisation](design-patterns/lazy-initialisation.md) | Delay creation of an object or computation of a value until the first time it is needed |
| [Multiton](design-patterns/multiton.md) | Like Singleton but keyed — one instance per named key, managed by the class itself |
| [Object Pool](design-patterns/object-pool.md) | Reuse a fixed set of expensive objects rather than creating and destroying them per use |
| [Prototype](design-patterns/prototype.md) | Clone an existing object rather than constructing from scratch |
| [Singleton](design-patterns/singleton.md) | Ensure a class has exactly one instance; prefer dependency injection over global access |

## Structural
| Pattern | Summary |
|---|---|
| [Adapter](design-patterns/adapter.md) | Wrap an incompatible interface so it matches the one a client expects |
| [Bridge](design-patterns/bridge.md) | Decouple an abstraction from its implementation so both can vary independently |
| [Composite](design-patterns/composite.md) | Treat individual objects and compositions uniformly through a shared interface |
| [Decorator](design-patterns/decorator.md) | Add behaviour to an object at runtime by wrapping it; preserves the interface |
| [Facade](design-patterns/facade.md) | Provide a simplified interface over a complex subsystem |
| [Flyweight](design-patterns/flyweight.md) | Share fine-grained objects to reduce memory when many instances share state |
| [Module](design-patterns/module.md) | Group related functions, types, and state behind a single cohesive interface; hide internals |
| [Proxy](design-patterns/proxy.md) | Control access to an object — for lazy init, access control, or caching |

## Behavioural
| Pattern | Summary |
|---|---|
| [Chain of Responsibility](design-patterns/chain-of-responsibility.md) | Pass a request along a chain of handlers; each handler decides to process or forward |
| [Command](design-patterns/command.md) | Encapsulate a request as an object; enables undo, queuing, and logging |
| [Interpreter](design-patterns/interpreter.md) | Define a grammar for a language and provide an interpreter to evaluate sentences in it |
| [Iterator](design-patterns/iterator.md) | Provide sequential access to elements without exposing the underlying structure |
| [Mediator](design-patterns/mediator.md) | Centralise communication between objects to reduce direct dependencies |
| [Memento](design-patterns/memento.md) | Capture and restore an object's state without violating encapsulation |
| [Null Object](design-patterns/null-object.md) | Provide a do-nothing implementation of an interface to eliminate null checks at call sites |
| [Observer](design-patterns/observer.md) | Notify dependents automatically when an object's state changes |
| [Specification](design-patterns/specification.md) | Encapsulate a business rule as a composable predicate object; combine with and/or/not |
| [State](design-patterns/state.md) | Allow an object to alter its behaviour when its internal state changes |
| [Strategy](design-patterns/strategy.md) | Define a family of algorithms, encapsulate each, and make them interchangeable |
| [Template Method](design-patterns/template-method.md) | Define the skeleton of an algorithm in a base class; let subclasses fill in steps |
| [Visitor](design-patterns/visitor.md) | Add operations to an object structure without modifying the classes of its elements |

## Architectural
| Pattern | Summary |
|---|---|
| [Active Record](design-patterns/active-record.md) | Wrap a database row in a domain object that also handles its own load, save, and delete |
| [Anti-Corruption Layer](design-patterns/anti-corruption-layer.md) | Translate between two different domain models at an integration boundary so neither corrupts the other |
| [Broker](design-patterns/broker.md) | Decouple clients from servers through an intermediary that locates servers, routes requests, and forwards results |
| [Data Mapper](design-patterns/data-mapper.md) | Map between domain objects and database rows without coupling either side to the other |
| [Event-Driven Architecture](design-patterns/event-driven-architecture.md) | Components communicate exclusively through events; producers and consumers are fully decoupled |
| [Hexagonal Architecture (Ports and Adapters)](design-patterns/hexagonal-architecture.md) | Isolate the domain from all external concerns behind ports; adapters implement the ports for specific technologies |
| [Layered Architecture](design-patterns/layered-architecture.md) | Organise code into horizontal layers with dependencies flowing downward only |
| [Microservices](design-patterns/microservices.md) | Decompose an application into small, independently deployable services, each owning its data and business capability |
| [Pipe and Filter](design-patterns/pipe-and-filter.md) | Process data through a sequence of independent processing steps (filters) connected by channels (pipes) |
| [Repository](design-patterns/repository.md) | Abstract persistence behind a collection-like interface; domain does not know about storage |
| [Service Layer](design-patterns/service-layer.md) | Define an application's boundary with a layer of services that establishes available operations and coordinates responses |
| [Service Object](design-patterns/service-object.md) | Encapsulate a single business operation in a stateless object with one public method |
| [Space-Based Architecture](design-patterns/space-based-architecture.md) | Eliminate the database as a bottleneck by storing all shared state in an in-memory data grid distributed across processing units |
| [Strangler Fig](design-patterns/strangler-fig.md) | Incrementally replace a legacy system by routing requests to new implementation; retire the old gradually |
| [Unit of Work](design-patterns/unit-of-work.md) | Track all changes made during a transaction and write them out as a single atomic operation |

## Concurrency
| Pattern | Summary |
|---|---|
| [Active Object](design-patterns/active-object.md) | Decouple method invocation from execution; calls are queued and executed asynchronously in the object's own thread |
| [Future / Promise](design-patterns/future-promise.md) | A proxy for a result not yet computed; the computation proceeds concurrently while the caller may continue or block when the result is needed |
| [Half-Sync/Half-Async](design-patterns/half-sync-half-async.md) | Separate synchronous and asynchronous processing layers with a queue between them |
| [Monitor Object](design-patterns/monitor-object.md) | Synchronise concurrent method execution so only one method runs at a time within an object |
| [Proactor](design-patterns/proactor.md) | Handle asynchronous operations by invoking completion handlers when operations finish |
| [Reactor](design-patterns/reactor.md) | Handle service requests dispatched concurrently by demultiplexing events and dispatching to registered handlers |
| [Read-Write Lock](design-patterns/read-write-lock.md) | Allow multiple concurrent readers or one exclusive writer; readers never block each other |
| [Scheduler](design-patterns/scheduler.md) | Control the order in which threads access shared resources based on a defined policy |
| [Thread Pool](design-patterns/thread-pool.md) | Maintain a pool of worker threads that pick up tasks from a queue, avoiding per-task thread creation overhead |

## Enterprise Integration
| Pattern | Summary |
|---|---|
| [Aggregator](design-patterns/aggregator.md) | Collect related messages and combine them into a single message once a completion condition is met |
| [Claim Check](design-patterns/claim-check.md) | Store a large message payload externally and pass only a reference (claim check) in the message |
| [Content-Based Router](design-patterns/content-based-router.md) | Route a message to a different channel based on its content |
| [Correlation Identifier](design-patterns/correlation-identifier.md) | Attach a unique ID to a request so that replies can be matched back to the original request |
| [Dead Letter Channel](design-patterns/dead-letter-channel.md) | Move unprocessable messages to a holding channel for investigation rather than discarding them |
| [Message Store](design-patterns/message-store.md) | Persist messages to a central store for auditing, replay, and debugging without disrupting the primary flow |
| [Process Manager](design-patterns/process-manager.md) | Maintain state and coordinate a multi-step workflow across multiple channels and services |
| [Request-Reply](design-patterns/request-reply.md) | Send a message and receive a reply on a known reply channel, achieving synchronous semantics over async messaging |
| [Routing Slip](design-patterns/routing-slip.md) | Attach a list of processing steps to a message; each processor removes itself from the slip and forwards to the next |
| [Scatter-Gather](design-patterns/scatter-gather.md) | Broadcast a request to multiple recipients and aggregate their replies into a single response |
| [Splitter](design-patterns/splitter.md) | Split a composite message into individual messages for separate downstream processing |
| [Wire Tap](design-patterns/wire-tap.md) | Intercept messages on a channel for logging or monitoring without disrupting the primary flow |

## Distributed
| Pattern | Summary |
|---|---|
| [Ambassador](design-patterns/ambassador.md) | Proxy network calls from the main service through a helper that handles retries, circuit breaking, and observability |
| [API Gateway](design-patterns/api-gateway.md) | Single entry point for all clients that routes to backend services, handles auth, and aggregates responses |
| [Backends for Frontends (BFF)](design-patterns/backends-for-frontends.md) | Separate backend API surface per client type to serve each client's specific needs |
| [Blue-Green Deployment](design-patterns/blue-green-deployment.md) | Maintain two identical environments; switch all traffic between them for zero-downtime deployments and instant rollback |
| [Bulkhead](design-patterns/bulkhead.md) | Isolate components into pools so a failure in one pool does not exhaust resources for others |
| [Canary Release](design-patterns/canary-release.md) | Route a small percentage of traffic to a new version of a service; monitor before rolling out fully |
| [Change Data Capture (CDC)](design-patterns/change-data-capture.md) | Capture row-level changes from a database and publish them as events to downstream consumers |
| [Choreography](design-patterns/choreography.md) | Services react to events with no central coordinator; each service knows what to do when it receives an event |
| [Circuit Breaker](design-patterns/circuit-breaker.md) | Stop calling a failing service after a threshold; reset after a cool-down period |
| [Compensating Transaction](design-patterns/compensating-transaction.md) | Undo a completed step in a distributed workflow by applying a semantically inverse operation |
| [Competing Consumers](design-patterns/competing-consumers.md) | Multiple consumer instances read from the same queue; each message processed by exactly one consumer |
| [CQRS](design-patterns/cqrs.md) | Separate read and write models; reads use a denormalised projection, writes go through a command handler |
| [Distributed Tracing](design-patterns/distributed-tracing.md) | Attach a trace ID to a request and collect timing spans from every service it touches to reconstruct the full execution path |
| [Event Sourcing](design-patterns/event-sourcing.md) | Store state as an append-only sequence of events; current state is derived by replaying them |
| [Externalized Configuration](design-patterns/externalized-configuration.md) | Extract all environment-specific configuration from the service binary into an external store |
| [Feature Toggle](design-patterns/feature-toggle.md) | Enable or disable features at runtime without deploying new code |
| [Health Endpoint Monitoring](design-patterns/health-endpoint-monitoring.md) | Expose a dedicated endpoint that reports service health; consumed by load balancers and orchestrators |
| [Idempotent Consumer](design-patterns/idempotent-consumer.md) | Ensure processing a message more than once has the same effect as processing it once |
| [Inbox](design-patterns/inbox.md) | Store incoming messages in a local inbox table and process them exactly once, even if the same message is delivered multiple times |
| [Leader Election](design-patterns/leader-election.md) | Designate one node as coordinator for a task; remaining nodes stand by and take over on failure |
| [Outbox](design-patterns/outbox.md) | Write events to a local outbox table in the same transaction as the domain write; a relay process forwards them to the broker |
| [Publisher-Subscriber](design-patterns/publisher-subscriber.md) | Producers publish to topics; consumers subscribe independently; producers and consumers are fully decoupled |
| [Read Replicas](design-patterns/read-replicas.md) | Route read queries to replicas of the primary to offload read load and improve throughput |
| [Retry with Backoff](design-patterns/retry-with-backoff.md) | Re-attempt a failed operation with increasing delays; cap total attempts |
| [Saga](design-patterns/saga.md) | Coordinate a long-running transaction across services using local transactions with compensating actions on failure |
| [Service Discovery](design-patterns/service-discovery.md) | Services register their network location; clients query a registry to find them rather than using hard-coded addresses |
| [Sharding](design-patterns/sharding.md) | Partition data across multiple storage nodes by a shard key to distribute load and storage |
| [Sidecar](design-patterns/sidecar.md) | Deploy a helper process alongside the main service to handle cross-cutting concerns |
| [Throttling](design-patterns/throttling.md) | Limit the rate at which a consumer can use a resource; shed excess load gracefully |
| [Two-Phase Commit (2PC)](design-patterns/two-phase-commit.md) | Coordinate an atomic commit across multiple participants using a prepare phase followed by a commit or abort |
| [Valet Key](design-patterns/valet-key.md) | Grant a client a time-limited, scoped token to access a resource directly without routing through the service |
| [Write-Ahead Log (WAL)](design-patterns/write-ahead-log.md) | Write changes to a durable log before applying them to the data structure; enables crash recovery and replication |

## UI / Presentation
| Pattern | Summary |
|---|---|
| [Flux / Redux](design-patterns/flux-redux.md) | Unidirectional data flow — actions describe what happened, a dispatcher routes them, a store updates state, the view re-renders from state |
| [Model-View-Controller (MVC)](design-patterns/mvc.md) | Separate data (model), display (view), and user input handling (controller) into distinct components |
| [Model-View-Presenter (MVP)](design-patterns/mvp.md) | Like MVC but the presenter takes full control of the view; the view is passive |
| [Model-View-ViewModel (MVVM)](design-patterns/mvvm.md) | The view model exposes data and commands as observable streams that the view binds to declaratively |
| [Presentation Model](design-patterns/presentation-model.md) | Extract all UI logic into a presentation model object; the view is a thin rendering shell |
