## Law of Demeter

A unit should talk only to its immediate collaborators. Do not reach through an object to call methods on the objects it holds.

**The rule**: a method may call methods on:
1. Itself.
2. Objects passed to it as arguments.
3. Objects it constructs directly.
4. Its own direct fields/properties.

It must not call methods on objects returned by any of those calls.

**Signal of violation** — chains of dots:
```
# bad — reaching through order into customer into address
city = order.get_customer().get_address().get_city()

# good — ask the order directly
city = order.get_shipping_city()
```

Each extra dot in a chain is a dependency on the internal structure of an object you do not own. If that structure changes, your code breaks.

**Reducing cross-coupling**:
- Pass in what you need, do not navigate to it.
- Tell objects what to do; do not ask them for data and act on it yourself
(tell, don't ask).
- A unit that requires many imports from many different modules is coupled
to all of them — narrow the interface and inject only what is needed.
- Coupling travels in one direction: high-level policy depends on
abstractions; low-level detail implements them. Never reverse this.
- Shared mutable state is the strongest form of coupling — eliminate it
before all other coupling.

**Metrics to watch**:
- **Afferent coupling (Ca)** — how many modules depend on this one. High Ca
means a change here has wide impact; stabilise the interface.
- **Efferent coupling (Ce)** — how many modules this one depends on. High Ce
means this module is fragile to changes elsewhere; reduce imports.
- **Instability (I = Ce / (Ca + Ce))** — a module with high instability
(close to 1) changes often and has few dependents. A module with low instability (close to 0) is stable and depended upon by many — its interface must be locked down.

---
