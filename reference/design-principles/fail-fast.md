## Fail-Fast

Detect and surface problems at the earliest possible point. Do not allow invalid state to propagate deeper into the system where it is harder to trace and more expensive to fix.

**Rules**:
- Validate inputs at the boundary — the moment data enters the system.
- Raise an error immediately on invalid state; do not carry it forward with
a sentinel value.
- Do not write defensive checks deep inside business logic for conditions
that should have been caught at the entry point.
- An assertion that fires early is better than a corrupted database record
discovered later.

---
