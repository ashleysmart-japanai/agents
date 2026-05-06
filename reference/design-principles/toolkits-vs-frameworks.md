## Toolkits vs Frameworks

These represent opposite sides of the inversion of control boundary.

**Toolkit**: a library of components you call. You are in control of the program's structure and flow. You reach into the toolkit when you need it. Examples: a date library, an HTTP client, a JSON parser.

- You own `main`.
- You decide the architecture.
- You can adopt or drop individual pieces without restructuring.
- Testing does not require the toolkit to be running.

**Framework**: a skeleton that calls your code. You fill in the blanks the framework defines. The framework owns the program's flow. Examples: a web framework, an ORM, a test runner.

- The framework owns `main` (or its equivalent).
- It dictates the structure — where to put routes, handlers, models.
- Replacing it requires restructuring the application.
- Testing often requires the framework to be bootstrapped.

**Default to toolkits.** A toolkit gives you the capability without surrendering control. Reach for a framework only when its conventions solve a concrete, present structural problem that toolkit composition cannot address as simply.

**Choosing**:
- Use a toolkit unless there is a specific, concrete reason not to.
- A framework is acceptable when its conventions eliminate a class of
structural problems that would otherwise require significant bespoke scaffolding — and the lock-in cost is explicitly understood and accepted.
- Never adopt a framework speculatively (YAGNI). The switching cost is high
and grows with every line of code written against its API.
- If a framework is adopted, keep domain logic free of framework types and
base classes. Domain code must be importable and testable without bootstrapping the framework.
- If you find yourself fighting a framework — working around its
conventions, mocking its internals in tests, or bending your domain to fit its model — replace it with toolkits.

---
