## Fail-Closed

Any code that filters, permits, or gates defaults to deny. Access is granted only by an explicit, present, positive rule — never by the absence of a rule.

**Rules**:
- Present-but-empty means deny. An empty permission set, filter list, or role array grants nothing — never treat empty as "allow all".
- Absent means deny. "Absent → legacy, allow" is permitted only where the spec documents that exception explicitly.
- Missing declarations exclude. An item without a permission or type declaration is left out of results, not included by default.
- Unrecognized values are denied. A new or unknown enum variant is excluded, not passed through.
- Every gate states its posture in the spec: what happens when input is absent, empty, or unrecognized.

**Why**:
- A bug, a missing config, or an unhandled case fails toward *no access*, not *full access*.
- The dangerous default (fail-open) grants access silently; the safe default surfaces as a visible denial that gets reported and fixed.

---
