# Agent Guidelines

Rules and expectations for all AI agents working in this repository tree. These guidelines apply to every project unless a project-level `Agents.md` explicitly overrides a section.

---

## 1. Micro Spec Convention

> How to write specs: `@design/SPECS.md`

- Every non-trivial task begins with a micro spec written **before** any code.
- No code is written until the micro spec exists and is committed.
- Spec is the source of truth. Code to its intended target — do not rewrite it to match the code.
- Resolve gaps by size:
  - **In-scope gap** → apply conventions, record the assumption, continue. Never ask.
  - **Ambiguous** (conventions conflict or none applies) → ask.
  - **Small drift** (naming, local structure) → update spec, continue.
  - **Large divergence** (new approach, changed contract, added/dropped requirement) → stop and ask. Do not self-approve by editing the spec.
  - Unsure if large → treat as large, ask.
- Fill in-scope gaps with the established conventions:
  - Security → [security-principles](reference/security-principles.md):
    - Fail-closed — deny on absent/empty/unknown.
    - Secure by query — the query is the gate, not fetch-and-filter.
    - Least privilege — narrowest scope that works.
  - Design → SOLID + [design-principles](reference/design-principles.md) + [design-patterns](reference/design-patterns.md):
    - One responsibility.
    - One owner per contract.
    - No speculative abstraction.
  - Standards → §4 + [`CONVENTIONS.md`](CONVENTIONS.md) + [`style/`](style/) (per-language):
    - Enums for closed sets.
    - No primitive obsession.
- Then check the result against [`reference/anti-patterns.md`](reference/anti-patterns.md):
  - The *negative* set — things to avoid, not conventions to apply.
  - E.g. gold plating, primitive obsession, smuggler.
- Acceptance criteria drive the test plan — every criterion maps to at least one test.
- In markdown docs, do not manually hard-wrap prose lines.

### Negative example — inventing a requirement

- **Task:** read table `records` via credential `C`, scoped by org. One credential is the data boundary; one preflight check is the gate.
- **Failure:** agent added a per-row permission check nobody asked for — access predicate, batch checker, post-fetch filter — a permission tier with no credential, no ACL column, no way to configure it.
- Adding a per-row gate is a *new access model*, not an in-scope gap → was a large divergence → stop and ask.
- Fail-closed hardens the *one* defined gate; it never means invent a second gate → the per-row layer is [Gold Plating](reference/anti-patterns/gold-plating.md) + a §4 C6 violation (no consumer).
- Post-fetch filtering is fetch-then-check — the anti-pattern the single query gate already avoided.
- When flagged, the agent defended the layer and pushed to spread it "for consistency" instead of deleting it.
- The unrequested machinery dwarfed the actual task.
- **Tell:** adding a check/credential/gate the spec never named — per row, per field, per call — is a large divergence, not a gap. Stop and ask.
- **Rule:** if your defense of a layer is your own reasoning, not a spec line, delete it — do not defend it.

---

## 2. Unit Test Standard

> Full details: `@unittesting/GENERAL.md` | Pre-submit: `@unittesting/CHECKLIST.md`

- **Target**: 97% line coverage, 100% branch coverage on public interfaces
- **Cycle**: Red → Green → Refactor. Never write production code before seeing a red test.
- **Red means committed red**: the failing test is added to the real suite and committed *while it fails*, before any production-code change. A "temporary" test that is run once and never committed is not a red light — it is fabricated evidence. The commit history must show the red-test commit preceding the fix commit. When pre-commit hooks require a green suite, commit the red state via an expected-failure marker (§5 step 6) — the marker proves the failure without breaking the hook.
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

Call the principle out by abbreviation in review comments and specs (e.g. "this violates SRP — split the parse and persist steps").

### SRP — Single Responsibility

- One reason to change per module, class, or function.
- A unit doing two things — parse *and* persist, validate *and* format — is split.
- The name states the single responsibility; you should not need to read the body.

### OCP — Open / Closed

- Add behaviour by extending, not by editing existing code.
- Achieve it with composition, strategy objects, and defined extension points.
- Needing to edit an existing class body signals the abstraction boundary is wrong.

### LSP — Liskov Substitution

- Every subtype honours its base type's contract.
- A caller holding the base type observes identical behaviour for any subtype.
- Violations: a subtype that throws where the parent does not, returns a narrower type, or silently ignores a method.

### ISP — Interface Segregation

- No implementor defines methods it does not use.
- Split wide interfaces into focused ones.
- Clients depend only on the slice they call.

