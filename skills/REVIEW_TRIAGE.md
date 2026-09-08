---
name: review-triage
description: Slash command /review-triage. Mechanized review-claim triage per CODER.md §5 — record claims, cascade/scope gates, red-light proof, gated fixes. All store writes go through review_triage.py; judgment gates run as narrow-goal subagents. Use after any review produces claims.
---

# Review Triage

**This skill is the review-claim triage and red-light procedure.** `~/agents/CODER.md` §5 mandates it after any review and states the invariants; the workflow below is the definition of the steps.

**All review-store writes go through the script.** Never hand-edit `review.md` or `<ID>.md` files during triage — the script enforces gate order, full IDs, required evidence, and store consistency:

```bash
python3 ~/agents/skills/review_triage.py --dir ~/reviews/<repo>-pr-<n> --repo <checkout> <command>
```

The script refuses out-of-order operations (red-light before gate, close without red-light, bare short IDs, human-only statuses). If it refuses, the procedure is being violated — fix the order, do not work around the script.

## Subagent rule

Judgment gates run as **subagents with one narrow goal each**. Give the subagent only its question and the minimal context; it returns a structured verdict, and the orchestrator records it via the script. A subagent never edits the store, never fixes code outside its goal, and never answers a question it wasn't asked.

## Finish the whole triage

- The triage runs to completion in one turn: every recorded claim reaches a closed or needs-review status (`REVIEW_METHOD.md` § Status tokens) before the turn ends.
- A per-claim halt (`--cascade-of`, `unproven`, `needs-review`) stops that claim only; the pipeline continues for every other claim.
- Step reports are text within the turn, not a turn boundary — report the step, then start the next step in the same turn.
- Do not end the turn to ask permission for a step the workflow already includes.
- Spawn independent subagents together and keep working while they run; record each verdict as it returns.
  - A claim whose subagent is still running is not terminal — the triage is not done until every verdict is recorded; do not guess a pending verdict.
- Token scope: reasoning is for the verdict, output is for the record — write each store record and step report once, as it completes; the triage is not drafted as reasoning and again as output.
- The turn ends after step 9 `check` and the step 10 report, or when blocked on input the user has to provide (a cascade ruling, a human-only status).

## Workflow

1. **Init** the store (idempotent — refreshes `head:`/`reviewed:` if it exists):
   ```bash
   review_triage.py --dir <DIR> init --repo-name <repo> --pr <n> --branch <branch> --base origin/main --head <sha>
   ```
2. **Record every claim first** — no triage before recording:
   ```bash
   review_triage.py --dir <DIR> open --type B --sev HIGH --title "..." --file "path:line" --desc "..." --evidence "..." --fix "..." --reverify "..."
   ```
   It prints the full ID and warns `POSSIBLE CASCADE` when the claim's file overlaps a prior issue.
   `--fix` records the **reviewer's suggested fix** — untrusted input stored for the record, never the implementation plan (see step 7).
3. **Cascade gate** — spawn a cascade-judge subagent per claim. Goal: given this claim, the `cascade-scan <ID>` output, and the overlapping issues' detail files — was the code this claim points at changed by a prior claim's fix? Verdict: `cascade-of:<full ID> + why`, or `not-cascade`. Record:
   ```bash
   review_triage.py --dir <DIR> gate <ID> --cascade-of <FULLID> --why "..."   # cascade → this claim halts for the user; the pipeline continues with the others
   ```
4. **Scope gates** — spawn a scope-judge subagent per surviving claim. Goal: given the claim, the micro-spec, `steering.md`, and the branch's changed-file list — does it fail micro-spec scope, steering design, or scope-creep? Verdict: first failing gate + reason, or pass. Decide fast — the verdict is a lookup against the spec and the changed-file list, not a design discussion; a good suggestion with no spec line behind it is `scope-creep`. Record:
   ```bash
   review_triage.py --dir <DIR> gate <ID> --out-of-scope micro-spec|steering|scope-creep --why "..."
   review_triage.py --dir <DIR> gate <ID> --doc-claim     # claim against a non-executable artifact (spec prose, comments, naming)
   review_triage.py --dir <DIR> gate <ID> --style-claim   # style-only code change, no observable output diff (e.g. require()->import)
   review_triage.py --dir <DIR> gate <ID> --pass          # all gates clear → red-light next
   ```
   **Kind decides `--doc-claim` / `--style-claim`, not size.** They classify what the artifact is — non-executable prose, or a code rewrite with no observable difference — never how big the change is: a doc-claim that rewrites a spec's whole design section is still a doc-claim; a one-character code typo with observable effect still red-lights. If a committed test *could* distinguish pre-fix from post-fix, it is not this gate — use `--pass` and red-light normally.
   Doc/style claims skip trace and red-light (`redlight:n/a-docs`) and are **never `UNPROVEN`** — the script refuses it; a red-light refusal on one of these is the signal you took the wrong path, not a blocker. They still get a verify pass, not a wave-through:
   - Read the current artifact at the claimed location — the claim is a hypothesis and may already be stale.
   - Quote the defective text and the corrected text as the close `--verify` evidence.
   - A fix that changes settled design direction (micro-spec, `steering.md`) goes to `needs-review` for the user's ruling, never silently in.
