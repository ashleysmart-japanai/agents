# Agent Guidelines

Rules and expectations for all AI agents working in this repository tree.
These guidelines apply to every project unless a project-level `Agents.md`
explicitly overrides a section.

---

## 1. Micro Spec Convention

> How to write specs: `@design/SPECS.md`

- Every non-trivial task begins with a micro spec written **before** any code.
- No code is written until the micro spec exists and is committed.
- The spec is the source of truth. If code diverges, update the spec first.
- Acceptance criteria drive the test plan — every criterion maps to at least one test.
- In markdown docs, do not manually hard-wrap prose lines; let the editor handle visual wrapping.

---

## 2. Unit Test Standard

> Full details: `@unittesting/GENERAL.md` | Pre-submit: `@unittesting/CHECKLIST.md`

- **Target**: 97% line coverage, 100% branch coverage on public interfaces
- **Cycle**: Red → Green → Refactor. Never write production code before seeing a red test.
- **Pattern**: AAA (Arrange, Act, Assert). One assertion per test. No shared mutable state.
- **Structure**: `tests/unit/` (every save), `tests/integration/` (on PR), `tests/e2e/` (on merge). Mirror source paths.
- **Deterministic**: no randomness, no wall-clock time, no network — stub at the boundary
- **CI gate**: coverage below 97% fails the PR
- **Automation**: unit tests, lints, and formatting are enforced by deterministic tools via CI and pre-commit hooks — never run manually or by the agent. If a check can be automated, it must be.

---

## 3. SOLID Design Principles

This project applies all five SOLID principles:

| Abbr | Full name | One-line rule |
|---|---|---|
| **SRP** | Single Responsibility | One reason to change per module, class, or function |
| **OCP** | Open / Closed | Open for extension, closed for modification |
| **LSP** | Liskov Substitution | Subtypes must be drop-in replacements for their base type |
| **ISP** | Interface Segregation | Many narrow interfaces over one wide one |
| **DIP** | Dependency Inversion | Depend on abstractions, not concretions |

Call the principle out by abbreviation in code review comments and micro
specs (e.g. "this violates SRP — split the parse and persist steps").

### SRP — Single Responsibility

A module, class, or function has exactly one reason to change. When a unit
does two things — parsing *and* persisting, validating *and* formatting —
split it. The name of each unit should make its single responsibility
obvious without needing to read the body.

### OCP — Open / Closed

New behaviour is added by extending the system, not by editing existing
code. Achieve this through composition, strategy objects, and well-defined
extension points. A change request that requires editing an existing class
body is a signal the abstraction boundary is in the wrong place.

### LSP — Liskov Substitution

Every subtype must honour the contract of its base type. A caller that holds
a reference to the base type must observe identical behaviour regardless of
which concrete subtype it receives. Violations: a subtype that throws where
the parent does not, returns a narrower type, or silently ignores a method.

### ISP — Interface Segregation

No implementor should be forced to define methods it does not use. Split
wide interfaces into focused ones. Clients depend only on the slice of the
interface they actually call.

### DIP — Dependency Inversion

High-level policy modules do not import low-level detail modules. Both
depend on a shared abstraction. Concrete implementations are injected at
the composition root — never constructed inside business logic.

---

## 4. Engineering Quality Standards

### Leverage compiler safety

In languages with strong type systems (TypeScript, Rust, Go, etc.), exploit
the compiler to catch bugs at build time rather than at runtime.

- **Use `as const` for literal types.** When a value must be a specific
  string or number (e.g. an ID in a discriminated union, a route name, an
  action type), assert it with `as const` so the compiler narrows the type
  to the literal rather than widening to `string`.
  ```typescript
  // Bad — id is typed as string, typos compile silently
  { id: "setting", label: t("settings") }

  // Good — id is the literal type "setting", mismatches are compile errors
  { id: "setting" as const, label: t("settings") }
  ```
- **Prefer const enums / union types over plain strings** for finite sets
  of values (action types, status codes, mode names).
- **Enable strict compiler flags** (`strict: true` in tsconfig,
  `-Wall -Werror` in C/C++, `clippy` in Rust). Never weaken them to fix
  a build — fix the code instead.
- **Let the type system replace runtime guards.** If a check can be
  expressed as a type constraint, do that instead of writing an `if` that
  throws at runtime.