### DIP — Dependency Inversion

- High-level policy modules do not import low-level detail modules.
- Both depend on a shared abstraction.
- Concrete implementations are injected at the composition root — never constructed inside business logic.

---

## 4. Engineering Quality Standards

### Leverage compiler safety

- In strongly-typed languages (TypeScript, Rust, Go, etc.), exploit the compiler to catch bugs at build time, not runtime.
- **Use `as const` for literal types.** When a value must be a specific string or number (e.g. an ID in a discriminated union, a route name, an action type), assert it with `as const` so the compiler narrows the type to the literal rather than widening to `string`.
  ```typescript
  // Bad — id is typed as string, typos compile silently
  { id: "setting", label: t("settings") }

  // Good — id is the literal type "setting", mismatches are compile errors
  { id: "setting" as const, label: t("settings") }
  ```
- **Prefer const enums / union types over plain strings** for finite sets of values (action types, status codes, mode names).
- **Enable strict compiler flags** (`strict: true` in tsconfig, `-Wall -Werror` in C/C++, `clippy` in Rust). Never weaken them to fix a build — fix the code instead.
- **Let the type system replace runtime guards.** If a check can be expressed as a type constraint, do that instead of writing an `if` that throws at runtime.
- **Never use `any` unless absolutely necessary.** `any` disables type checking and defeats the purpose of a type system. Use `unknown` when the type is genuinely not known — it forces callers to narrow before use. If a third-party API returns `any`, wrap it and type the return at the boundary. The only acceptable uses of `any` are interop with untyped legacy code where a proper type is infeasible — and these must include a `// eslint-disable-next-line @typescript-eslint/no-explicit-any` comment explaining why.

### Fail-closed defaults

- Any code that filters, permits, or gates defaults to deny.
- **Present-but-empty means deny.** An empty permission set, an empty filter list, or an empty role array grants nothing — never treat empty the same as absent.
- **Absent may mean "legacy, allow" only if the spec documents it.** If there is no documented legacy exception, absent also means deny.
- **Missing declarations exclude.** An item without a permission or type declaration is excluded from results, not included by default.
- **State the posture in the spec.** Every gate or filter in a micro spec must say what happens when input is absent, empty, or unrecognized.

### Booleans over string arrays for fixed permission sets

- Closed, compile-time-known permission sets are a record of booleans (`{ read: true, write: false }`), not a string array (`["read"]`).
- Booleans cannot be misspelled, are self-documenting, and the compiler catches missing keys.

### No metadata in data namespaces

- System fields (timestamps, version markers, internal IDs) never share a namespace with user-supplied data.
- System fields live under a single reserved envelope key, written after user data so they cannot be shadowed.
- The reserved key is stripped from user input at the boundary.

### Cursor pagination, not offset pagination

- All paginated endpoints and list queries use cursor-based pagination keyed on a stable record ID — never offset/page-number.
- Offset pagination breaks under concurrent writes (skipped/duplicated rows) and degrades at depth (`OFFSET 10000` scans and discards 10,000 rows).
- The cursor is an opaque token derived from the last record's ID (or a composite key when sort order requires it).
- Response shape: `{ items, nextCursor, hasMore }`. No `page`, `totalPages`, or `offset` fields.
- The underlying query uses a `WHERE id > :cursor ORDER BY id LIMIT :size` pattern (or equivalent for the ORM/database).
- If a UI needs a page-number display, the frontend synthesises it from cursor state — the API never exposes offset semantics.

### No compatibility shims for internal code

- No backwards-compatibility wrappers, re-exports, or adapter layers for internal callers.
- When an internal interface changes, update every caller.
- Compat shims are only justified at published public API boundaries.

### Code style

- Follow the language's idiomatic style guide.
- Maximum function length: **30 lines** of logic (excluding blank lines and comments). If longer, extract a helper with a clear name.
- Maximum file length: **400 lines**. Larger files signal more than one concept in the file.
- No commented-out code committed. Use version control instead.

### Naming

- Names are pronounceable, unambiguous, and domain-specific.
- No abbreviations unless universally understood in the domain.
- Boolean names start with `is_`, `has_`, `can_`, or `should_`.

### Error handling

- Never silently swallow exceptions. Log and re-raise, or convert to a typed domain error with context.
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

  <body — why, not what; optional, max 3 lines>
  ```
  Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`.
