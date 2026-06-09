# Star-Alias Anti-Pattern

**Also known as:** Type Widening at Implementation, Overloaded Variable, Column Stuffing

## Problem

A single variable, parameter, or storage location is used to hold distinct pieces of data, or is reused for a different purpose than its name suggests. The name says one thing, the contents say another.

Three common forms:

1. **Type widening** — an implementation widens a parameter type beyond what the interface declares (e.g. intersection types). Callers following the interface contract don't know about the extra field.
2. **Column/variable stuffing** — two distinct values packed into one field (e.g. `"userId:orgId"` in a single column, or a `status` field that also encodes an error message).
3. **Variable reuse** — a variable is assigned once for one purpose, then reassigned later for a completely different purpose. The name no longer describes what it holds.

## Example

```typescript
// Interface declares a clean contract
interface Adapter {
  introspectFields(args: {
    resource: string;
    context: AdapterContext;
  }): Promise<FieldResult>;
}

// Implementation silently widens the type
class SfaAdapter implements Adapter {
  async introspectFields(args: {
    resource: string;
    context: AdapterContext & { credentialId?: string }; // ← smuggled field
  }) {
    const cred = args.context.credentialId; // works at runtime
    // ...
  }
}
```

TypeScript allows this because the implementation can accept a *wider* type than the interface requires (covariance on input is unsound but TypeScript permits it for pragmatism). The code compiles, but:

- The interface lies about what callers must provide
- Every adapter independently re-declares the same intersection
- A new adapter following the interface signature won't receive the field
- The service layer must manually jam the extra field onto the object — the type system doesn't enforce it

## Why It Happens

1. **Incremental feature addition** — a new capability is needed but adding a proper field or parameter feels risky or requires touching many files.
2. **Convenience** — packing data into an existing field is quick. Splitting it out means a migration or interface change.
3. **Lack of ownership** — no one wants to change the shared contract or schema, so everyone stuffs data into what's already there.
4. **Variable laziness** — reusing an existing variable instead of declaring a new one with a clear name.

## Consequences

- **Hidden contract** — the real structure of the data is not visible from the type, schema, or variable name.
- **Fragile parsing** — consumers must "know" the encoding (split on `:`, check prefix, etc). Miss the convention and data is silently wrong.
- **Ambiguous reads** — a variable or column means different things at different points in time or in different contexts.
- **Testing gaps** — tests written against the declared type won't cover the smuggled data.
- **Migration pain** — unpacking stuffed columns later requires backfills and dual-read logic.

## Detection

- `grep` for `& {` on method parameters in classes that implement an interface (type widening).
- Look for string splitting/joining on columns or variables (`split(":")`, `${a}:${b}`).
- A variable assigned in one block and reassigned to something unrelated later.
- A database column whose values require parsing to extract distinct pieces of data.
- In code review: if you need to explain "this field actually contains X and Y", it's star-alias.

## Fix

Each value gets its own named location. One variable, one meaning. One column, one value.

```typescript
// Wrong — credentialId smuggled into context via intersection
introspectFields(args: {
  resource: string;
  context: AdapterContext & { credentialId?: string };
})

// Right — each parameter is one thing
introspectFields(args: {
  resource: string;
  credentialId?: string;
  context: AdapterContext;
})
```

```sql
-- Wrong — two values packed into one column
identifier TEXT  -- contains "userId:orgId"

-- Right — each value has its own column
user_id TEXT
org_id  TEXT
```

```python
# Wrong — variable reused for different purpose
result = fetch_users()
# ... 50 lines later ...
result = calculate_totals()  # now "result" means something else

# Right — distinct names
users = fetch_users()
totals = calculate_totals()
```

## Related

- **Data Clumps** — multiple fields always passed together should be a named type.
- **Feature Envy** — if the implementation reaches into the widened context for data it shouldn't need, the responsibility may be in the wrong place.
- **Leaky Abstraction** — the interface hides a dependency that implementations actually require.
- **Shotgun Surgery** — fixing the interface later requires updating every implementation that independently widened the type.
