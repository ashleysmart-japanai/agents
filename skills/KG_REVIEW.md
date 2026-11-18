---
name: kg-review
description: Slash command /kg-review. Review claims or code against prior claims and the reference data, then propose fixes. For each claim — understand the problem, run a Graphify GraphRAG query to locate similar prior items, rank them against the claim, review the prior decisions (supersedes, user rulings, human comments, steering, anti-patterns and design principles), summarise them, and propose a fix grounded in them. Fixes apply only on confirmation; each new ruling is recorded once. Also /reviewer-kg for the support tasks (build, update, lint, remember).
---

# KG Review

Use this skill when the user asks to run `/kg-review`, to KG-review claims, or to review code against prior claims and the reference data.

- **Objective:** review claims or code against prior claims and the reference data, and propose fixes.
- Building, updating, and linting the graph are support tasks for that objective.
- Spec: `~/agents/specs/20261118-reviewer-kg/microspec.md`.

## Inputs

- **Claims:** tracking IDs (`B11.2wBdp3GP2TbcM0eotPjNVV`), `store/ID`, or a review store (`~/reviews/<repo>-pr-<n>/`) whose not-closed claims are reviewed.
- **Code:** a branch or diff; review it per `~/agents/review/REVIEW_METHOD.md` first to produce claims, then run the per-claim review on each.

## Tools

- `KG=~/agents/scripts/build_reviewer_kg.py`
- `G=~/agents-secret/kg/reviewer/graph.json`
- `CTX='--context similar_to --context touches --context steered_by --context supersedes --context about --context cascade_of'`
- Precedent links only; `in_store`, `decided_as`, `raised_by`, `exemplifies`, and `cites` are hubs that flood the traversal.
- `LOG="python3 $KG log --run $RUN"` — append a step to the run log.

## Run log

- Every `/kg-review` run writes a debug log under `~/review-kg/<YYYYMMDD-HHMMSS>-<target>/`.
- Start it first: `RUN=$(python3 $KG run-start --target "<claims, store, or branch>" --agent <codex|claude>)`.
- The run holds `meta.json`, `events.jsonl`, each claim's Graphify output and `match` JSON, and `run.md`.
- `match --log-run $RUN` logs what the KG found; the agent logs what it used and why with `$LOG`.
- Each `$LOG` call takes `--claim <store/ID> --kind <kind> --text "<what>"`, plus `--evidence` (file:line, command and result, URL) and `--ref` (prior ID, ruling ID, steering name, reference doc) as needed.
- Log the step before acting on it; a run with no log entry for a decision is incomplete.
- Finish with `python3 $KG run-report --run $RUN` and give the user the `run.md` path.
- The log is private: it holds prior-claim text from other repos; never copy it into a repo.

## Per-claim review

Run these steps for each claim, in order.

1. **Understand the claim:**
   - Read its `<ID>.md` detail file: title, description, evidence, file, status.
   - Read the code at the cited `file:line` in the current checkout.
   - State the problem in one or two lines as data flow, control flow, call order, or state.
   - `$LOG --claim <store/ID> --kind understanding --text "<problem>" --evidence "<file:line>"`
   - Prove it locally: trace the code path, or run the existing failing test; a claim that cannot be proved is reported unproven.
   - Do not write or commit red tests, and do not run review-triage gates; that is `/review-triage`, run only when the user asks.
2. **Locate similar items with Graphify GraphRAG:**
   - `GQ="$RUN/<store>__<ID>.graphify.txt"`
   - `graphify query "<claim title>" --seed "finding:<store>/<ID>" $CTX --graph $G --budget 8000 > "$GQ"`
   - For a claim not yet in the graph, omit `--seed` and query with the title and file path.
3. **Rank what matches the claim:**
   - `python3 $KG match --finding <store>/<ID> --graphify "$GQ" --log-run "$RUN" --top 8 --format json`
   - The claim is excluded from its own matches; graph-retrieved and text-retrieved candidates are ranked together.
   - Keep a prior when it matches the problem, not only the wording; drop false friends (same word, different meaning).
   - Label each kept prior as same file, same PR, or other PR.
   - Log each prior: `--kind kept` or `--kind dropped`, with the reason and `--ref <prior ID>`.
