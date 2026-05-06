# Singleton Overuse

Using Singleton as a back door for global state — any code can reach the instance at any time, creating hidden dependencies throughout the system.

**Applies to**: Object-Oriented Design

---

**What it is**: Using Singleton as a back door for global state — any code can reach the instance at any time, creating hidden dependencies throughout the system.

**Why not**: Singletons accessed globally are untestable (state leaks between tests), create hidden coupling, and make call order implicit. Inject dependencies explicitly instead.
