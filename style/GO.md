# Go Standards

## For Loops

Use `range` for slices, maps, and channels. Ignore unused values with `_`.

```go
for _, user := range users {
	ActivateUser(user)
}

for i, user := range users {
	LogUser(i, user)
}
```

Use a three-part `for` only when controlling index arithmetic.

## Enums

Use a named type plus constants. Do not compare raw strings or magic numbers inline.

```go
type CapabilityMode string

const (
	CapabilityNone     CapabilityMode = "none"
	CapabilityOptional CapabilityMode = "optional"
	CapabilityRequired CapabilityMode = "required"
)

if mode == CapabilityRequired {
	EnableCapability()
}
```

Use `iota` only for internal numeric states where serialized values do not matter.

```go
type JobState int

const (
	JobQueued JobState = iota
	JobRunning
	JobDone
)
```

## Switches

Use `switch` for one discriminant with several known cases. Return from cases when possible.

```go
func LabelMode(mode CapabilityMode) (string, error) {
	switch mode {
	case CapabilityNone:
		return "Disabled", nil
	case CapabilityOptional:
		return "Optional", nil
	case CapabilityRequired:
		return "Required", nil
	default:
		return "", fmt.Errorf("unknown capability mode: %s", mode)
	}
}
```

Use `if` for ranges, compound conditions, or predicates.

## Fail Early

Return errors and empty cases first. Keep the normal path unindented.

```go
func SendInvite(user User) error {
	if user.Email == "" {
		return fmt.Errorf("email is required")
	}
	if user.Disabled {
		return nil
	}

	return SendEmail(user.Email)
}
```

Avoid deep nesting for ordinary validation.
