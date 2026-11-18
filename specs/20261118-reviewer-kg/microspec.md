# Reviewer knowledge graph and KG review

- **What:** a rebuildable reviewer KG of prior review findings and reference guidance, with append-only memory, lint, and a `/kg-review` skill that researches each bug, gives a pre-judgement from the user's prior rulings, and proposes fixes.
- **When:** 2026-11-18.
- **Owner:** repository maintainer.

## Problem

- Review findings are recorded per PR in `~/reviews/<store>/` and are not reused across PRs.
- The same bug classes recur across PRs, and each review rediscovers them and the fix that was accepted last time.
- Decisions on findings (fixed, rejected, out of scope, not reproduced) live in detail-file prose; nothing looks them up when a similar claim reappears.
- A later decision can contradict an earlier one, and nothing records which decision holds.
- The user rules on the same kind of issue again and again because no ruling carries to the next review.
- The guidance in `reference/` (anti-patterns, design principles, design patterns, security principles) is not linked to the findings that exemplify it.
- The review store holds findings from private repositories; this repository is public.

## Objective

- **Decision:** build a graph that links prior findings, their decisions, the code files they touch, and the reference guidance. Keep new decisions in an append-only memory that can supersede, but never delete, a prior result. Review through a skill that consults the graph before proposing each fix.
- **Success:** the user rules on an issue once; the next review of a matching issue returns that ruling as a pre-judgement and follows it without asking again.
- **Success:** for a new finding without a ruling, the reviewer surfaces the closest prior decisions and reference guidance and proposes a fix that cites them.

## Terms

- **Review store:** one `~/reviews/<store>/` directory holding `review.md` and `<ID>.md` detail files (`review/ISSUE_TRACKING.md`).
- **Finding:** one `<ID>.md` detail file.
- **Outcome:** the decision class derived from a finding's status: `fixed`, `rejected`, `out-of-scope`, `not-reproduced`, `invalid`, `obsolete`, `deferred`, `undecided`.
- **Memory entry:** one line of `memory.jsonl`; a decision, supersede, or note added after the review store was written.
- **Supersede:** a newer item replaces a prior decision; the prior item stays in the graph with a link to its successor.
- **Current decision:** the item reached by following supersede links from a prior item to the newest one.
- **Ruling:** a `verified` memory entry recording how the user decided an issue should be handled.
- **Pre-judgement:** the verdict `match` derives before the agent asks: from a current ruling, else from agreeing prior findings, else none.

## Requirements

