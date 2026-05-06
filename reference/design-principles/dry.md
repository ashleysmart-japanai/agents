## DRY — Don't Repeat Yourself

Every piece of knowledge must have a single, unambiguous representation in the system. Duplication is not just copied code — it is copied logic, copied configuration, copied documentation. When the knowledge changes, every copy must change; miss one and the system is inconsistent.

**Applies to**: code, data schemas, configuration, documentation, test fixtures, and build scripts.

**Violation signals**: copy-paste with minor edits, parallel if-chains that mirror each other, the same constant defined in two places, tests that re-implement the logic they are testing.

**Fix**: extract to a single authoritative location and reference it everywhere. If two things look the same but change for different reasons, they are not duplicates — do not merge them (that would violate SRP).

---