4. **Review the prior instances and their decisions:**
   - **Outcome:** `fixed`, `rejected`, `out-of-scope`, `not-reproduced`, or `undecided`, from its status.
   - **Supersedes:** a prior with `superseded_by` is governed by its `current_decision`, not its own outcome.
   - **User rulings:** `rulings` on a prior and the `prejudgement` block; a `user-ruling` basis decides the handling.
   - **Human comments:** `justification`, `reviewer_ack`, `pushback`, `reply`, `scope`, and the `thread` URL.
   - **Steering:** `steering` entries from the stores' `task.md` `# DECISIONS`.
   - **Reference data:** the `references` on each prior and the top-level reference matches; open the doc and read its Fix section.
   - Open the prior's `detail` file when a field is truncated or the decision is unclear.
   - Log what was used: `--kind prior_decision`, `--kind steering`, and `--kind reference`, each with `--ref` and `--evidence`.
5. **Summarise:**
   - One line per kept prior: ID, store, outcome, what was decided, and why.
   - The reference docs and design principles that applied, with the rule from each.
   - The pre-judgement: basis and verdict.
   - Coverage gaps: no prior found, or no reference doc for the problem.
   - Log `--kind prejudgement` (basis, verdict, the ruling or priors it rests on) and each `--kind gap`.
6. **Propose the fix:**
   - Base it on the governing prior decision and the reference doc's fix, adapted to the current code.
   - A prior `rejected` or `out-of-scope` decision is stated first; propose against it only with a stated reason.
   - Show the fix as a unified diff with `file:line` citations.
   - Log `--kind decision` (what to do and why, with the evidence and refs it rests on) and `--kind proposal` (a summary of the fix and the files it touches).

## Proposal and ruling

1. Print one table: tracking ID, severity, problem, governing prior and outcome, reference rule, pre-judgement, proposed fix.
2. Follow a `user-ruling` pre-judgement without asking how to handle the claim; cite the ruling ID.
3. Ask once:
   - which fixes to apply: **all**, a list of tracking IDs, or **none**;
   - how to handle each claim without a `user-ruling` pre-judgement.
4. Log the user's answer per claim: `--kind user_response`.
5. Apply the confirmed fixes to the working tree; run the tests for the touched files; report each command's result.
   - Log `--kind applied` with the test command and its result as `--evidence`.
6. Record each new ruling once:
   - `python3 $KG remember --about <store>/<ID> --outcome <o> --confidence verified --title "<the rule as a general statement>" --fix "<how>" --rationale "<user's words>" --source <PR or thread URL>`
   - Write the title as the general rule so it matches the next occurrence.
   - Add `--supersedes <prior>` when the ruling contradicts a prior decision.
   - Record only rulings the user gave.
   - Log `--kind ruling` with the memory ID `remember` printed.
7. Close the run: `python3 $KG run-report --run "$RUN"`; give the user the `run.md` path.

## Support tasks (`/reviewer-kg`)

- **Refresh before a review:** `python3 $KG update`.
- **Lint before a review:** `python3 $KG lint`; stop on errors; report warning counts in one line.
- `/reviewer-kg build` → `python3 $KG build`.
- `/reviewer-kg update` → `python3 $KG update`.
- `/reviewer-kg lint` → `python3 $KG lint`; resolve each `W2 conflicting decisions` pair by asking the user and recording a supersede.
- `/reviewer-kg remember ...` → `python3 $KG remember ...`.
- After recording rulings: `python3 $KG update` then `python3 $KG lint`.

## Rules

- When the user explicitly asks to use `/kg-review`, treat that request as approval to run the graph commands and to append the rulings the user gives to memory.
- `/kg-review` does not run `/review-triage`; it does not move claims through triage gates or change their status.
- Review tracking follows `~/agents/review/ISSUE_TRACKING.md`; review triage (`~/agents/skills/REVIEW_TRIAGE.md`) runs only when the user asks.
- Ask before applying any fix; apply only the confirmed set.
- Never commit or push.
- Never apply a `NEEDS_REVIEW:cascade` claim without the user's explicit ruling.
- Never edit or delete lines in `memory.jsonl`; supersede instead.
- Edit review-store files only through the `~/agents/review/ISSUE_TRACKING.md` procedure.
- A verified user ruling decides handling; a hypothesis, a prior finding, or a steering note only informs it.
- The graph is advisory evidence; each claim still needs proof in current code.
- Keep graph content private: do not copy prior-claim text, evidence, or URLs from other repos into public repos, PR comments, or commits.
- Cite a prior claim by its full tracking ID and store.