- **Keep commit messages terse.** The summary line is under 72 characters. The body, if present, is 1–3 lines explaining *why* — not a changelog, not a list of every file touched, not a paragraph restating the diff. If the diff is self-explanatory, the body is omitted entirely.
- No merge commits on feature branches; rebase onto main before merging.
- **Do not squash** unless explicitly instructed. A squash is a one-time operation — after completing it, return to pushing incremental commits. Do not squash on every subsequent fix after an authorised squash.
- Branch names: `<type>/<short-slug>`.

### Pull / merge requests

- PR description links to the micro spec doc.
- Checklist before requesting review:
  - [ ] All acceptance criteria from the micro spec are met.
  - [ ] Coverage gate passes locally.
  - [ ] No new lint warnings introduced.
  - [ ] Micro spec updated if scope changed during implementation. Any large divergence from the spec's intent was raised with the user and approved before proceeding — not self-approved by editing the spec (see §1).
  - [ ] CHANGELOG entry added for user-visible changes.

---

## 5. Agent Workflow

- An agent picking up a task **must** follow this order.
- Every gate demands an artifact — instructions that produce nothing get skipped; instructions whose absence is visible cannot.
- No agent claims work complete until every applicable gate has a recorded artifact.

### Before code

1. **Read the bug report or task fully.** If the task references a review issue, read the entire `<ID>.md` detail file — description, evidence, fix guidance, and reverify steps. Do not skim summaries or titles. Do not make decisions, push back, or categorise an issue without reading the full detail file first.
2. **Read** the relevant micro spec (or create one if absent).
3. **Read** existing code in the affected area before writing anything.
4. **Write or update** the micro spec if the task is new or scope changes.

**Process gates — stop here until all pass:**

| # | Gate | Evidence |
|---|------|----------|
| P1 | **Spec-with-matrix exists.** For any feature that filters, permits, gates, or falls back: the spec contains the full input-state × behavior table — with absent and present-but-empty as separate rows — and no cell reads TBD. | The table in the spec doc, committed before implementation. |
| P2 | **Acceptance criteria are executable.** Every AC names a test file/case that fails before implementation and passes after. Prose-only ACs are invalid. | Red run before, green run after — both captured, and the red test is a committed suite file (commit sha), not a temporary/uncommitted file. |
| P3 | **Design is checked against the anti-pattern catalog before coding.** Named check of `anti-patterns/CHECKLIST.md` sections relevant to the design (smuggler for any new field on shared objects, primitive-obsession for any new string, boat-anchor for anything speculative). | Pass/fail/N-A list in the spec. |

### During implementation

5. **Red** — write one test in the real suite (committed file paths, not scratch/temp files), run the suite, confirm that test fails for the right reason, and **commit the failing test** with its raw red output referenced in the commit message. A test that cannot be seen to fail proves nothing; a red run with no committed test is unverifiable and does not count.
6. **Green** — write the minimum production code needed to make that test pass. No more. The fix is a separate commit after the red-test commit, so history proves the test failed before the code changed.
   - If the pre-commit hook runs the suite (the normal case — see §2 Automation), commit the red test under the framework's **expected-failure marker** (`test.failing` Jest, `test.fails` Vitest, `@pytest.mark.xfail(strict=True)` pytest) with the full issue ID in the test description. The marker passes only while the test fails, so the hook stays green and the red state is machine-proven. The fix commit flips the marker to a normal test in the same commit as the code change.
   - Never use `--no-verify` and never skip the red commit. If the framework has no expected-failure mechanism, stop and surface it to the user.
7. **Repeat** steps 5–6 for each acceptance criterion in the micro spec.
8. **Refactor** — with all tests green, clean names, split large functions, remove duplication. Run the suite after every refactor step.

**Code gates — every new or changed symbol must satisfy all that apply:**

| # | Gate | Evidence |
|---|------|----------|
| C1 | **Fail closed, stated explicitly.** Every gate declares its posture in the spec: absent → documented compat or deny; empty → deny; undeclared item → excluded. Fail-open requires a written justification. | Posture declaration in the spec for every gate. |
| C2 | **No closed set as a raw string.** Every finite value set is a named union/enum at every layer it crosses. | `grep` new fields for bare `string` types — zero hits. |
| C3 | **Invalid states unrepresentable.** Flags are booleans, not membership arrays; domain types over primitives. `{ read: true }` cannot typo; `["raed"]` can. | Type definitions in the diff use records/enums, not string arrays. |
| C4 | **System metadata never shares a namespace with user data.** One reserved envelope key, written after user data, stripped from user input at the boundary. | Smuggler checklist against the diff. |
| C5 | **One owner per contract.** A type crossing N boundaries is declared once and imported, or each copy carries a `KEEP-IN-SYNC` reference to the master, and a test pins the wire shape. | Single declaration site, or `KEEP-IN-SYNC` references plus a shape-pinning test. |
| C6 | **Only functional code.** No field, param, shim, or fallback without a current consumer named in the spec. Reviewer suggestions are proposals — they get scope-checked against objectives, not implemented by default. | Every new symbol has a caller in the diff; spec lists no unused additions. |

