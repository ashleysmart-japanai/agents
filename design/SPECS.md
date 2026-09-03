# Writing Specs for AI Agents

## Objective

- Capture the design requirements and goals.
- Capture the acceptance requirements.
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

## File location

PR-scoped: `<project>/docs/<YYYYMMDD>_<short-task-slug>.md`
Long-lived: `<project>/docs/<module-slug>.md`

## Authorship

| # | Section | Author | Agent rule |
|---|---|---|---|
| 1 | Requirements | Human | Read-only. Do not add, remove, or reword. |
| 2 | Design | Human or Agent | If human provides it, follow it. If missing, propose and wait for approval. |
| 3 | Use cases — summary | Human or Agent | Numbered checklist (`U<id>`). References requirements. Human reviews. |
| 4 | Use cases — detail | Human or Agent | Expanded walkthroughs. Validates requirements against real workflows. |
| 5 | Task breakdown — summary | Agent | Numbered checklist (`A<id>`). Ordered by dependency. Human reviews before work starts. |
| 6 | Task breakdown — detail | Agent | Expanded task descriptions with modules, tests, dependencies. |
| 7 | Test plan | Agent | Derive from requirements. Human reviews for completeness. |
| 8 | Security checklist | Agent | Agent checks before completion. Human verifies. |
| 9 | Acceptance checklist | Human | Read-only. |
| 10 | References | Human or Agent | Append-only. Do not remove entries. |

If the agent finds a gap or conflict in a human-authored section, it asks — it does not silently fix it.

The spec phase ends the turn with an approval request; implementation starts on approval (`CODER.md` §5 Two phases). Specs are exempt from the token-scope rule — deliberate as long as the design needs.

## Spec sections

### 1. Requirements (human)

What the system must do. Describe the **outputs and outcomes**, not the implementation.

- One requirement per bullet, numbered for tracking: `- [ ] R1: The system must...`
- Terse. One sentence per requirement. If it needs explanation, it's two requirements.
- Enough detail to be unambiguous. Not so much that it dictates implementation.
- No code names or internal jargon.
- Group related requirements under subheadings.
- List what is **out of scope**.
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

### 2. Design (human or agent)

How to meet the requirements. Sets direction without micromanaging.

- Interfaces: API shape, data in/out, events
- Components: what is involved, how they connect
- Data flow: inputs, outputs, where state lives
- Constraints: performance, security, compatibility
- Key decisions: technology/pattern choices with reasoning

The agent has flexibility in how it implements the design. The design defines the shape of the solution, not every line of code.

### 3. Use cases — summary (human or agent)

Terse list of named scenarios that exercise the requirements. One line per use case, numbered for tracking.

Format:

```markdown
- [ ] U1: Developer creates and deploys a hello world app (R1, R13, R17)
- [ ] U2: Developer adds Custom Objects capability (R19, R23)
- [ ] U3: Agent deploys an app through the API (R8, R10)
```

Each use case references the requirements it exercises. The summary is the checklist — reviewers scan it to confirm coverage. Every requirement should appear in at least one use case.

### 4. Use cases — detail (human or agent)

Expanded walkthrough for each use case listed in the summary.

- Identify the actor (user, agent, system, external service)
- Describe the trigger — what starts it
- Walk through the steps — what happens, in what order, through which components
- State the outcome — what the actor sees when it succeeds
- State the failure cases — what happens when it fails, what the actor sees

Use cases bridge requirements and design. Requirements say *what* the system must do. Design says *how* the system is structured. Use cases show *how actors interact with the system* in practice — they validate that the requirements are complete and the design supports real workflows.

### 5. Task breakdown — summary (agent)

Terse checklist of implementation steps, numbered for tracking. One line per task, ordered by dependency — foundations first.

Format:

```markdown
- [ ] A1: Split monolithic controller into domain-specific packages (depends: —)
- [ ] A2: Extract Knative Service template builder (depends: A1)
- [ ] A3: Add Binding type to CRD (depends: A1)
```

Each task references its dependencies. One commit per task. The summary is the progress tracker.

### 6. Task breakdown — detail (agent)

Expanded description for each task listed in the summary.

- What changes
- Which module/files are affected
- What tests verify completion
- Dependencies explained

### 7. Test plan (agent)

Every requirement is covered. The plan is a floor, not a ceiling — implementation derives more tests than it names (see § Acceptance criteria are guides, not inventories).

- Every requirement has at least one test.
- The plan names groups of testing, never the test inventory.
- Happy path per requirement
- Error cases from section 1
- Boundary conditions: zero, one, max
- Design-mandated test constraints and pins earn a line; routine case enumeration does not.

### 8. Security checklist (agent, human reviews)

Agent checks these before marking work complete. Human verifies during review. Numbered for tracking.

Format:

```markdown
- [ ] S1: No secrets, keys, or credentials in code or config files
- [ ] S2: All user input validated and sanitized at the boundary
```

Default items (include in every spec):

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
  - Why a direction was chosen or reversed → `task.md` `# DECISIONS` (ISSUE_TRACKING.md § Task file).
  - Review claims and their outcomes → the review store `<ID>.md` files (ISSUE_TRACKING.md).
  - Implementation progress → the task breakdown checkboxes (`A<id>`), checkbox state only.
- The only tracking surfaces in a spec are the numbered checklists (R/U/A/S/X and `A<id>`) — checkbox flips, never prose annotations.

## Rules

- Spec is the source of truth. Code out to the spec's intended target, filling
  in-scope gaps with the established conventions (fail-closed for security,
  SOLID for design, the coding standards) rather than prompting for
  micro-requirements. Only ask when those conventions give no clear answer.
  Update the spec before changing code direction — but a large or clear
  divergence from the spec's intent is a stop-and-ask, not a self-approved spec
  rewrite. See CODER.md §1 for the full divergence-by-size rule.
- Every requirement must be verifiable.
- Keep all sections in sync. A gap between them is a bug in the spec.
