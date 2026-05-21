# Testing Standards

## Automation First

Unit tests, lints, and formatting are enforced by deterministic tools via CI and pre-commit hooks — never run manually or by the agent. If a check can be automated, it must be. Human and agent review is for judgment calls that tools cannot make.

## Coverage Target

**97% line coverage, 100% branch coverage on public interfaces.**

- Verify coverage on new code before submitting
- If a line is intentionally uncoverable (e.g., defensive fallback that can't be triggered), add a brief comment explaining why
- CI must fail if coverage drops below 97% on any PR touching production code
- See `@tooling/TOOLING.md` / `@tooling/TOOLING_<lang>.md` for per-language coverage commands

### What is explicitly excluded from the 97% target

- Auto-generated code — mark with the project's coverage-skip mechanism
- Third-party adapters that are thin pass-throughs with no logic
- Entry-point bootstrapping that wires the dependency graph

Exclusions must be listed in the micro spec under *Scope > Out of scope*.

## What Must Be Tested

- Every public function / method / endpoint
- Every error path listed in the micro spec's *Error cases* section
- Every boundary value (zero, one, max, overflow where relevant)
- Every state transition if the module is stateful
- Happy path
- Error cases (invalid input, null/empty, missing data, thrown exceptions)
- Side effects (was the notification sent? was the log written?)

## What NOT to Test

- Third-party library internals
- Simple type definitions or constants
- Code you did not change (unless your change affects its behavior)

## Test Structure

```
tests/
  unit/         # fast, no I/O, no network — run on every save
  integration/  # real DB / filesystem, use fixtures — run on PR
  e2e/          # full stack — run on merge to main
```

Each test file mirrors its source file in path and name.

## Red / Green / Refactor Cycle

Each acceptance criterion from the micro spec is implemented through exactly
one cycle:

1. **Red** — write the test, run the suite, read the failure output.
   The failure must be an assertion failure against the behaviour under test,
   not a setup or import error. Fix setup issues until the failure is clean,
   then stop.
2. **Green** — write the smallest production change that turns that test
   green. Run the full suite to confirm no regressions.
3. **Refactor** — improve the code while the suite stays green.

An agent must never write production code before observing a red failure.
Skipping the red step invalidates the test as a safety net.

## Test Anatomy (AAA)

```
test <behaviour>_<condition>_<expected outcome>:
    // Arrange
    set up inputs and dependencies

    // Act
    result = call the unit under test

    // Assert
    verify result matches expectation
```

- Follow the AAA pattern: Arrange, Act, Assert
- One logical assertion per test
- Tests are deterministic: no randomness, no wall-clock time, no network —
  inject or stub these at the boundary
- Tests never share mutable state across test functions

## Mocking

- Mock external dependencies (DB, APIs, Pub/Sub) — do not mock the unit under test
- See `@tooling/TOOLING.md` / `@tooling/TOOLING_<lang>.md` for test file conventions, runners, and coverage commands per language

## Running Tests

Use the narrowest scope that gives confidence. See `@tooling/TOOLING.md` / `@tooling/TOOLING_<lang>.md` for per-language commands.

## Linting, Formatting, and Type Checking

See `@tooling/TOOLING.md` / `@tooling/TOOLING_<lang>.md` for language-specific lint, format, and typecheck commands.

- Lint all changed code before submitting. Fix all errors and warnings — do not suppress or disable rules without justification.
- Auto-format code to keep syntax in standard form. Group and sort includes/imports where sane:
    - Imports should not randomly change in git diffs
    - Imports should not make code build via a transitive include
