# Long Parameter List

A function or constructor takes so many parameters that callers cannot reason about what each one does.

**Applies to**: Software Design

---

**What it is**: A function or constructor takes so many parameters that callers cannot reason about what each one does.

**Why not**: Signals a missing abstraction — the parameters likely belong in an object. Positional arguments are easy to swap silently. Makes the function hard to call, read, and test.
