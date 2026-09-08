# Agent Specs — reading the spec, writing the tasking file

Agent rules for the two spec documents. The human spec's authoritative convention is the project's own spec guide; this document states what the agent expects to find in it, what the agent checks (`/check-spec`), and what the agent writes in the tasking file.

## Objective

- Capture the design requirements and goals.
- Capture the acceptance requirements.
- The spec is where the problem is thought through before building — not a task brief for an agent.
  - It states what is being solved, what is assumed, where the boundary is, and how success is measured.
  - It names the alternatives considered and why they were not chosen.
- Write in dot-point-srp style (`~/agents/style/DOT_POINT_SRP.md`): one terse clause per line, sub-clauses indented into a sub-list.
- The spec is **not** a code-in-text-form document.
  - It does not perfectly represent the exact code that is written.
  - It documents the objective of the happy path.
  - It documents the main exceptions to the happy path in a generalized way.
- Use function and class names, not hand-waving terms, to discuss target code.
- Statements follow SOLID (`~/agents/style/DOT_POINT_SRP.md` § SOLID statements); open/closed is the rule agent specs most often break.
  - Each requirement, design line, and acceptance criterion states what this change adds or does.
  - It does not enumerate the module's full set of behaviours — that inventory goes stale when parallel work lands on the same module.
  - GOOD: "`RecordAdapter` will add `browse(cursor)`".
  - BAD: "`RecordAdapter` has `create`, `browse`".
- Use durable references.
  - Do not use line numbers — they go stale.
  - Use full repo paths for filenames.

## Whether and which spec

- Blast radius decides whether: one file, no new interface, no cross-module impact, no team decision → no spec; fix it and open the PR.
- Touches core, the data model, or more than one service → a spec, read end to end and explicitly reviewed before work starts.
- Kind and complexity decide the tier; hours are a proxy, not the line.
  - Micro spec: bug fixes, docs, and config changes — under a day.
  - Quick spec: a small feature that can be summed up in a few words — one to three days.
  - Standard or full spec: beyond that, or anything that changes core, the data model, or more than one service.
- Tier mismatch (a multi-service change under a micro or quick spec) is a large divergence → the agent asks before tasking.

## Tier shapes

Human-written in every tier; the agent's task breakdown and test plan go in the tasking file.

Every tier opens with the three questions, one line each before the first section heading: `- What: <what ships>`, `- When: <date>`, `- Owner: <who>`. A spec that cannot answer them is a draft.

- Micro spec — a bug fix, docs, or config change:
  - **Goal**: one sentence — what problem this solves, for whom, and why.
  - **Scope**: what is in, what is explicitly out, and the boundary — which modules change and which do not.
  - **Behaviour**: numbered acceptance criteria (`R<id>`), written as observable facts.
  - **Error cases**: how each failure mode is detected and surfaced.
  - **Alternatives**: the other ways considered and why not those, one line each; the minimal fix is one of them.
  - **Open questions**: assumptions that need a human decision before or during implementation.
  - **Interfaces** appears when a public shape changes; there is no Design section — the fix is the design.
- Quick spec — a small feature summed up in a few words: the micro sections plus Design (§2) and Use cases — summary (§3).
- Standard or full spec: sections 1–4, 9, and 10 in full.

## File location

PR-scoped: `<project>/docs/<YYYYMMDD>_<short-task-slug>/<tier>.md` — the tier file is `microspec.md`, `quick-spec.md`, or the standard/full equivalent.
Long-lived: `<project>/docs/<module-slug>/<tier>.md`
Tasking file: `agent_tasking.md`, in the same directory as the spec it serves — next to `microspec.md`.

## Authorship

- The human owns the spec's content; the agent may hold the pen — the `task.md` contract (`review/TASK_FILE.md`).
  - The agent drafts from the human's words, near-verbatim, formatted into the tier shape; it shows the draft and writes on approval.
  - Allowed: grammar, spelling, expanding shorthand, placing text under the right heading.
  - Not allowed: rephrasing, summarising, or adding content the human did not say — no invented requirements, design, or alternatives.
- The agent's own analysis goes in the tasking file (§ Tasking file).
- A gap or conflict in the spec → the agent asks; the human supplies the words.

| # | Section | Lives in | Author | Agent rule |
|---|---|---|---|---|
| 1 | Requirements | Spec | Human | Human's words. Missing or empty → tasking does not start; ask. |
| 2 | Design | Spec | Human | Human's words. Missing → the agent proposes one in the tasking file and asks. |
| 3 | Use cases — summary | Spec | Human | Human's words. Numbered checklist (`U<id>`). |
| 4 | Use cases — detail | Spec | Human | Human's words. |
| 5 | Task breakdown — summary | Tasking file | Agent | Numbered checklist (`A<id>`). Ordered by dependency. Human reads end to end before work starts. |
| 6 | Task breakdown — detail | Tasking file | Agent | Expanded task descriptions with modules, tests, dependencies. |
| 7 | Test plan | Tasking file | Agent | Derive from requirements. Human reads for completeness. |
| 8 | Security checklist | Tasking file | Agent | Agent checks before completion. Human verifies. |
| 9 | Acceptance checklist | Spec | Human | Human's words. |
| 10 | References | Spec | Human | Human's words. Append-only. |