- **Never use `any` unless absolutely necessary.** `any` disables type
  checking and defeats the purpose of a type system. Use `unknown` when
  the type is genuinely not known — it forces callers to narrow before use.
  If a third-party API returns `any`, wrap it and type the return at the
  boundary. The only acceptable uses of `any` are interop with untyped
  legacy code where a proper type is infeasible — and these must include a
  `// eslint-disable-next-line @typescript-eslint/no-explicit-any` comment
  explaining why.

### Code style

- Follow the language's idiomatic style guide.
- Maximum function length: **30 lines** of logic (excluding blank lines and
  comments). If longer, extract a helper with a clear name.
- Maximum file length: **400 lines**. Larger files signal more than one
  concept in the file.
- No commented-out code committed. Use version control instead.

### Naming

- Names are pronounceable, unambiguous, and domain-specific.
- No abbreviations unless universally understood in the domain.
- Boolean names start with `is_`, `has_`, `can_`, or `should_`.

### Error handling

- Never silently swallow exceptions. Log and re-raise, or convert to a
  typed domain error with context.
- Every public function that can fail has a documented failure contract.
- Errors are typed — avoid bare catch-all error types.

### Dependencies

- No new dependency is added without a note in the micro spec justifying it.
- Prefer standard library over third-party where the effort is comparable.
- Pin all dependency versions; no floating version ranges in lock files.

### Git hygiene

- Commits are atomic: one logical change per commit.
- Commit message format:
  ```
  <type>: <imperative short summary>

  <body — why, not what; optional>
  ```
  Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`.
- No merge commits on feature branches; rebase onto main before merging.
- **Do not squash** unless explicitly instructed. A squash is a one-time
  operation — after completing it, return to pushing incremental commits.
  Do not squash on every subsequent fix after an authorised squash.
- Branch names: `<type>/<short-slug>`.

### Pull / merge requests

- PR description links to the micro spec doc.
- Checklist before requesting review:
  - [ ] All acceptance criteria from the micro spec are met.
  - [ ] Coverage gate passes locally.
  - [ ] No new lint warnings introduced.
  - [ ] Micro spec updated if scope changed during implementation.
  - [ ] CHANGELOG entry added for user-visible changes.

---

## 5. Agent Workflow

When an AI agent picks up a task it **must** follow this order:

1. **Read** the relevant micro spec (or create one if absent).
2. **Read** existing code in the affected area before writing anything.
3. **Write or update** the micro spec if the task is new or scope changes.
4. **Red** — write one test, run the suite, confirm that test fails for the
   right reason. A test that cannot be seen to fail proves nothing.
5. **Green** — write the minimum production code needed to make that test
   pass. No more.
6. **Repeat** steps 4–5 for each acceptance criterion in the micro spec.
7. **Refactor** — with all tests green, clean names, split large functions,
   remove duplication. Run the suite after every refactor step.
8. **Commit** in atomic commits following the git hygiene rules above.
9. **Push** to the PR branch after each completed change. Do not batch up
   commits — push proactively so the PR stays up to date.
10. **Do not merge** PRs. Merging is done by the user. Do not expect to be
    involved in the merge process.
11. **Do not deploy** unless the user explicitly says so.

An agent must stop and surface an open question rather than guess when:
- A spec section is ambiguous.
- An interface from another module is missing or contradicts the spec.
- The 97 % coverage target cannot be reached without unreasonable stubbing.

---

## 6. What Agents Must Never Do

### Scope creep — the hardest rule

An agent works only on what was explicitly asked for. When in doubt, do less
and ask. Violations erode trust and create hidden regressions.

- **Do not add features** that were not in the current task or micro spec,
  even if they seem obviously useful.
- **Do not refactor code** outside the files directly touched by the task.
- **Do not rename** symbols, files, or directories unless renaming is the
  explicit task.
- **Do not add logging, metrics, or instrumentation** beyond what the spec
  requires.
- **Do not add comments or documentation** to code that was not part of the
  change, even to "improve" it.
- **Do not change formatting** in lines that were not otherwise modified.

---

## 7. Skills

- `squash-rebase`: `~/agents/skills/SQUASH_REBASE.md`
- `/squash-rebase`: `~/agents/skills/SQUASH_REBASE.md`
- `rebase-squash`: `~/agents/skills/SQUASH_REBASE.md`
- `/rebase-squash`: `~/agents/skills/SQUASH_REBASE.md`
- `clean-check`: `~/agents/skills/CLEAN_CHECKS.md`
- `/clean-check`: `~/agents/skills/CLEAN_CHECKS.md`
- `update-main`: `~/agents/skills/MAIN_UPDATE.md`
- `/update-main`: `~/agents/skills/MAIN_UPDATE.md`
