# TypeScript Standards

## For Loops

Prefer `for...of` for values and `.entries()` when the index is needed.

```typescript
for (const user of users) {
  activateUser(user);
}

for (const [index, user] of users.entries()) {
  logUser(index, user);
}
```

Avoid C-style index loops unless the index arithmetic is the point.

## Enums

Use exported `as const` values plus a union type derived from `typeof` for finite string modes, statuses, and capability flags.

Do not use raw inline string comparisons or magic numbers for domain values. Named constants make call sites searchable, prevent typo-prone literals from spreading, and keep the compiler tied to the actual exported values.

```typescript
// Bad: raw string literals become magic values at every call site.
export type CapabilityMode = "none" | "optional" | "required";

if (mode === "required") {
  enableCapability();
}
```

```typescript
// Good: constants define the allowed values and comparisons reuse them.
export const CAPABILITY_NONE = "none" as const;
export const CAPABILITY_OPTIONAL = "optional" as const;
export const CAPABILITY_REQUIRED = "required" as const;

export type CapabilityMode =
  | typeof CAPABILITY_NONE
  | typeof CAPABILITY_OPTIONAL
  | typeof CAPABILITY_REQUIRED;

if (mode === CAPABILITY_REQUIRED) {
  enableCapability();
}
```

For numeric domain values, use the same principle: give the value a named constant and compare against the constant instead of an inline number.

## Switches

Use `switch` for one discriminant with several known cases. Keep each case short and force exhaustiveness with `never`.

```typescript
function labelMode(mode: CapabilityMode): string {
  switch (mode) {
    case CAPABILITY_NONE:
      return "Disabled";
    case CAPABILITY_OPTIONAL:
      return "Optional";
    case CAPABILITY_REQUIRED:
      return "Required";
    default: {
      const exhaustive: never = mode;
      return exhaustive;
    }
  }
}
```

Use `if` for ranges, compound conditions, or predicates that are not one exact value.

## Fail Early

Use guard clauses to reject invalid or empty cases first. Keep the main path at the left edge.

```typescript
function sendInvite(user: User): void {
  if (!user.email) {
    throw new Error("email is required");
  }
  if (user.isDisabled) {
    return;
  }

  sendEmail(user.email);
}
```

Avoid deep nesting for ordinary validation and preconditions.
