# Code Review Check Groups

> **Method**: Follow the review methodology in [REVIEW_METHOD.md](REVIEW_METHOD.md) before running these check groups.

Check groups for code PRs. Each group produces a PASS / FAIL / N/A.

### Code quality & best practices
- Does the code follow the language's idiomatic style and conventions?
- Are naming, structure, and patterns consistent with the rest of the codebase?
- Is the code readable and maintainable?
- Is the function size limited? Is the code logically divided (SRP)?

### Bugs & edge cases
- Are there potential bugs or unhandled edge cases?
- Are error paths handled (null/empty, overflow, missing data, exceptions)?
- Does the API leave the system in a half state on failure, or does it recover correctly?

### Performance & efficiency
- Are there unnecessary loops, repeated work, or redundant allocations?
- Are there N+1 queries, unnecessary re-renders, or blocking calls?
- Does the code use fail-early/preflight checks to reduce wasted CPU and memory?
- Could verbose logic be replaced with a clearer standard library call or idiom?
- When new data fetches are added, is the same data already available from a previous step in the call chain?

### Readability & complexity
- Is the code easy to follow, or is it overly complex (deep nesting, spaghetti)?
- Are there premature abstractions or over-engineered patterns that add indirection without value?
- Could overly complex code be simplified?

### Security
- Any hardcoded keys, secrets, or "test" passwords left in?
- Does the API validate and clean inputs?
- Any new attack surface (injection, XSS, CSRF)?

### Route safety (Next.js / file-based routers)
- Do new static route files sit alongside a `[param].ts` dynamic route in the same directory? If so, the dynamic route may shadow the static file — move static routes into a subdirectory (e.g. `actions/`) to avoid ambiguity.
- Are all fetch paths in frontend code consistent with the actual route file locations?

### Shims & dead indirection
- Are there re-export shims (file A just re-exports from file B) left behind after refactors? Consumers should import directly.
- Are there pass-through wrappers that add no logic — functions/classes that only delegate to another with the same signature?
- Are there barrel exports (`index.ts`) still exporting symbols that were moved or deleted? Remove stale entries.
- Are there empty interfaces, abstract classes, or type aliases that exist only for "backwards compatibility" with no remaining consumers?

### Optimizations & simplification
- Is there overly complex code that could be reduced?
- Could any section be simplified without losing correctness?
- Are there opportunities to reuse existing code instead of duplicating?

### Test quality
- Do test inputs match the actual function signatures?
- Do assertions match the actual return types and shapes?
- Are mocks/stubs compatible with real implementations?
- Can the test scenario actually be constructed? Trace `.unwrap()` / `.expect()` in setup through production validation — will setup steps succeed?
- Does the asserted error/value have a producer in the current codebase?

### Checklist
- Read `review/CHECKLIST.md` and walk through every item against the diff.
- For each checklist category, note PASS / FAIL / N/A.
- List any failures with `file:line` references.
