# Issue Tracking

This document specifies the **persisted `review.md` store**: how the finding grammar defined in [REVIEW_METHOD.md § Finding Grammar](REVIEW_METHOD.md#finding-grammar) is applied to the on-disk review directory. The status tokens, severity values, and ID prefixes are defined there and imported here — this file does not redefine them; it says where they are written and how the files are kept in sync.

- Store review output in `~/reviews/<repo>-pr-<number>/`.
- Use `review.md` as the index file. It contains only `# META` and `# SUMMARY`.
- Use `feedback.md` as the external feedback ingress file.
- Store every issue's detail record in its own `<ID>.md` file.
- `review.md` never contains detail records.
- Migrate legacy files from `~/reviews/<repo>-pr-<number>-review.md`.
- Preserve all issue history during migration.
- Start `review.md` with `** WARNING do not delete review entries ever **`.
- Put `# META` first.
- Put `# SUMMARY` second.
- No other top-level sections.

## Feedback ingress

- `feedback.md` is a sibling of `review.md` in the review directory.
- External systems (CI, other agents, human notes) write feedback points to `feedback.md`.
- `feedback.md` is append-only from external writers. The reviewer does not edit it directly.
- Each feedback entry should include enough context to trace back to its source.

### Processing feedback

Run this procedure during Stage 0, after reading existing review state:

1. Read PR comments from the PR's own scope for new feedback. Review all comments and update `review.md` accordingly.
   - Do not filter anyone's comments. Include all commenters, including bot accounts.
2. Run `wc -l ${FEEDBACK_FILE}` to check if `feedback.md` has content.
3. If the file has content:
   - Move `feedback.md` to `feedback.lock.md` (atomic swap to prevent concurrent writers from losing entries).
   - Touch `feedback.md` to create a new blank file (external writers can resume appending immediately).
4. Read `feedback.lock.md`, triage each feedback point, and open or update review issues using the normal opening flow.
5. Delete `feedback.lock.md` after all entries have been processed.

## Review handling rules

### Never ignore review points

- Every review point from any source (PR comments, feedback.md, reviewer findings) is tracked.
- No finding is silently dropped, filtered, or skipped.

### NEEDS_REVIEW usage

`NEEDS_REVIEW` has strict limits. It is for engineering concerns only.

- `NEEDS_REVIEW:reviewer` — the reviewer is uncertain whether a finding is valid and needs the user to decide.
- `NEEDS_REVIEW:coder` — the coder believes the fix is problematic and is pushing back with evidence.

When asked to provide a list of open `NEEDS_REVIEW` items, list both `:reviewer` and `:coder` items. For each, explain with evidence the problem and the reason for the `NEEDS_REVIEW` status.

### Coder obligations for OPEN issues

- Before acting on any issue, read the full `<ID>.md` detail file. Do not decide, push back, or categorise based on the title alone.
- If an issue is `OPEN`, the coder fixes it. No deferral.
- The coder may push back by moving to `NEEDS_REVIEW:coder` only for valid engineering reasons:
  - The fix breaks prior fixes.
  - The fix will regress security.
  - The fix has a logical mistake.
  - The fix violates the design.
- These are not valid reasons to push back:
  - "Too much work."
  - "Too big a change."
  - "Not in scope for this PR."
- When the coder pushes back, they must update the detail record in `<ID>.md` with evidence explaining the problem that prevents the fix.

## Review directory layout

- `review.md` is the index: META and SUMMARY only.
- Every issue gets its own `<ID>.md` file at creation time.
- No detail records in `review.md`. Ever.
- One detail file per issue ID.

## META section

- `# META` stores grepable review metadata.
- Place `# META` immediately after the warning line.
- Required: `repo:`.
- Required: `pr:`.
- Required: `branch:`.
- Required: `base:`.
- Required: `head:`.
- Required: `reviewed:`. Last review datetime as `<yyyy-mm-dd HH:MM>`. Overwrite on each review, do not append.
- Required: `open:`.
- `open:` contains every not-closed issue ID, comma-separated with no spaces.
- Not-closed statuses are `OPEN`, `NEEDS_REVIEW:reviewer`, `NEEDS_REVIEW:coder`, and `DEFERRED`.
- If there are no not-closed issues, write `open:none`.
- Update `open:` when an issue opens, closes, reopens, moves to `NEEDS_REVIEW:reviewer`, moves to `NEEDS_REVIEW:coder`, moves to `DEFERRED`, or moves to `WILL_NOT_FIX`.
- Do not list closed IDs in `open:`. Closed statuses are `CLOSED verified:<yyyy-mm-dd>` and `WILL_NOT_FIX`.
- The `open:` key name is legacy; it tracks not-closed IDs, not only issues with status `OPEN`.
- Add other grepable metadata only as `key:value` lines under `# META`.

## SUMMARY section

- Keep `# SUMMARY` as one flat checkbox list.
- Do not add headings.
- Do not add tables.
- Do not add verdicts.
- Do not add checks.
- Do not add prose.
- Keep exactly one summary item per issue ID.
- Each item uses the finding grammar line format from [REVIEW_METHOD.md § Finding Grammar](REVIEW_METHOD.md#finding-grammar): `- [<x| >] <ID> - <STATUS> [<SEVERITY>] - <title> \`file:line\``.
- The status tokens, severity values, and ID prefixes are defined in REVIEW_METHOD.md. Do not redefine them here.
- The `<title>` is a short label, not a description. Keep it under one line. Full details go in `<ID>.md`.
- Use `[ ]` for not-closed issues; `[x]` for closed issues. Do not use `[?]`.
- Not-closed statuses: `OPEN`, `NEEDS_REVIEW:reviewer`, `NEEDS_REVIEW:coder`, `DEFERRED`.
- Closed statuses: `CLOSED verified:<yyyy-mm-dd>`, `WILL_NOT_FIX`.
- Do not put a category token after the ID.
- Put location keys in the title text.
- Sort by prefix order (`B`, `SEC`, `I`, `S`, `O`, `D`, `T`, `M`), then by issue ID within each prefix.
- Use `- none` when there are no issues.
- Keep `# SUMMARY` in `review.md`.
- Never move summary items out of `review.md`.
- Align checkbox state with `open:` in `# META`.
- Align summary status with the `status:` in the issue's `<ID>.md` file.

## Detail files (`<ID>.md`)

- Every issue gets its own `<ID>.md` file at creation time.
- The file contains the full detail record for that issue.
- Required field: `ID:`.
- Required field: `type:`.
- Required field: `severity:`.
- Required field: `title:`.
- Required field: `file:`.
- Required field: `pr:`.
- Required field: `status:`.
- Required field: `description:`.
- Required field: `evidence:`.
- Required field: `fix:`.
- Required field: `reverify:`.
- The detail `status:` value must match the status in that issue's `# SUMMARY` item.
- Valid detail statuses are `OPEN`, `NEEDS_REVIEW:reviewer`, `NEEDS_REVIEW:coder`, `DEFERRED`, `CLOSED verified:<yyyy-mm-dd>`, and `WILL_NOT_FIX`.
- Never delete a detail file.
- Never truncate a detail file to a stub.
- Update the detail file in place when status changes.

## Opening an issue

- Give every finding a unique ID.
- Include enough context to re-verify the finding later.
- Use the ID prefix rules from `# SUMMARY`.
- Severity values are `CRITICAL`, `HIGH`, `MEDIUM`, and `LOW`.
- Always include the actual code snippet or command output that proves the issue.
- Never open an issue without evidence.
- Create `<ID>.md` with the full detail record.
- Add the ID to the `open:` line in `# META`.
- Add one unchecked `- [ ] <ID> - OPEN [<SEVERITY>] - <title>` item to the flat list in `# SUMMARY`.
- Include `pr:` in the detail record when the issue comes from cross-PR parent/child tracking.
- Use `NEEDS_REVIEW:reviewer` when the reviewer is uncertain or needs human input.
- Use `NEEDS_REVIEW:coder` when the coder pushes back with evidence that the fix is problematic.
- Never drop an uncertain finding silently.

## Closing an issue

- When a fix is confirmed, update the entries in place.
- Remove the ID from the `open:` line in `# META`.
- Change its `# SUMMARY` prefix to `- [x] <ID> - CLOSED verified:<yyyy-mm-dd> [<SEVERITY>] - `.
- Update `status:` in `<ID>.md` to `CLOSED verified:<yyyy-mm-dd>`.
- Add `commit:`, `reverify:`, and `fixed:` to `<ID>.md` if missing.
- Keep the original summary, description, file reference, PR reference, and evidence intact.

## Changing an issue status

- The reviewer may move an issue to `NEEDS_REVIEW:reviewer` when uncertain or needing human input.
- The coder may move an issue to `NEEDS_REVIEW:coder` when pushing back on a fix with evidence.
- Only the user/human may move an issue to `DEFERRED`. Agents must never set this state.
- Only the user/human may move an issue to `WILL_NOT_FIX`. Agents must never set this state.

For `NEEDS_REVIEW:reviewer`:

- Keep or add the ID in the `open:` line in `# META`.
- Keep the `# SUMMARY` checkbox unchecked and change the summary status to `NEEDS_REVIEW:reviewer`.
- Update `status:` in `<ID>.md` to `NEEDS_REVIEW:reviewer`.

For `NEEDS_REVIEW:coder`:

- Keep or add the ID in the `open:` line in `# META`.
- Keep the `# SUMMARY` checkbox unchecked and change the summary status to `NEEDS_REVIEW:coder`.
- Update `status:` in `<ID>.md` to `NEEDS_REVIEW:coder`.
- Add evidence in `<ID>.md` explaining why the fix is problematic.

For `DEFERRED` (human-only — agents must never set this state):

- Keep or add the ID in the `open:` line in `# META`.
- Keep the `# SUMMARY` checkbox unchecked and change the summary status to `DEFERRED`.
- Update `status:` in `<ID>.md` to `DEFERRED`.
- Add `defer:<yyyy-mm-dd> - <reason>` in `<ID>.md` when the reason is known.

For `WILL_NOT_FIX` (human-only — agents must never set this state):

- Remove the ID from the `open:` line in `# META`.
- Change its `# SUMMARY` prefix to `- [x] <ID> - WILL_NOT_FIX [<SEVERITY>] - `.
- Update `status:` in `<ID>.md` to `WILL_NOT_FIX`.
- Add `decision:<yyyy-mm-dd> - <reason>` in `<ID>.md` when the reason is known.

## Reopening an issue

If a fix is reverted or no longer holds:

- Add the ID back to the `open:` line in `# META`.
- Change its `# SUMMARY` prefix to `- [ ] <ID> - OPEN [<SEVERITY>] - `.
- Update `status:` in `<ID>.md` back to `OPEN`.
- Add `reopened:<yyyy-mm-dd> - <reason and sha if known>` in `<ID>.md`.

## Structural rules

- Never rewrite the review directory from scratch.
- Never put inline detail records in `review.md`.
- Never delete `<ID>.md` files.
- Never truncate `<ID>.md` files to stubs.
- Never move `# SUMMARY` out of `review.md`.
- Never remove an issue from `# SUMMARY`.
- Never create index sections beyond `# META` and `# SUMMARY`.
- Do not create a separate cross-PR tracking section. Cross-PR parent/child context belongs in each issue's `pr:` field.
- Multiple agents work with these files concurrently. Structural changes break their references.
- State must match across all three places:
  - `open:` in `# META`
  - checkboxes and status tokens in `# SUMMARY`
  - `status:` in the issue's `<ID>.md` file

## Review log

- Keep a persistent `log.md` alongside `review.md`.
- `log.md` records what was checked at each commit.
- `log.md` is append-only.
- Never delete existing `log.md` entries.
- Never edit existing `log.md` entries.
- Never reorder existing `log.md` entries.
- Every `log.md` entry is a permanent record.
- Append a new entry every time the reviewer checks the code.
- Append an entry even when there are no new commits.
- Each file checked gets one line.
- Log only files actually read or verified in that pass.
- Do not log every file in the diff unless every file was checked.
- Use this log line format: `<datetime> - <git-hash> - <issue-id>:<status> - <path> - <summary of check>`.
- Use `log.md` to audit which files were checked.
- Use `log.md` to audit what was checked in each file.

## Reference example

````md
~/reviews/<repo>-pr-<number>/
  review.md
  feedback.md
  B1.md
  B2.md
  log.md

# review.md
** WARNING do not delete review entries ever **

# META
repo:<repo>
pr:<number>
branch:<branch>
base:<base-branch>
head:<head-sha>
reviewed:<yyyy-mm-dd HH:MM>
open:B1

# SUMMARY
- [ ] B1 - OPEN [HIGH] - Short title `path/file.ts:10`
- [x] B2 - CLOSED verified:2026-06-11 [MEDIUM] - Short title `path/file.ts:42`

# B1.md
## B1
ID:B1
type:BUG
severity:HIGH
title:Short title
file:`path/file.ts:10`
pr:`#<number>`
status:OPEN

description:
<description of the issue>

evidence:
```evidence
<code snippet or command output showing the problem>
```

fix:<what needs to change>
reverify:<exact grep/read/test command or file:line to check>

# B2.md
## B2
ID:B2
type:BUG
severity:MEDIUM
title:Short title
file:`path/file.ts:42`
pr:`#<number>`
status:CLOSED verified:2026-06-11
commit:`<short sha>` or `squash to <sha>`

description:
<original description - preserved unchanged>

evidence:
```evidence
<original proof snippet or command output - preserved unchanged>
```

fix:<original fix guidance - preserved unchanged>
reverify:<exact grep/read/test command or file:line to check>
fixed:<one-line description of the change>

# log.md
2026-06-11 09:00:20 - df9fc5386 - B1:OPEN - path/file.ts - open issue still present
2026-06-11 09:03:14 - df9fc5386 - B2:CLOSED verified:2026-06-11 - path/file.ts - fix verified
````
