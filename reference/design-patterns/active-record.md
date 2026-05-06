# Active Record

Wrap a database row in a domain object that also handles its own load, save, and delete.

**Applies to**: Software Architecture

---

**What it is**: An object carries both data and the behaviour to persist itself. Each class maps to a table; each instance maps to a row. The object knows how to read and write itself.

**When to use**:
- Simple CRUD applications where domain logic is minimal.
- The domain model maps closely to the database schema.
- Development speed is more important than clean separation of concerns.

**Trade-offs**:
- Couples domain objects to the database — violates SRP and DIP.
- Hard to test without a real database.
- Does not scale well when domain logic becomes complex.
