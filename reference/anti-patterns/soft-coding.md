# Soft Coding

Making every decision configurable to avoid committing to anything — the opposite of magic numbers but equally harmful.

**Applies to**: Software Design

---

**What it is**: Making every decision configurable to avoid committing to anything — the opposite of magic numbers but equally harmful. Business logic is pushed into configuration files or databases.

**Why not**: The system's behaviour becomes invisible without reading the config. Errors are caught at runtime rather than compile time. Make decisions in code; configuration is for things that genuinely vary by deployment.
