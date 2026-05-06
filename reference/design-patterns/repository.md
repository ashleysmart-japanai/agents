# Repository

Abstract persistence behind a collection-like interface; domain does not know about storage.

**Applies to**: Software Architecture

---

**What it is**: Mediates between the domain and data mapping layers. The domain sees a collection of objects; the repository handles all query and persistence logic behind that interface.

**When to use**:
- Domain logic should be independent of how data is stored or queried.
- Multiple storage backends may be needed (database, in-memory, cache).
- Unit testing domain logic without a real database.

**Trade-offs**:
- Can become a leaky abstraction if domain queries are too storage-specific.
- Generic repositories can push query logic into the domain or service layer.