### Before commit

**Truth gates — claims in the diff must match the code:**

| # | Gate | Evidence |
|---|------|----------|
| T1 | **Every prose claim is verified in the same pass that touches the behavior.** Comments, docblocks, test names, spec assertions — if the claim describes behavior, either point it at a test or re-verify it when the behavior changes. A claim that cannot be checked gets deleted. | No reviewer-bait items survive the diff review. |
| T2 | **Report failures verbatim.** Failing tests, skipped steps, and unverified paths are stated plainly, never smoothed over. | Raw output included — no editorialised summaries of failures. |

9. **Commit** in atomic commits following the git hygiene rules above.

### Before push / claiming complete

**Submission gates — no push until all pass:**

| # | Gate | Evidence |
|---|------|----------|
| S1 | **The published checklists actually execute, with artifacts.** `~/agents/review/REVIEW_METHOD.md` every PR; `~/agents/review/SECURITY_REVIEW.md` check groups whenever the diff touches APIs/auth/credentials; `~/agents/reference/anti-patterns/CHECKLIST.md` against the diff. Each produces a filled item → pass/fail/N-A → `file:line` record. No artifact = didn't happen. | Checklist output files with `file:line` evidence for every item. |
| S2 | **Findings map to objectives before they map to fixes.** Every review finding is classified on-objective / robustness-layer / out-of-scope before any code is written; robustness layers default to rejected pending user decision. | Classification tag on each finding before implementation begins. |
| S3 | **Fresh state before verdicts.** Reviews and fixes run against the current HEAD after fetch — never against a stale checkout. | `git fetch` + `HEAD` SHA recorded before each review or fix pass. |

### Reporting findings