- [ ] **R1 — Builder:** `scripts/build_reviewer_kg.py` (Python standard library only) builds the graph from the review store root and the reference root.
- [ ] **R2 — Private output:** the graph, cache, report, and memory are written to `~/agents-secret/kg/reviewer/`, outside this public repository.
- [ ] **R3 — Rebuild and update:** `build` reparses every source; `update` reparses only review stores and reference docs whose files changed, and drops stores that no longer exist.
- [ ] **R4 — Finding fields:** each finding node carries its ID, store, repo, PR, type, severity, status, outcome, title, file and line, description, evidence, fix, fixed, justification, reviewer acknowledgement, pushback, scope, commit, reviewer, thread, and detail-file path.
- [ ] **R5 — Graph links:** the graph links finding → store → repo, finding → code file, finding → reviewer, finding → outcome, finding → parent finding for cascades, and reference → category.
- [ ] **R6 — Inferred links:** finding → similar finding and finding → reference links are marked `INFERRED` with a similarity score; an explicit multi-word reference name in the claim text is an `EXTRACTED` link.
- [ ] **R7 — Graphify compatible:** `graph.json` is readable by `graphify explain|query|path --graph <path>`.
- [ ] **R8 — Match:** `match` takes claim text, a unified diff, or touched file paths, and returns ranked prior findings with outcome, fix, fixed, justification, reviewer acknowledgement, thread, and linked references, plus ranked reference docs.
- [ ] **R9 — Match by file:** a prior finding on the same file path ranks above one that only shares wording.
- [ ] **R10 — Memory is append-only:** `remember` appends one entry to `memory.jsonl`; no command rewrites or deletes a memory line or a review-store file.
- [ ] **R11 — Supersede keeps history:** a supersede entry links the newer item to each prior item; the prior item keeps its original fields and gains `superseded_by`.
- [ ] **R12 — Supersede chains:** a superseded memory entry can itself be superseded; the current decision is the end of the chain.
- [ ] **R13 — Superseded items are flagged in search:** `match` still returns a superseded prior item, ranks it below current items, and shows its current decision.
- [ ] **R14 — Fixed vocabulary:** memory outcome and confidence values come from fixed vocabularies; `remember` rejects other values at write time.
- [ ] **R15 — Confidence:** every memory entry carries `verified` (a human confirmed it), `hypothesis` (agent-inferred), or `reported` (an external claim).
- [ ] **R16 — Lint errors:** `lint` exits non-zero on invalid memory lines, memory references to missing nodes, supersede cycles, and out-of-vocabulary values.
- [ ] **R17 — Lint warnings:** `lint` warns on items superseded by more than one current item, similar findings with conflicting decisions and no supersede, fixed findings without fix text, non-canonical status tokens, a graph older than its sources, and summary rows without a detail file.
- [ ] **R18 — KG review skill:** `/kg-review` refreshes and lints the graph, reviews the change, matches each finding to prior decisions and reference guidance, and proposes a fix per finding citing what it matched.
- [ ] **R19 — Apply on confirmation:** the skill applies proposed fixes only after the user confirms all, or a listed set of tracking IDs; it never commits or pushes.
- [ ] **R20 — Write-back:** each user ruling on a proposed fix is recorded with `remember` as `verified`, superseding any prior decision it contradicts.
- [ ] **R21 — Prior rejections surface:** a proposed fix whose closest prior match was rejected or ruled out of scope says so and asks before proposing the same change.
- [ ] **R22 — Research first:** the skill proves each bug in current code with a `file:line` trace or a red test before giving a pre-judgement.
- [ ] **R23 — Pre-judgement from a ruling:** when a current ruling matches the claim, or is recorded about a matching prior finding, `match` returns that ruling's verdict and handling with `ask: false`.
- [ ] **R24 — Pre-judgement without a ruling:** when no ruling matches, `match` returns the agreeing outcome of the closest decided prior findings, or no verdict, with `ask: true`.
- [ ] **R25 — Conflicting rulings:** when current rulings with different outcomes match at near-equal scores, `match` returns verdict `conflict` with `ask: true`.
- [ ] **R26 — Hypotheses do not decide:** a memory entry with confidence `hypothesis` or `reported` never produces `ask: false`.
- [ ] **R27 — Ruled once:** the skill follows a `user-ruling` pre-judgement without asking how to handle the issue, and asks only which fixes to apply.

## Scope

- In scope: the builder script and its tests, the memory file contract, the lint checks, the `/kg-review` skill and its command mappings.
- Out of scope: vector embeddings; model-backed semantic extraction; edge-strength spreading activation; writing to the review store from the builder; hosting the graph.
- Boundary: changes `scripts/`, `tests/`, `skills/`, `skills/SKILL.md`, `specs/`, and the `CODER.md` skill map; reads `~/reviews/` and `reference/` read-only; writes only `~/agents-secret/kg/reviewer/`.

## Acceptance Criteria

