---
name: review-triage
description: Slash command /review-triage. Mechanized review-claim triage per CODER.md §5 — record claims, cascade/scope gates, red-light proof, gated fixes. All store writes go through review_triage.py; judgment gates run as narrow-goal subagents. Use after any review produces claims.
---

# Review Triage

Executes the review-claim triage and red-light procedure from `~/agents/CODER.md` §5. The procedure text there is the definition; this skill is how it is run.

**All review-store writes go through the script.** Never hand-edit `review.md` or `<ID>.md` files during triage — the script enforces gate order, full IDs, required evidence, and store consistency:

```bash
python3 ~/agents/skills/review_triage.py --dir ~/reviews/<repo>-pr-<n> --repo <checkout> <command>
```

The script refuses out-of-order operations (red-light before gate, close without red-light, bare short IDs, human-only statuses). If it refuses, the procedure is being violated — fix the order, do not work around the script.

## Subagent rule

Judgment gates run as **subagents with one narrow goal each**. Give the subagent only its question and the minimal context; it returns a structured verdict, and the orchestrator records it via the script. A subagent never edits the store, never fixes code outside its goal, and never answers a question it wasn't asked.

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
3. **Cascade gate** — spawn a cascade-judge subagent per claim. Goal: given this claim, the `cascade-scan <ID>` output, and the overlapping issues' detail files — was the code this claim points at changed by a prior claim's fix? Verdict: `cascade-of:<full ID> + why`, or `not-cascade`. Record:
   ```bash
   review_triage.py --dir <DIR> gate <ID> --cascade-of <FULLID> --why "..."   # cascade → stops here, user decides
   ```
4. **Scope gates** — spawn a scope-judge subagent per surviving claim. Goal: given the claim, the micro-spec, `steering.md`, and the branch's changed-file list — does it fail micro-spec scope, steering design, or scope-creep? Verdict: first failing gate + reason, or pass. Record:
   ```bash
   review_triage.py --dir <DIR> gate <ID> --out-of-scope micro-spec|steering|scope-creep --why "..."
   review_triage.py --dir <DIR> gate <ID> --docs-nit      # doc fix allowed only if design unchanged
   review_triage.py --dir <DIR> gate <ID> --pass          # all gates clear → red-light next
   ```
5. **Red-light** — spawn a red-light subagent per passed claim. Goal: write ONE failing test in the real suite proving this claim, commit it red (the `--no-verify` carve-out, CODER.md §5 step 6), return `sha + file:case + raw red output`. Record (the script verifies the sha exists and touches the test file):
   ```bash
   review_triage.py --dir <DIR> --repo <checkout> redlight <ID> --sha <sha> --test "file:case" --output "<raw failure>"
   ```
   If the subagent cannot make a test fail: `unproven <ID> --probe "<test code>" --output "<passing output>"` — no fix happens.
6. **Fix** — spawn a fixer subagent per red-lighted claim. Goal: minimum production change to turn that one test green; never edit the test; micro-review the diff (anti-patterns, security, steering/micro-spec, acceptance criteria). If the fix fails or causes new claims: `needs-review <ID> --why "..."`, revert, and record the new claims via `open` + cascade gate.
7. **Close** with the fix commit and verification evidence:
   ```bash
   review_triage.py --dir <DIR> --repo <checkout> close <ID> --fix-sha <sha> --verify "<reverify command + result>"
   ```
   The close output names the red-light test that proves the claim — relay it verbatim when reporting the fix.
8. **Check** store consistency at the end (and before reporting to the user):
   ```bash
   review_triage.py --dir <DIR> check
   ```
9. **Report** to the user in chat as the finding-grammar checkbox list. **Every fixed claim is reported with its matching red-light test** — the `file:case` and red commit sha that prove the claim (`list --tests` prints the pairing). A fix reported without its proving test is an incomplete report.

## Rules

- Claims are recorded before they are judged. The script's `open` is always the first touch.
- `NEEDS_REVIEW:cascade` items are never red-lighted, fixed, or closed without the user's explicit approval.
- The script's refusals are the procedure working. Do not bypass with hand edits, and never set `DEFERRED`/`WILL_NOT_FIX` (human-only).
- Subagents get one goal and minimal context; verdicts come back to the orchestrator, which records them.
- Chat may use short IDs; every store record and code/test/commit reference uses the full ID (grammar: `REVIEW_METHOD.md § ID format`).
