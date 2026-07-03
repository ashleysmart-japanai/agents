# C++ Standards

## For Loops

Prefer range-for when iterating values. Use indices only when index arithmetic is required.

```cpp
for (const User& user : users) {
  ActivateUser(user);
}

for (std::size_t i = 0; i < users.size(); ++i) {
  LogUser(i, users[i]);
}
```

## Enums

Use scoped enums. Do not use raw integers or unscoped enum values for domain states.

```cpp
enum class CapabilityMode {
  kNone,
  kOptional,
  kRequired,
};

if (mode == CapabilityMode::kRequired) {
  EnableCapability();
}
```

Use named `constexpr` constants for numeric domain values.

```cpp
constexpr int kMaxRetries = 3;
```

## Switches

Use `switch` for one enum or integral discriminant with several known cases. Keep cases short.

```cpp
std::string LabelMode(CapabilityMode mode) {
  switch (mode) {
    case CapabilityMode::kNone:
      return "Disabled";
    case CapabilityMode::kOptional:
      return "Optional";
    case CapabilityMode::kRequired:
      return "Required";
  }

  throw std::logic_error("unknown capability mode");
}
```

Use `if` for ranges, compound conditions, or predicates.

## Fail Early

Validate preconditions first. Keep the normal path unindented.

```cpp
void SendInvite(const User& user) {
  if (user.email.empty()) {
    throw std::invalid_argument("email is required");
  }
  if (user.disabled) {
    return;
  }

  SendEmail(user.email);
}
```

Avoid deep nesting for ordinary validation.
