# Defensive Duct-Taping

**Also known as:** Shotgun Null-Checking, Glue-Safety Duct-Tape

## Problem

- Fallback operators (`?? {}`, `?? []`, `?.`, `|| ""`) are added to silence a crash instead of fixing the data contract.
- The fallback fabricates a value the caller never sent.
- The fabricated value is validated, passed on, or discarded as if it were real input.
- The same fallback is repeated at every layer because no layer owns the contract.

## Example

```typescript
// Wrong: validates a fabricated {} and discards the parsed result.
parseV2(empty, body ?? {});
await oauth.start(credentialId, body?.callback ?? "");
```

- `body ?? {}` is a conversion hidden inside a validation call.
- `parseV2` checks an object the caller did not send.
- The parsed result is thrown away, so the check proves nothing downstream.
- `body?.callback` repeats the guard the boundary was meant to settle.

```typescript
// Right: the boundary states the contract once; downstream takes typed values.
assertNoBody(req);
await oauth.start(credentialId, caller, callbackContext);
```

## Why It Happens

- **Crash-driven patching** — a `TypeError` in a log is fixed at the line that threw, not at the source of the value.
- **Unknown contract** — nobody stated whether the value is required, optional, or absent.
- **Copy-forward** — a guard seen in one place is copied to every neighbour.

## Consequences

- **Masks upstream bugs** — an API, query, or parent function that wrongly returned `null` is never found; the failure surfaces far from its origin or not at all.
- **Hidden conversion** — the real input and the value in use differ, and the switch is an inline side effect.
- **Cascading noise** — once one function accepts unexpected nullish values, every downstream function adds `?? {}` or `?.` to survive.
- **False type safety** — `?? {}` satisfies the TypeScript compiler without guaranteeing the expected properties exist at runtime.
- **Zombie states** — the app keeps running on empty defaults (blank UI cards, empty payloads) instead of hitting an error boundary, retry state, or validation error.
- **Untraceable flow** — a reader cannot tell which layer owns the null case.
- **Dead guards** — downstream checks for states the boundary already excluded.
- **Allocation churn** — `x ?? {}` allocates a new object on every nullish call.
- **Reference instability** — `x ?? {}` / `x ?? []` as a React prop or dependency breaks shallow equality and re-renders.

## Detection

- `grep` for `?? {}`, `?? []`, `|| {}`, `|| []`, `?? ""`, `.get(k, {})`, `or {}`.
- A fallback inside a call argument: `f(x ?? {})`.
- A validator or parser whose return value is unused.
- `?.` on a value whose type is non-optional, or that the boundary already validated.
- The same guard on the same value in more than one layer.

## Fix

- **State the contract** — decide per input: required, optional with a named default, or absent.
- **Validate once at the boundary** — reject missing required input with a typed error or 4xx.
- **Use the parsed result** — the validator returns the typed value and downstream takes that value.
- **Bodyless commands take no body** — assert no body; pass the explicit params (IDs, caller, context).
- **Name real defaults** — a legitimate default is a named constant set at the boundary, not an inline `?? {}`.
- **Delete downstream guards** — internal code trusts the typed value the boundary produced.
- **Tighten types** — remove `| undefined` / `Optional` from internal signatures the boundary already settled.

## Related

- **Exception Swallowing** — both hide a failure instead of surfacing it.
- **Star-Alias** — the fallback widens a value's meaning to "real input or fabricated default".
- **Lava Flow** — dead guards accumulate and nobody dares remove them.
- **Design Review → Defensive Programming** — defensive checks belong at the boundary, not throughout internals.
