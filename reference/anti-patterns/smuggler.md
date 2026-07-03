# Smuggler Anti-Pattern

**Also known as:** Metadata Smuggling, Data Envelope Bypass, Hidden Side Channel

## Problem

Metadata is hidden inside a data object instead of being carried beside it in a separate field or envelope. The object now has two meanings: user data and system control data.

Common forms:

1. **Metadata in row data** — fields like `_permissions`, `_rowType`, `_allowedOps`, `_internal`, or `__meta` are mixed into the same object as user records.
2. **Reserved-prefix contracts** — code relies on prefixes such as `_` or `__` to distinguish system fields from user fields.
3. **Projection bypasses** — early returns skip the mapper/projector that strips or validates hidden metadata.
4. **Allowlist patches** — an allowlist is added to protect the hidden metadata convention instead of separating the data model.

## Example

```typescript
// Wrong: metadata and user fields share one namespace.
const row = {
  recordId: "acct_123",
  name: "Acme",
  _rowType: "folder",
  _permissions: { read: true },
};

if (properties.length === 0) {
  return row; // skips projection and leaks every raw field
}
```

```typescript
// Right: data and metadata cannot collide.
const row = {
  recordId: "acct_123",
  data: {
    name: "Acme",
  },
  meta: {
    rowType: "folder",
    permissions: { read: true },
  },
};
```

## Why It Happens

1. **Fast wiring** — adding one field to an existing row is quicker than changing the contract.
2. **Flat API convenience** — callers want one object even when it contains separate concerns.
3. **Avoided migration** — changing to an envelope requires updating adapters, projectors, tests, and callers.
4. **Post-hoc safety** — allowlists and spread-order rules are added after collisions appear.

## Consequences

- **Namespace collision** — a user field can look like system metadata.
- **Security leakage** — raw adapter/source fields can reach UI or API callers.
- **Hidden contract** — consumers must know prefix rules and spread order.
- **Projection holes** — zero-field, empty-list, or early-return paths skip sanitization.
- **Fragile tests** — happy-path projection tests pass while raw bypass paths leak.

## Detection

- `grep` for metadata-looking keys inside row/data shapes: `_rowType`, `_permissions`, `_allowedOps`, `_meta`, `__meta`, `meta_`.
- Look for prefix filters or allowlists such as `startsWith("_")`, `ROW_META_KEYS`, or `allowedMetaKeys`.
- Inspect every early return around projection/mapping code, especially zero-property and empty-list cases.
- Trace raw adapter rows to the API/UI boundary. Every path must pass through the same projector or sanitizer.
- In review: if the fix depends on spread order, reserved prefixes, or an allowlist for mixed data, call it smuggling.

## Fix

Use an explicit envelope. User data and system metadata get separate named locations.

```typescript
type AdapterRow = {
  recordId: string;
  data: Record<string, unknown>;
  meta: {
    rowType?: string;
    permissions?: RowPermissions;
    allowedOps?: string[];
  };
};
```

Project every response through one path. No early return may bypass validation, projection, or sanitization.

## Related

- **Star-Alias** — one field or variable holds multiple meanings.
- **Primitive Obsession** — raw strings and prefixes substitute for domain types.
- **Leaky Abstraction** — callers must know internal metadata conventions.
- **Security Review** — raw internal fields can leak across trust boundaries.