5. **Trace** — spawn a trace subagent per passed claim, before any red-light work. Goal: read the code at the claim's `file:line` on **current HEAD** and trace the path the claim depends on — where the value comes from, its types and DB constraints, existing guards, the call sites. The claim's own description and stored code snippets are **not** evidence; they describe the code as it was when the claim was written. Verdict, recorded via the script (which refuses red-light until `trace:possible`):
   ```bash
   review_triage.py --dir <DIR> --repo <checkout> trace <ID> --possible --path "<file:line trace of how the defect manifests>"
   review_triage.py --dir <DIR> --repo <checkout> trace <ID> --impossible --evidence "<file:line quotes: types/guards/constraints>"
   review_triage.py --dir <DIR> --repo <checkout> trace <ID> --already-fixed <sha> --evidence "<file:line quotes of the fix>"   # sha must be an ancestor of HEAD
   ```
   **Every claim resolves with a committed test in code — never agent speculation.** A `possible` verdict leads to a red proof test; `impossible` and `already-fixed` lead to a **green disproof test** — one committed test pinning why the claim cannot happen (e.g. an empty entity id cannot reach the call) or guarding the prior fix. Spawn a disproof subagent for it, then close via:
   ```bash
   review_triage.py --dir <DIR> --repo <checkout> disprove <ID> --sha <sha> --test "file:case" --output "<green run output>"
   ```
   `UNPROVEN` is reserved for the rare claim where neither a red proof nor a green disproof is constructable — it stays open for the user.
6. **Red-light** — spawn a red-light subagent per traced-possible claim. Goal: write ONE failing test in the real suite proving this claim, commit it red (the `--no-verify` carve-out, CODER.md §5 step 6), return `sha + file:case + raw red output`. Record (the script verifies the sha exists and touches the test file):
   ```bash
   review_triage.py --dir <DIR> --repo <checkout> redlight <ID> --sha <sha> --test "file:case" --output "<raw failure>"
   ```
   If the subagent cannot make a test fail: `unproven <ID> --probe "<test code>" --output "<passing output>"` — no fix happens.
7. **Fix** — spawn a fixer subagent per red-lighted claim. Goal: design the fix **from the trace, not from the reviewer's suggestion**, then make the minimum production change, within the micro-spec's scope, to turn that one test green; never edit the test; micro-review the diff (anti-patterns, security, steering/micro-spec, acceptance criteria). Before writing code the fixer must:
   - Re-examine the problem itself — the trace's mechanism is the spec, the claim's prose is not.
   - Audit the recorded `fix:` suggestion before reusing any part of it: compounding issues and design failures; out-of-scope additions and code bloat; over-engineering measured against the happy path most code takes — especially when the fix targets an edge case, worst of all an edge case of an edge case.
   - Return, with the diff, a **justification**: why this fix resolves the defect class fully and why it will not compound — including why it differs from (or is smaller than) the suggestion.
   If the fix fails or causes new claims: `needs-review <ID> --why "..."`, revert, and record the new claims via `open` + cascade gate.
8. **Close** with the fix commit, verification evidence, and the fixer's justification (recorded in the detail file — the cascade gate reads it later):
   ```bash
   review_triage.py --dir <DIR> --repo <checkout> close <ID> --fix-sha <sha> --verify "<reverify command + result>" --justification "<why the fix resolves the class fully and will not compound>"
   ```
   The close output names the red-light test that proves the claim — relay it verbatim when reporting the fix.
9. **Check** store consistency at the end (and before reporting to the user):
   ```bash
   review_triage.py --dir <DIR> check
   ```
10. **Report** to the user in chat as the finding-grammar checkbox list. **Every fixed claim is reported with its matching red-light test** — the `file:case` and red commit sha that prove the claim (`list --tests` prints the pairing). A fix reported without its proving test is an incomplete report.

