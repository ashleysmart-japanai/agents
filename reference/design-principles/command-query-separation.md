## Command Query Separation (CQS)

A function either changes state or returns data — never both.

| Type | Does | Returns |
|------|------|---------|
| **Command** | Mutates state | Nothing (void / unit) |
| **Query** | Reads state | A value |

**Why**: a query can be called freely — it is safe to call multiple times, in any order, without side effects. A command changes the world. Mixing the two means a caller cannot read without risk and cannot trust that reading is free.

**Exception**: factory methods that construct and return a new object are acceptable. The exception is narrow and intentional — document it.

---
