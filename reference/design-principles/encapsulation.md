## Encapsulation

Hide internal implementation. Expose only what consumers need.

**Rules**:
- Fields are private by default. Expose a field only when there is a
concrete reason for a consumer to read or write it.
- Expose behaviour, not data. A consumer should tell an object what to do,
not extract its data and act on it externally (tell, don't ask).
- Internal representation can change freely as long as the public interface
stays stable.
- Avoid exposing collection internals — return an immutable view or a copy,
not a reference to the internal collection.

**Violation signals**: public fields on domain objects; getters and setters for every field (a data class pretending to be an object); logic that belongs inside an object living in its caller instead.

---
