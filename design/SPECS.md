# Writing Specs for AI Agents

## File location

PR-scoped: `<project>/docs/<YYYYMMDD>_<short-task-slug>.md`
Long-lived: `<project>/docs/<module-slug>.md`

## Authorship

| Section | Author | Agent rule |
|---|---|---|
| Requirements | Human | Read-only. Do not add, remove, or reword. |
| Design | Human or Agent | If human provides it, follow it. If missing, propose and wait for approval. |
| Task breakdown | Agent | Derive from design. Human reviews before work starts. |
| Test plan | Agent | Derive from requirements. Human reviews for completeness. |
| Security checklist | Agent | Agent checks before completion. Human verifies. |
| Acceptance checklist | Human | Read-only. |

If the agent finds a gap or conflict in a human-authored section, it asks — it does not silently fix it.

## Spec sections

### 1. Requirements (human)

What the system must do. Describe the **outputs and outcomes**, not the implementation.

- One requirement per bullet. Compound items become sub-lists.
- Enough detail to be unambiguous. Not so much that it dictates implementation.
- No code names or internal jargon.
- List what is **out of scope**.
- List every error case: what triggers it, what the caller sees.

### 2. Design (human or agent)

How to meet the requirements. Sets direction without micromanaging.

- Interfaces: API shape, data in/out, events
- Components: what is involved, how they connect
- Data flow: inputs, outputs, where state lives
- Constraints: performance, security, compatibility
- Key decisions: technology/pattern choices with reasoning

The agent has flexibility in how it implements the design. The design defines the shape of the solution, not every line of code.

### 3. Task breakdown (agent)

Ordered implementation steps derived from the design.

- One commit per task
- Ordered by dependency — foundations first

### 4. Test plan (agent)

Maps 1-to-1 to requirements. No requirement without a test. No test without a requirement.

- Happy path per requirement
- Error cases from section 1
- Boundary conditions: zero, one, max

### 5. Security checklist (agent, human reviews)

Agent checks these before marking work complete. Human verifies during review.

- [ ] No secrets, keys, or credentials in code or config files
- [ ] All user input validated and sanitized at the boundary
- [ ] Auth required on every endpoint — no silent fallback to anonymous
- [ ] Authorization checked: caller can only access their own resources
- [ ] No SQL injection, command injection, or XSS vectors
- [ ] Sensitive data not logged or exposed in error messages
- [ ] Dependencies have no known critical vulnerabilities
- [ ] File paths, URLs, and redirects cannot be manipulated by user input
- [ ] Rate limiting or abuse protection on public-facing endpoints
- [ ] Multi-tenant: resources scoped by tenant — no cross-tenant access

Add project-specific items from `@SECURITY_REVIEWER.md` when applicable.

### 6. Acceptance checklist (human)

What a human verifies when reviewing the delivered code.

- [ ] Code solves the stated goal
- [ ] Behaviour matches each requirement
- [ ] Scope boundaries respected — nothing extra added
- [ ] Interfaces match the design
- [ ] Error cases handled as specified
- [ ] No TODOs or placeholders left

Add project-specific items as needed.

## Rules

- Spec is the source of truth. Update the spec before changing code direction.
- Every requirement must be verifiable.
- Keep all sections in sync. A gap between them is a bug in the spec.