## Tasking file

- The tasking file ("tasking") is the agent's spec — the spec document the agent writes.
- The agent owns it; humans read and approve it.
- It references the human spec by `R<id>` / `U<id>`; it does not restate requirements.
- It holds the agent-authored sections (5–8) and the agent's derived artifacts, including:
  - Gap assumptions (`CODER.md` §1).
  - The input-state × behaviour matrix when the spec lacks one (P1).
  - The anti-pattern check (P3).
  - The acceptance-criterion → test mapping (P2).
  - Open questions for the human.
- Same style and tracker rules as the spec (§ Objective, § The spec is not a tracker).
- Its commit is separate from code commits.
- The tasking phase ends the turn with the tasking file pushed and an approval request (`CODER.md` §5 Two phases).
- It is a draft until a human has read it end to end and approved it explicitly in the thread or PR.
  - Silence is not approval; "confirmed offline" is not approval.
  - The agent records where the approval is.
- Spec and tasking work is exempt from the token-scope rule — deliberate as long as the design needs.

## Spec sections

### 1. Requirements (human)

What the system must do. Describe the **outputs and outcomes**, not the implementation.

- Answer up front: who the user is, what problem this solves, the alternatives and why not those, how success is measured.

- One requirement per bullet, numbered for tracking: `- [ ] R1: The system must...`
- Terse. One sentence per requirement. If it needs explanation, it's two requirements.
- Enough detail to be unambiguous. Not so much that it dictates implementation.
- No code names or internal jargon.
- Group related requirements under subheadings.
- List what is **out of scope**.
- State the boundary: which modules change and which do not.
  - A change that crosses the boundary (an "extension" that rewrites core) is a large divergence → ask.
- List every error case: what triggers it, what the caller sees.

Format:

```markdown
### Subheading
- [ ] R1: The system accepts any OCI container image that listens on a port.
- [ ] R2: No infrastructure implementation detail is exposed to clients.

### Out of Scope
- Thing we are not building
```

The `R<id>` numbers are stable identifiers. Use cases, test plans, and task breakdowns reference them. Do not renumber after review — append new requirements at the end.

### 2. Design (human)

How to meet the requirements. Sets direction without micromanaging.

- Interfaces: API shape, data in/out, events
- Components: what is involved, how they connect
- Data flow: inputs, outputs, where state lives
- Constraints: performance, security, compatibility
- Key decisions: technology/pattern choices with reasoning

The agent has flexibility in how it implements the design. The design defines the shape of the solution, not every line of code.

### 3. Use cases — summary (human)

Terse list of named scenarios that exercise the requirements. One line per use case, numbered for tracking.

Format:

```markdown
- [ ] U1: Developer creates and deploys a hello world app (R1, R13, R17)
- [ ] U2: Developer adds Custom Objects capability (R19, R23)
- [ ] U3: Agent deploys an app through the API (R8, R10)
```

Each use case references the requirements it exercises. The summary is the checklist — reviewers scan it to confirm coverage. Every requirement should appear in at least one use case.

### 4. Use cases — detail (human)

Expanded walkthrough for each use case listed in the summary.

- Identify the actor (user, agent, system, external service)
- Describe the trigger — what starts it
- Walk through the steps — what happens, in what order, through which components
- State the outcome — what the actor sees when it succeeds
- State the failure cases — what happens when it fails, what the actor sees

Use cases bridge requirements and design. Requirements say *what* the system must do. Design says *how* the system is structured. Use cases show *how actors interact with the system* in practice — they validate that the requirements are complete and the design supports real workflows.

### 5. Task breakdown — summary (agent — tasking file)

Terse checklist of implementation steps, numbered for tracking. One line per task, ordered by dependency — foundations first.

Format:

```markdown
- [ ] A1: Split monolithic controller into domain-specific packages (depends: —)
- [ ] A2: Extract Knative Service template builder (depends: A1)
- [ ] A3: Add Binding type to CRD (depends: A1)
```

Each task references its dependencies. One commit per task. The summary is the progress tracker.

### 6. Task breakdown — detail (agent — tasking file)

Expanded description for each task listed in the summary.

- What changes
- Which module/files are affected
- What tests verify completion
- Dependencies explained

### 7. Test plan (agent — tasking file)

Every requirement is covered. The plan is a floor, not a ceiling — implementation derives more tests than it names (see § Acceptance criteria are guides, not inventories).

- Every requirement has at least one test.
- The plan names groups of testing, never the test inventory.
- Happy path per requirement
- Error cases from section 1
- Boundary conditions: zero, one, max
- Design-mandated test constraints and pins earn a line; routine case enumeration does not.

