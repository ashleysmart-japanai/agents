# claim-brief

A **claim-brief** describes one review claim to the user in chat. Use it when the user asks about a single claim ("hit me with M5", "explain B11") or when a claim is presented on its own.

- A claim list or a multi-claim report uses its own format; a claim-brief is for one claim.
- Write it in ASD-STE100 Simplified Technical English (§ Writing rules).
- Write every section as terse-srp dot points (`style/DOT_POINT_SRP.md`): one fact per line, no paragraphs.

## Template

```md
**<full tracking ID> [<SEVERITY>]**

**Problem:** <short summary>.

**Origin:** <New in this PR | Made worse by this PR | On main before this PR> — <commit or merge-base evidence>.

**Details:**
- <where: file and symbol, and what the symbol does>
- <what happens: the change, call order, or data flow>
- <effect: the impact>
- <limit: what it does not change>
- <state: fix applied, proposed, or not started>

**Proposed fix:**
- <the concrete change>
- <how it resolves the issue>
- <what to keep unchanged>

**Reviewer suggested:**
- <reviewer (bot or human)>: <the reviewer's fix>
- <why the proposed fix differs, with the prior or ruling>

**Prior evidence:**
- `<store>/<full ID>` — <Outcome>: <the decision, one line> (`<detail path>`)
- `<store>/<full ID>` — <Outcome>: <the decision, one line> (`<detail path>`)
```

- **Heading:** the full tracking ID and severity; nothing else.
- **Problem:** one short sentence: the defect only, with no cause and no fix.
- **Origin:** one line; required in every brief.
  - **New in this PR:** this PR added the code that causes the problem; name the PR commit SHA and what it added.
  - **Made worse by this PR:** the code was on main, and this PR's change exposes or widens the problem; name both.
  - **On main before this PR:** the cited code is unchanged from the merge-base; this PR only brought it into view.
  - Prove it: `git -C <repo> log --oneline $(git -C <repo> merge-base origin/main HEAD)..HEAD -- <file>` and `git -C <repo> blame` on the cited lines.
  - Never present a problem this PR caused as pre-existing, and never omit that this PR's own change is the cause.
  - Not provable (no file, or a PR-level claim): write `Origin: not determined — <reason>`.
- **Details:** one dot point per fact; five or fewer.
  - Where: the file and the real symbol names (`style/QUICK_REF.md`), and what each symbol does.
  - What happens: the change, call order, or data flow that causes the defect.
  - Effect: the impact, and the limits of the impact (for example, "It does not change permission checks").
- **Proposed fix:** the concrete change, and how it resolves the issue; what to keep unchanged.
  - Base it on the decided priors and user rulings from § KG search, not on the reviewer's suggestion.
- **Reviewer suggested:** only when the reviewer's fix differs from the proposed fix.
  - Quote the reviewer's fix in one line and name the reviewer: bot or human.
  - State in one sentence why the proposed fix differs, citing the prior or ruling.
  - Reviewer bot suggestions are almost never right; treat them as a hint to check, never as the fix.
  - A human reviewer's suggestion carries more weight; a user ruling still decides.
- **Prior evidence:** other claims, fixes, proposals, and user decisions that bear on this claim, from § KG search only.
  - Never cite the claim itself, or a copy of it in a stacked PR; it is not its own precedent.
  - The claim's own history (recorded, repeated by a reviewer, extended by a reviewer, its status) goes in Details.
  - One prior per dot point: `store/ID`, outcome, the decision in one line, and the detail path.
  - Cite commits by SHA.
  - State the decision of each prior: fixed, rejected, out of scope, or undecided, and any user ruling.
  - Say which other claim or commit caused this one.
  - No prior found: write `No prior evidence found.`
- Leave out a section that has no content; do not write "N/A".
- Say in Details whether this claim's fix is applied, proposed, or not started.
- No sentence runs across two facts; split it into two dot points.

## KG search

Run this for every claim-brief, before writing it. Do each step; do not shorten it.

1. Use the shared graph: `python3 ~/agents/scripts/build_reviewer_kg.py match --finding <store>/<ID> --top 3`.
   - Do not pass `--out`, and do not build a private copy of the graph.
   - Do not lower `--top` or `--top-refs`.
   - A claim that is not in the graph is read from its review store; `match` still works.
