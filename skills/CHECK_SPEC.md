---
name: check-spec
description: Slash command /check-spec. Check a spec directory (micro-spec.md / quick-spec.md / requirements.md+design.md+tasks.md and agent_tasking.md) against design/HUMAN_SPECS.md and design/AGENT_TASKING.md — mechanical checks via scripts/validate_spec.py, then a judgment pass for what the script cannot see. Reports violations; edits nothing.
---

# Check Spec

Checks a spec directory against `~/agents/design/HUMAN_SPECS.md` (the human spec) and `~/agents/design/AGENT_TASKING.md` (the tasking file). Read-only: the spec carries the human's words and the tasking file is the agent's Phase 1 artifact — this skill reports, it does not edit either.

## Workflow

1. Resolve the spec directory: the argument, else the directory the PR description links to, else `specs/<YYYYMMDD>-<slug>/` for the current branch. Unknown → ask.
2. Run the mechanical checks and relay the output verbatim:
   ```bash
   python3 ~/agents/scripts/validate_spec.py <spec-dir>
   ```
   It checks the spec (`micro-spec.md`, `quick-spec.md`, or `requirements.md` + `design.md` + `tasks.md`): the `When` / `Owner` lines, the micro fields (What / Why / How / Acceptance / Not changing / Alternatives, `## Related`), the quick sections (Problem with Decision / Success / Next, Requirements `R<n>`, Implementation approach, Implementation tasks, Verification, Related), out-of-scope, boundary, and alternatives lines, tracker markers, line-number citations. When `agent_tasking.md` is present: required sections, `A<id>` lines, `S1–S10`, every spec `R<id>` referenced, no restated human sections.
3. Judgment pass — read the tier file end to end and check what the script cannot:
   - Requirements state outputs and outcomes from the user's perspective, not implementation (HUMAN_SPECS.md § Every tier).
   - Statements are open/closed — what the change adds, not the module inventory — and free of hyperbole (`style/DOT_POINT_SRP.md` § SOLID statements).
   - Alternatives name the minimal fix and say why not.
   - The boundary matches the tier: a micro spec that touches core, the data model, or more than one service is a tier mismatch (HUMAN_SPECS.md § Whether and which spec).
   - No code-in-text-form: no test inventories, no line-by-line implementation (AGENT_TASKING.md § Acceptance criteria are guides, not inventories).
   - Dot-point SRP style: one clause per line, no hand-wrapped prose.
   - Tasking file, when present: references `R<id>` rather than restating; every task names its tests; a design change appears as an open question, not as settled text.
4. Report in chat as a flat checkbox list, mechanical findings first, one line each: `- [ ] <file> § <section> - <violation>`. `OK` when both passes are clean.

## Rules

- Report only. The human edits the spec; the agent edits the tasking file in its own Phase 1 turn.
- A spec that fails the mechanical pass is a draft — Phase 2 does not start on it (CODER.md §5 Two phases).
- The coder runs it before asking for approval; the reviewer runs it before verifying P1–P3.
- The script's output is the evidence — relay it, do not paraphrase it.