## Cascade fixes (only after the user approves)

A cascade means a prior fix's recorded justification was wrong. When the user approves fixing a `NEEDS_REVIEW:cascade` item:

1. Read the prior issue's detail file, including its `justification:` — that is the reasoning that failed.
2. State, in chat and in the new issue's detail, **where that justification went wrong** — which assumption the cascade disproves.
3. Follow every `cascade-of:` link to the root of the chain; the redesign starts from the root defect, not from the latest symptom.
4. Redesign the fix from the ground up against the whole chain — never a patch on top of the failed fix.
5. Resume the pipeline: `reopen <ID> --why "user approved cascade fix"`, then `gate --pass` → trace → red-light → fix → close. The new close `--justification` must name the prior fix's failure and why the redesign does not repeat it.

## Step reporting — no shortcuts

- **Report every step as it completes, before starting the next — in the same turn.** One line per claim per step, in chat:
  ```
  [triage] step 2 record  — I43.<SID> opened (OPEN, redlight:pending)
  [triage] step 3 cascade — I43.<SID>: not-cascade
  [triage] step 4 scope   — I43.<SID>: pass
  [triage] step 5 trace   — I43.<SID>: impossible — a.ts:1 id NOT NULL uuid
  [triage] step 6 test    — I43.<SID>: green disproof tests/a.spec.ts:no-empty-id @ <sha>
  ```
- The script's printed output IS the step evidence — relay it verbatim, never paraphrase it into looser language.
- Steps run in order for every claim. Skipping a step, batching claims through "obvious" verdicts without their subagent, or reporting several steps retroactively in one block is shortcutting — the failure this skill exists to prevent.
- A step with no report did not happen. If the user asks "what step are you on?", the answer must be reconstructable from the chat transcript alone.
- Finish with `check` and the `list --tests` pairing before the final summary.

## Rules

- Claims are recorded before they are judged. The script's `open` is always the first touch.
- **Scope first.** The micro-spec defines it; the scope gate is decisive — a claim not traceable to a spec requirement or the branch's changed files is `OUT_OF_SCOPE`, however good the suggestion. A claim is not admitted by widening the spec; a fix that needs a new requirement is `needs-review`, not a spec edit.
- **A claim is a hypothesis about the code, not a fact.** Never reason from the claim's description or its stored snippets — they age. Every verdict after the scope gates starts with reading the current code at the claimed location. The claim's analysis and framing are equally untrusted — reviewer prose never decides fix-vs-document or picks the remedy.
- **The reviewer's suggested fix is untrusted input.** Reviewers routinely flag their own suggestions as broken on the next pass. The fixer designs from the trace; any reused part of the suggestion is audited first (step 7).
- **Every resolved claim has a committed test**: red proves it, green disproves it. Prose evidence selects which test to write; it never substitutes for one.
- **Every close records a justification** — why the fix resolves the defect class fully and will not compound. It is the artifact the cascade procedure audits when a fix turns out wrong.
- A reverted fix's red test stays committed and red until the issue is resolved — never deleted, never masked to make the suite green.
- Doc-claims and style-claims (`--doc-claim` / `--style-claim`) are kind classifications, not size — any claim against a non-executable artifact qualifies, however large the change. They are fixed only when the change does not change the design in the micro-spec or `steering.md`, and — for `--style-claim` — does not change observable output; otherwise `needs-review` with the conflict explained.
- `--style-claim` is for claims like SEC2-style `require()`→`import` swaps: the fix is real and correct, but nothing distinguishes pre-fix from post-fix at runtime, so no red/green test is constructable. Do not reach for it just because writing the test is inconvenient — it is for changes with *no possible* observable difference, not merely a hard-to-test one.
- A doc-claim or style-claim is never `UNPROVEN` — `UNPROVEN` means "a test is owed but cannot be constructed", and no test is owed here. The script refuses it; route verify-and-fix or `needs-review`.
- `NEEDS_REVIEW:cascade` items are never red-lighted, fixed, or closed without the user's explicit approval.
- The script's refusals are the procedure working. Do not bypass with hand edits, and never set `DEFERRED`/`WILL_NOT_FIX` (human-only).
- Subagents get one goal and minimal context; verdicts come back to the orchestrator, which records them.
- Chat may use short IDs; every store record and code/test/commit reference uses the full ID (grammar: `REVIEW_METHOD.md § ID format`).
