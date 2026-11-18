---
name: kg-review
description: Slash command /kg-review. Review a branch or diff using the reviewer knowledge graph — research each bug, match it to prior findings and the user's prior rulings, give a pre-judgement, propose a fix citing what matched, apply fixes only on confirmation (all or listed tracking IDs), and record each new ruling once so the next review follows it. Also /reviewer-kg for build, update, lint, and remember.
---

# KG Review

Use this skill when the user asks to run `/kg-review`, review with the reviewer KG, or apply prior review decisions to a change.

- The aim: the user tells the agent once how to handle an issue; every later review gets that ruling back as a pre-judgement and follows it.
- Spec: `~/agents/specs/20261118-reviewer-kg/microspec.md`.

## Tool

- `KG=~/agents/scripts/build_reviewer_kg.py`
- Graph, cache, and memory live in `~/agents-secret/kg/reviewer/` (private).
- `python3 $KG update` — refresh from `~/reviews/` and `~/agents/reference/`.
- `python3 $KG lint` — exit 1 on errors.
- `python3 $KG match --text "<claim>" --file <path> [--repo <repo>] [--format json]` — pre-judgement, prior matches, reference matches.
- `python3 $KG match --diff <file|->` — prior findings on the changed lines and files.
- `python3 $KG remember --about <finding> --outcome <o> --confidence verified --title "<rule>" --fix "<how>" --rationale "<why>" --source <url>` — record a ruling.
- `python3 $KG remember --kind supersede --supersedes <prior> ...` — replace a prior decision; the prior stays.
- Graphify reads the same graph: `graphify explain|query|path --graph ~/agents-secret/kg/reviewer/graph.json`.

## Workflow

1. Refresh and lint the graph:
   - `python3 $KG update`
   - `python3 $KG lint`
   - Stop and report on lint errors.
   - Report lint warnings in one line with counts.
2. Establish the change:
   - Fetch and prune: `git -C <repo> fetch --all --prune`.
   - Record repo, branch, HEAD, base, and dirty-worktree state.
   - Diff: `git -C <repo> diff <base>...HEAD`.
3. Pull prior findings for the change before reviewing:
   - `git -C <repo> diff <base>...HEAD | python3 $KG match --diff - --format json --top 10`
   - Treat each prior finding on a changed file as a recurrence candidate to check.
4. Map impact with Graphify per `~/agents/skills/graphify/SKILL.md`:
   - `graphify update <repo>` or `graphify extract <repo> --code-only` when the index is stale.
   - `graphify affected "<changed symbol>" --depth 2` for callers and consumers.
5. Review the change per `~/agents/review/REVIEW_METHOD.md` and the selected check groups.
6. Research each bug yourself before judging it:
   - Read the code path end to end and cite `file:line`.
   - Prove it with a trace or a red test per `~/agents/CODER.md`.
   - A claim that cannot be proved is reported as unproven, not as a bug.
7. Get the pre-judgement for each proved finding:
   - `python3 $KG match --text "<title and claim>" --file <path> --repo <repo> --format json`
   - Read `prejudgement.basis`, `verdict`, `ask`, and `instruction`.
8. Act on the pre-judgement:
   - **`user-ruling`** → follow the ruling's handling without asking how to handle it; cite the ruling ID.
   - **`conflict`** → show both rulings; ask which holds; supersede the other.
   - **`prior-findings`** → propose the prior outcome as a hypothesis; ask once.
   - **`none`** → propose a fix from the research and the matched reference doc; ask once.
   - A prior `rejected` or `out-of-scope` decision is stated before any fix is proposed.
   - A superseded prior is shown with its current decision; the current decision governs.
9. Propose a fix per finding:
   - Base it on the ruling's or prior's fix, adapted to the current code.
   - Cite the matched prior IDs, outcomes, commits, and reference docs.
   - Show it as a unified diff.
10. Print one table: tracking ID, severity, finding, pre-judgement basis and verdict, matched ruling or prior, reference, patch summary.
11. Ask once for the fixes to apply:
    - **all**, a list of tracking IDs, or **none**.
    - The same question records rulings for findings whose basis was not `user-ruling`.
12. Apply the confirmed fixes to the working tree.
    - Run the repo's tests for the touched files.
    - Report each result with its command output.
13. Record each new ruling once:
    - `python3 $KG remember --about <store/ID> --outcome <o> --confidence verified --title "<rule as a general statement>" --fix "<how>" --rationale "<user's words>" --source <PR or thread URL>`
    - Write the title as the general rule, not the single instance, so it matches the next occurrence.
    - A ruling that contradicts a prior decision adds `--supersedes <prior>`.
    - Do not record a ruling the user did not give; agent inferences use `--confidence hypothesis`.
14. Refresh and re-lint: `python3 $KG update` then `python3 $KG lint`.
15. Persist findings to the review store per `~/agents/review/ISSUE_TRACKING.md` when the review is persisted.

## `/reviewer-kg` maintenance

- `/reviewer-kg build` → `python3 $KG build`.
- `/reviewer-kg update` → `python3 $KG update`.
- `/reviewer-kg lint` → `python3 $KG lint`; resolve each `W2 conflicting decisions` pair by asking the user and recording a supersede.
- `/reviewer-kg remember ...` → pass the arguments to `python3 $KG remember`.

## Rules

- When the user explicitly asks to use `/kg-review`, treat that request as approval to run the graph commands and to append rulings the user gives to memory.
- Ask before applying any fix; apply only the confirmed set.
- Never commit or push.
- Never apply a `NEEDS_REVIEW:cascade` finding without the user's explicit ruling.
- Never edit or delete lines in `memory.jsonl`; supersede instead.
- Never edit review-store files from this skill except through the ISSUE_TRACKING.md procedure.
- A verified user ruling decides handling; a hypothesis or prior finding only suggests it.
- The graph is advisory evidence; each finding still needs proof in current code.
- Keep graph content private: do not copy prior-finding text, evidence, or URLs from other repos into public repos, PR comments, or commits.
- Cite a prior finding to the user by its full tracking ID and store.
