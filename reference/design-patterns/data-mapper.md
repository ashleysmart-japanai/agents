# Data Mapper

Map between domain objects and database rows without coupling either side to the other.

**Applies to**: Software Architecture

---

**What it is**: A layer of mappers that moves data between objects and a database while keeping them independent of each other. Neither the domain object nor the database schema knows about the other.

**When to use**:
- Domain objects and database schema differ significantly.
- Domain objects should have no knowledge of persistence.
- The database schema may change independently of the domain model.

**Trade-offs**:
- More complex to implement than Active Record.
- Requires maintaining the mapper layer alongside both domain and schema changes.