2. No decided prior in the top 3: run it again with `--decided --top 5`, and use the decided results.
3. Open the `detail` file of each kept prior; read its status, justification, reply, and thread.
4. Keep a prior that matches the problem; drop a wording-only match, and say so.
5. A user ruling (`prejudgement` basis `user-ruling`) decides the handling; follow it and cite its ID.
6. Read the `reviewer suggested` line of the claim; compare it with the decided priors.
7. The search fails: write `KG search failed: <error>` in Prior evidence; do not fill the section from other sources.

Never use as prior evidence:

- the conversation, the user's current instruction, or the PR description;
- the claim itself, or its copy in a stacked PR;
- an undecided prior presented as a decision;
- a result from a private or rebuilt graph copy.

## Apply it

- "Apply it", said while going through single claims, approves the proposed fix for the current claim.
- "Apply all" or a list of tracking IDs approves those claims.
- Do the fix in a background sub-agent, not in the main conversation.
  - The sub-agent prompt holds: the claim ID, the problem, the proposed fix, the files to touch, and the focused test command.
  - The sub-agent applies the fix and runs the focused tests.
  - The sub-agent does not commit, push, change claim status, or start other work.
- Return to the user at once, while the sub-agent works:
  - present the next unaddressed claim as a claim-brief, or
  - state "All claims are addressed." with one line per claim: ID and applied, applying, declined, or deferred.
- A claim is addressed when the user approved, declined, or deferred it.
- Run one sub-agent at a time on a file; queue a second fix that touches the same file.
- Consolidate each sub-agent when it finishes:
  - Claude: the sub-agent works on the branch in the main checkout, with no worktree; verify its diff and its test result.
  - Codex: the sub-agent may use a worktree; consolidate its changes into the main checkout as soon as it finishes.
  - Report one line: claim ID, files changed, test command and result.
  - Report a failed test or a conflict to the user; do not retry the fix without the user's answer.

## Writing rules (ASD-STE100)

- Write short sentences: 20 words or fewer for an instruction, 25 words or fewer for a description.
- Write one topic in each paragraph; use six sentences or fewer in a paragraph.
- Use the active voice.
- Use the simple tenses: present, past, and future.
- Write one instruction in each sentence; use the imperative for an instruction.
- Use each word with one meaning only; use the same word for the same thing each time.
- Use technical names (code symbols, file names, product names) as they are written.
- Use the articles "the", "a", and "an"; do not omit them to save words.
- Do not use a noun cluster of more than three words; split it with a preposition.
- Do not use phrasal verbs ("set up", "carry out"); use one verb ("configure", "do").
- Do not use the "-ing" form of a verb, except in a technical name.
- Write positive statements where possible; state what is true.
- Do not use slang, jargon that is not a technical name, or invented terms.

## Example

```md
**M5.0aBcDeFgHiJkLmNoPqRsTu [LOW]**

**Problem:** The access-warning comment is attached to the wrong method.

**Origin:** New in this PR — commit `1a2b3c4d5e6` inserted `getOwnerByIdUnsafe()` below the existing comment.

**Details:**
- `orders.service.ts` `getOwnerByIdUnsafe()` reads only the account and project IDs for the permission check.
- `orders.service.ts` `getByIdUnsafe()` reads the full order record, with its payment settings.
- The warning comment now sits above `getOwnerByIdUnsafe()`.
- `getByIdUnsafe()` has no warning that authorization must succeed first.
- It does not change permission checks or data access.
- The fix is proposed; it is not applied.

**Proposed fix:**
- Move the warning comment to `getByIdUnsafe()`.
- Add a comment to `getOwnerByIdUnsafe()` that it supports controller authorization.
- Keep both method names.

**Reviewer suggested:**
- Review bot: rename `getOwnerByIdUnsafe()`.
- The rename does not move the comment; `shop-pr-188/I5.1aBcDeFgHiJkLmNoPqRsTu` kept the method name.

**Prior evidence:**
- `shop-pr-188/I5.1aBcDeFgHiJkLmNoPqRsTu` — Fixed: commit `1a2b3c4d5e6` added the ownership-only method for permission checks (`~/reviews/shop-pr-188/I5.1aBcDeFgHiJkLmNoPqRsTu.md`)
- `shop-pr-150/D2.2bCdEfGhIjKlMnOpQrStUv` — Fixed: each `Unsafe` read method carries its own authorization warning (`~/reviews/shop-pr-150/D2.2bCdEfGhIjKlMnOpQrStUv.md`)
```