- Report bugs, issues, and findings **to the user in chat** using the finding grammar in [`~/agents/review/REVIEW_METHOD.md` § Finding Grammar](review/REVIEW_METHOD.md#finding-grammar): one line per finding, `- [<x| >] <ID> - <STATUS> [<SEVERITY>] - <title> \`file:line\``.
- Use the status tokens only (`OPEN`, `NEEDS_REVIEW:coder`, `CLOSED verified:<yyyy-mm-dd>`, …). **Never** describe a finding with a loose adjective like "present", "resolved", "done", or "handled".
- A fix that is written but not yet verified is `OPEN`, not `CLOSED verified:` — "verified" requires a passing reverify command, test, or trace, not merely that the code is present.
- Do **not** write to `review.md` or the `~/reviews/<repo>-pr-<number>/` directory. That persisted store is the reviewer/orchestrator's job (see `~/agents/review/ISSUE_TRACKING.md`). Your report is the in-chat list.
  - **One exception:** the review-claim triage and red-light procedure below. When executing it, the coder records and updates the claims it is processing in the review store per ISSUE_TRACKING.md.

### Review-claim triage and red-light (mandatory after any review)

Run this for every claim a review produces — self-review, reviewer findings, PR comments, feedback ingress. A review claim is **unproven** until a committed red test demonstrates it. Process each claim in order; the first failing gate ends that claim's processing.

1. **Record** the claim in the review store per `~/agents/review/ISSUE_TRACKING.md`: full ID (`<prefix><n>.<SID>`), status `OPEN`, detail field `redlight:pending`. Unproven-but-started is the recorded state — never triage a claim that isn't written down first.
2. **Scope-check against the micro-spec.** If the claim is not in scope for the micro-spec, mark it `OUT_OF_SCOPE` with `scope:micro-spec - <reason>`.
3. **Design-check against `steering.md`.** If the claim conflicts with the system design requirements in the repo's `steering.md`, mark it `OUT_OF_SCOPE` with `scope:steering - <reason>`.
4. **Creep-check.** If fixing the claim requires changes beyond the files already changed on the branch, mark it `OUT_OF_SCOPE` with `scope:scope-creep - <files it would pull in>`.
5. **Documentation nits:** correct the documentation *only if* the correction does not change the design stated in the micro-spec or `steering.md`. If it would, mark `NEEDS_REVIEW:coder` and explain the design conflict in the detail file. Doc-only fixes skip red-light — record `redlight:n/a-docs`.
6. **Red-light the claim.** Add a test to the real suite that proves the claimed defect and **commit it in its failing state** — the red commit is the proof of work. When hooks require a green suite, commit it under the expected-failure marker (§5 step 6). Record `redlight:<sha> <file:case>` in the detail file. If no test can be made to fail from the claim, mark it `UNPROVEN`, keep the attempted probe and its passing output in the detail file, and do not write a fix.
7. **Fix.** Change production code only to correct the proven issue. Never edit the red test to make it pass — hacking the test voids the proof and is fabricated evidence (T2).
8. **Micro-review the fix diff** before committing. Check it for:
   - anti-patterns (`~/agents/reference/anti-patterns/CHECKLIST.md`)
   - security issues (security check groups when the diff touches APIs/auth/credentials)
   - failure to follow `steering.md` / micro-spec requirements
   - failure to meet the micro-spec acceptance criteria
9. **Failure path.** If the fix does not turn the red test green, or the micro-review surfaces cascade claims against it, mark the issue `NEEDS_REVIEW:coder`, revert the production change, and document the problem plus the proposed correct code in the detail file. The red test stays committed — return it to its expected-failure marker (§5 step 6) so the suite stays green; never delete it.
10. **Commit** the verified fix as its own commit after the red commit, then update the issue to `CLOSED verified:<yyyy-mm-dd>` with both shas.

10. **Push** to the PR branch after each completed change. Do not batch up commits — push proactively so the PR stays up to date.
11. **Do not merge** PRs. Merging is done by the user. Do not expect to be involved in the merge process.
12. **Do not deploy** unless the user explicitly says so.

An agent must stop and surface an open question rather than guess when:
- A spec section is ambiguous.
- An interface from another module is missing or contradicts the spec.
- The 97 % coverage target cannot be reached without unreasonable stubbing.

---

## 6. What Agents Must Never Do

### No stashes — commit instead

- **Never use `git stash`.** WIP is committed to its branch (`wip:` prefix is fine) — commits are visible, attributable, durable, and pushable; stashes are none of those.
- A stash blocks history rewrites (squash-rebase fail-closes on stashes), survives invisibly across sessions, and loses its branch context.
- Found an existing stash? Do not apply, drop, or pop it silently — surface it, then preserve it as a commit on a branch (`git stash branch`) with the user's approval.

### No phantom tests — red evidence is committed evidence

- **Never fake the red light with a temporary test.** A test written in a scratch file, run once, and deleted, reverted, or left uncommitted is not red-light evidence — it is untraceable and unverifiable, and claiming it as a red run is a false completion claim (violates T2).
- Every red test lands in the real suite and is committed while failing, before the fix commit (§2, §5 step 5).
- This applies to red-lighting review findings, not just new features: the probe that proves a bug **is** the regression test for its fix. Commit it red, keep it in the suite, let the fix turn it green. "Temporary probes, since reverted" means the findings have no evidence and the fixes will have no regression guard.
- A red-light results table (🔴 verdicts) is only valid if every RED row cites a committed test `file:case` and its commit sha. If running the suite right now shows no failures, nothing is red-lighted — reporting it as confirmed is fabricated evidence.
- If a test used to prove a bug turns out not to belong in the suite, that decision is the user's — surface it, do not silently delete it.

### No side workspaces — work on the PR branch

- All code changes happen on the PR branch checkout. **Never** apply fixes in a separate clone, worktree, or "review workspace".
- A patch that exists only in a side workspace does not exist: it is unverifiable by others, not on the PR, and will be lost. Reporting such a patch as "addressed" is a false completion claim (violates T2).
- Reviewers propose; the fix lands on the branch via the normal red → green → commit → push cycle (§5), or it is reported as an OPEN finding — never as done.

### Scope creep — the hardest rule

- An agent works only on what was explicitly asked for. When in doubt, do less and ask.
- Violations erode trust and create hidden regressions.
- **Do not add features** that were not in the current task or micro spec, even if they seem obviously useful.
- **Do not refactor code** outside the files directly touched by the task.
- **Do not rename** symbols, files, or directories unless renaming is the explicit task.
- **Do not add logging, metrics, or instrumentation** beyond what the spec requires.
- **Do not add comments or documentation** to code that was not part of the change, even to "improve" it.
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