### 8. Security checklist (agent — tasking file; human verifies)

Agent checks these before marking work complete. Human verifies during review. Numbered for tracking.

Format:

```markdown
- [ ] S1: No secrets, keys, or credentials in code or config files
- [ ] S2: All user input validated and sanitized at the boundary
```

Default items (include in every tasking file):

- [ ] S1: No secrets, keys, or credentials in code or config files
- [ ] S2: All user input validated and sanitized at the boundary
- [ ] S3: Auth required on every endpoint — no silent fallback to anonymous
- [ ] S4: Authorization checked: caller can only access their own resources
- [ ] S5: No SQL injection, command injection, or XSS vectors
- [ ] S6: Sensitive data not logged or exposed in error messages
- [ ] S7: Dependencies have no known critical vulnerabilities
- [ ] S8: File paths, URLs, and redirects cannot be manipulated by user input
- [ ] S9: Rate limiting or abuse protection on public-facing endpoints
- [ ] S10: Multi-tenant: resources scoped by tenant — no cross-tenant access

Add project-specific items from `@review/SECURITY_REVIEW.md` when applicable. Continue numbering from S11.

### 9. Acceptance checklist (human)

What a human verifies when reviewing the delivered code. Numbered for tracking.

Format:

```markdown
- [ ] X1: Code solves the stated goal
- [ ] X2: Behaviour matches each requirement
```

Default items (include in every spec):

- [ ] X1: Code solves the stated goal
- [ ] X2: Behaviour matches each requirement
- [ ] X3: Scope boundaries respected — nothing extra added
- [ ] X4: Interfaces match the design
- [ ] X5: Error cases handled as specified
- [ ] X6: No TODOs or placeholders left

Add project-specific items as needed. Continue numbering from X7.

### 10. References

Provenance, prior art, and source material that informed the spec.

- **Research**: prior specs, design reviews, Slack threads, PRs, git history, and investigations that shaped the requirements and design. Include dates and authors so decisions can be traced.
- **Modules affected**: repos, directories, and services this spec touches.
- **External**: links to external docs, RFCs, standards, or tools referenced in the design.

References are append-only during the spec lifecycle. Do not remove references even if the linked material becomes stale — they are the audit trail for design decisions.

## Validation

- `/check-spec` (`~/agents/skills/CHECK_SPEC.md`) checks a spec directory against this document: `scripts/validate_spec.py` for the mechanical rules, then a judgment pass.
- The coder runs it before asking for tasking approval; the reviewer runs it before verifying P1–P3.
- A spec that fails it is a draft.

## Acceptance criteria are guides, not inventories

- An acceptance criterion states a set of claims and clauses to check.
- Each criterion defines a group of testing and checks, not a single test.
- Each criterion derives at least one test at implementation — usually more.
- Criteria list the important happy paths and the important edge cases.
  - Including happy paths or edge cases found missing in a coding pass.
- Criteria detail only what they need to; they are not exhaustive of the code.
- Leave criteria as generalizations where appropriate.
- The code and tests will exceed the criteria — the spec never reads as the ceiling of testing.
- Do not enumerate the actual tests in the spec — that is the code-in-text-form failure.
  - Only design-mandated test constraints and pins earn spec space.

## The spec is not a tracker

- The spec states the target contract — the settled truth, written as if it had always been so.
- The spec is never a status tracker, changelog, worklog, or review-claim litigation record.
- No status markers in spec prose: no `DONE`, `Status:`, `REVERTED`, `NOT IMPLEMENTED`, no "at spec phase".
- No edit history in spec prose: no "corrected", "rewritten", "was X now Y", no rebuttal of review claims.
- When a section changes, rewrite it to the new truth and delete the old text.
- A reader must not be able to tell from any section what order it was written in.
- Each kind of record has its own home — never the spec:
  - What changed and when → git history of the spec file.
  - Why a direction was chosen or reversed → `task.md` `# DECISIONS` (`review/TASK_FILE.md`).
  - Review claims and their outcomes → the review store `<ID>.md` files (ISSUE_TRACKING.md).
  - Implementation progress → the task breakdown checkboxes (`A<id>`) in the tasking file, checkbox state only.
- The tracking surfaces are the numbered checklists — R/U/X in the spec, A/S in the tasking file — checkbox flips, not prose annotations.

## Rules

- Spec is the source of truth. Code out to the spec's intended target, filling
  in-scope gaps with the established conventions (fail-closed for security,
  SOLID for design, the coding standards) rather than prompting for
  micro-requirements. Only ask when those conventions give no clear answer.
  A change of code direction is recorded in the tasking file (small drift) or
  asked about (large divergence) — the agent does not rewrite the spec. See
  CODER.md §1 for the full divergence-by-size rule.
- Every requirement must be verifiable.
- Keep all sections in sync. A gap between them is a bug in the spec.