- [ ] AC1: `build` on a fixture store parses every detail file into a finding node with outcome, file, line, evidence, and wrapped description lines intact (R1, R4).
- [ ] AC2: the default output directory is under `~/agents-secret/` (R2).
- [ ] AC3: `update` after one detail file changes reports one store reparsed; after a store is removed it reports that store removed (R3).
- [ ] AC4: the fixture graph holds `cites`, `similar_to`, `touches`, `decided_as`, and `in_store` links (R5, R6).
- [ ] AC5: `graphify explain <finding node> --graph graph.json` exits 0 and lists the finding's links (R7).
- [ ] AC6: a claim about an inline `?? {}` fallback on `src/api/orders.ts` returns both prior decisions on that file and not the unrelated SQL finding, and ranks Defensive Duct-Taping in the reference matches (R8, R9).
- [ ] AC7: after a supersede, the memory file holds one line, the prior finding keeps outcome `rejected`, and gains `superseded_by` (R10, R11).
- [ ] AC8: superseding the first memory entry makes the second entry the current decision, and both entries remain nodes (R12).
- [ ] AC9: `match` returns the superseded finding with its current decision's outcome (R13).
- [ ] AC10: `remember --outcome kinda-fixed` exits non-zero and appends nothing (R14).
- [ ] AC11: a memory entry without a vocabulary confidence is an `E4 vocabulary` lint error (R15, R16).
- [ ] AC12: lint reports an invalid JSON line, a dangling reference, and a two-node supersede cycle as errors and exits 1 (R16).
- [ ] AC13: lint reports a fixed-vs-rejected similar pair once, a summary row without a detail file, and a stale graph after a store file changes (R17).
- [ ] AC14: `/kg-review` on a branch lists each finding with its prior match, outcome, reference, and proposed patch, and asks before applying (R18, R19, R21).
- [ ] AC15: after the user rules on a fix, `memory.jsonl` gains a `verified` entry about that finding, and the next `match` on the same claim returns it (R20).
- [ ] AC16: before any ruling, `match` on a fixture claim returns `ask: true` (R24).
- [ ] AC17: after one verified ruling about a prior finding, a differently worded claim on the same file returns basis `user-ruling`, the ruling's verdict, and `ask: false` (R23).
- [ ] AC18: after that ruling is superseded, the same claim returns the newer ruling's verdict, and the older ruling is still a node (R12, R23).
- [ ] AC19: a matching `hypothesis` memory entry does not produce basis `user-ruling` (R26).
- [ ] AC20: two verified rulings with different outcomes on the same claim return verdict `conflict` (R25).
- [ ] AC21: a `/kg-review` run with a `user-ruling` pre-judgement cites the ruling ID and asks only which fixes to apply (R22, R27).

## Verification

- `python3 -m unittest tests/test_build_reviewer_kg.py` → all tests pass (AC1–AC13, AC16–AC20).
- `python3 scripts/build_reviewer_kg.py build` → writes `~/agents-secret/kg/reviewer/graph.json` and prints node, link, finding, and reference counts.
- `python3 scripts/build_reviewer_kg.py lint` → exit 0 with zero errors on the live store.
- `graphify explain "Exception Swallowing" --graph ~/agents-secret/kg/reviewer/graph.json` → lists findings linked to that anti-pattern.
- `git -C ~/agents ls-files | grep -c agents-secret` → 0; no graph, cache, or memory file is tracked in this repository.
- One `/kg-review` run on a real branch → proposals cite prior findings; the confirmed ruling appears in `memory.jsonl` (AC14, AC15).
- A second `/kg-review` run on a branch with a matching issue → pre-judgement `user-ruling`, no handling question (AC21).

## Related

- `review/ISSUE_TRACKING.md` — review store format the builder reads.
- `review/REVIEW_METHOD.md` — finding grammar, status tokens, and ID prefixes.
- `skills/graphify/SKILL.md` — Graphify usage and the ontology-enhanced review reference.
- `scripts/build_knowledge_graphs.py` — the FDE / DS / analyst knowledge graphs; separate graph, same repository.
- MOKA knowledge-architecture guide (internal, 2026-11-12) — source of the map-not-copy, supersede-not-delete, confidence-per-link, fixed-vocabulary, rules-in-code, and write-back-every-run principles applied here.
