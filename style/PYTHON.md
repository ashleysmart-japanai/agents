# Python Standards

## For Loops

Iterate directly over values. Use `enumerate` for indices and `zip` for paired sequences.

```python
for user in users:
    activate_user(user)

for index, user in enumerate(users):
    log_user(index, user)

for user, role in zip(users, roles, strict=True):
    assign_role(user, role)
```

Avoid `range(len(items))` unless index arithmetic is required.

## Enums

Use `Enum`, `StrEnum`, or named constants for domain values. Do not compare raw strings or magic numbers inline.

```python
from enum import StrEnum


class CapabilityMode(StrEnum):
    NONE = "none"
    OPTIONAL = "optional"
    REQUIRED = "required"


if mode is CapabilityMode.REQUIRED:
    enable_capability()
```

Use named constants for numeric domain values.

```python
MAX_RETRIES = 3
```

## Switches

Use `match` for one value with several known shapes or constants. Keep cases short.

```python
match mode:
    case CapabilityMode.NONE:
        label = "Disabled"
    case CapabilityMode.OPTIONAL:
        label = "Optional"
    case CapabilityMode.REQUIRED:
        label = "Required"
    case _:
        raise ValueError(f"unknown capability mode: {mode}")
```

Use `if` for ranges, compound conditions, or predicates.

## Fail Early

Use guard clauses for invalid or empty cases. Keep the main path at the left edge.

```python
def send_invite(user: User) -> None:
    if not user.email:
        raise ValueError("email is required")
    if user.disabled:
        return

    send_email(user.email)
```

Avoid deep nesting for ordinary validation.
