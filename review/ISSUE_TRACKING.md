# Issue Tracking

- Store review output in `<working-directory>/reviews/<repo>-pr-<number>/`.
- Use `review.md` as the required index file.
- Store archived closed detail records as sibling `<ID>.md` files.
- Migrate legacy files from `<working-directory>/reviews/<repo>-pr-<number>-review.md`.
- Preserve all issue history during migration.
- Start `review.md` with `** WARNING do not delete review entries ever **`.
- Put `# META` first.
- Put `# SUMMARY` second.
- Put `# DETAILS` third.
- No other top-level sections.
- No open/closed detail sections.
- No body moves for ordinary state changes.
- Move issue bodies only for archive and unarchive operations.

## Review directory layout

- Use the reference example for exact file layout.
- Keep not-closed detail records inline in `review.md`.
- Archive only verified-closed detail records.
- Archive only when the review tracks more than 15 issue IDs.
- Count issue IDs from `# SUMMARY`.
- Ignore `- none` when counting issue IDs.
- Store archived detail records as sibling `<ID>.md` files.
- Link archived detail records from `# DETAILS`.
- Keep one detail record per issue ID.
- Never duplicate one detail record inline and archived.

## META section

- `# META` stores grepable review metadata.
- Place `# META` immediately after the warning line.
- Required: `repo:`.
- Required: `pr:`.
- Required: `branch:`.
- Required: `base:`.
- Required: `head:`.
- Required: `reviewed:`.
- Required: `open:`.
- `open:` contains every not-closed issue ID, comma-separated with no spaces.
- Not-closed statuses are `OPEN`, `NEEDS_REVIEW`, and `DEFERRED`.
- If there are no not-closed issues, write `open:none`.
- Update `open:` when an issue opens, closes, reopens, moves to `NEEDS_REVIEW`, moves to `DEFERRED`, or moves to `WILL_NOT_FIX`.
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
- Use prefix format `- [<IS_CLOSED>] <ID> - <STATUS> [<SEVERITY>] - `.
- Use `[ ]` for not-closed issues.
- Use `[x]` for closed issues.
- Do not use `[?]`.
- Not-closed statuses: `OPEN`, `NEEDS_REVIEW`, `DEFERRED`.
- Closed statuses: `CLOSED verified:<yyyy-mm-dd>`, `WILL_NOT_FIX`.
- `OPEN` means coder must fix.
- `NEEDS_REVIEW` means user/human must review.
- `DEFERRED` means user chose to fix later.
- `CLOSED verified:<yyyy-mm-dd>` means fixed and verified.
- `WILL_NOT_FIX` means user rejected the issue.
- Do not put a category token after the ID.
- ID prefix `B` means `BUG`.
- ID prefix `SEC` means `SECURITY`.
- ID prefix `I` means `ISSUE`.
- ID prefix `S` means `SCOPING_AUTH`.
- ID prefix `O` means `OPTIMIZATION`.
- ID prefix `D` means `DESIGN`.
- ID prefix `T` means `TEST`.
- ID prefix `M` means `MINOR`.
- Write human summary text after the prefix.
- Put location keys in the summary text.
- Sort by prefix order: `B`, `SEC`, `I`, `S`, `O`, `D`, `T`, `M`.
- Sort by issue ID within each prefix.
- Use `- none` when there are no issues.
- Keep `# SUMMARY` in `review.md`.
- Never move summary items into archive files.
- Add `archive:<ID>.md` for archived closed issues.
- Remove `archive:<ID>.md` when unarchiving or reopening.
- Align checkbox state with `open:` in `# META`.
- Align summary status with the detail `status:`.

## DETAILS section

- `# DETAILS` contains one stable full record for every issue ID.
- Keep not-closed issue records inline under `# DETAILS`.
- Closed issue records may stay inline under `# DETAILS`.
- Do not move detail records for ordinary state changes.
- Only move detail records during explicit archive and unarchive operations.
- Archive only verified-closed issue records.
- Archive verified-closed issue records only when the review tracks more than 15 issue IDs.
- Store each archived issue record in one sibling `<ID>.md` file.
- Link each archived issue from `review.md` `# DETAILS`.
- Use one `# DETAILS` link per archived issue.
- Use a full issue record for every inline detail.
- Use a full issue record for every archived detail.
- Required field: `ID:`.
- Required field: `type:`.
- Required field: `severity:`.
- Required field: `summary:`.
- Required field: `file:`.
- Required field: `pr:`.
- Required field: `status:`.
- Required field: `description:`.
- Required field: `evidence:`.
- Required field: `fix:`.
- Required field: `reverify:`.
- The detail `status:` value must match the status in that issue's `# SUMMARY` item.
- Valid detail statuses are `OPEN`, `NEEDS_REVIEW`, `DEFERRED`, `CLOSED verified:<yyyy-mm-dd>`, and `WILL_NOT_FIX`.
- If the review has never recorded any issues, write `- none` under `# DETAILS`.
- Do not replace an archived detail file with a metadata-only stub.

## Opening an issue

- Give every finding a unique ID.
- Include enough context to re-verify the finding later.
- Use the ID prefix rules from `# SUMMARY`.
- Severity values are `CRITICAL`, `HIGH`, `MEDIUM`, and `LOW`.
- Always include the actual code snippet or command output that proves the issue.
- Never open an issue without evidence.
- Add the ID to the `open:` line in `# META`.
- Add one unchecked `- [ ] <ID> - OPEN [<SEVERITY>] - <summary>` item to the flat list in `# SUMMARY`.
- Add one full inline detail record under `# DETAILS`.
- Keep the detail record inline while the issue is not closed.
- Do not create `<ID>.md` for a new or not-closed issue.
- Include `pr:` in the detail record when the issue comes from cross-PR parent/child tracking.
- Use `NEEDS_REVIEW` when the agent is uncertain.
- Use `NEEDS_REVIEW` when the agent needs human input.
- Never drop an uncertain finding silently.

## Closing an issue

- When a fix is confirmed, update the existing entries in place.
- Do not move the detail record as part of closing.
- Remove the ID from the `open:` line in `# META`.
- Change its `# SUMMARY` prefix to `- [x] <ID> - CLOSED verified:<yyyy-mm-dd> [<SEVERITY>] - `.
- Change the detail status from its current value to `status:CLOSED verified:<yyyy-mm-dd>`.
- Add `commit:`, `reverify:`, and `fixed:` if missing.
- Keep the original summary, description, file reference, PR reference, and evidence intact.
- Do not move the issue body as part of the close itself.
- Archive the verified-closed issue only if the review tracks more than 15 issue IDs.
- Keep the verified-closed issue inline if the review tracks 15 or fewer issue IDs.

## Changing an issue status

- Agents may move an issue to `NEEDS_REVIEW` when they are uncertain.
- Agents may move an issue to `NEEDS_REVIEW` when they need human input.
- Only the user/human may move an issue to `DEFERRED`.
- Only the user/human may move an issue to `WILL_NOT_FIX`.

For `NEEDS_REVIEW`:

- Keep or add the ID in the `open:` line in `# META`.
- Keep the `# SUMMARY` checkbox unchecked and change the summary status to `NEEDS_REVIEW`.
- Change the detail status to `status:NEEDS_REVIEW`.

For `DEFERRED`:

- Keep or add the ID in the `open:` line in `# META`.
- Keep the `# SUMMARY` checkbox unchecked and change the summary status to `DEFERRED`.
- Change the detail status to `status:DEFERRED`.
- Add `defer:<yyyy-mm-dd> - <reason>` in the same detail record when the reason is known.

For `WILL_NOT_FIX`:

- Remove the ID from the `open:` line in `# META`.
- Change its `# SUMMARY` prefix to `- [x] <ID> - WILL_NOT_FIX [<SEVERITY>] - `.
- Change the detail status to `status:WILL_NOT_FIX`.
- Add `decision:<yyyy-mm-dd> - <reason>` in the same detail record when the reason is known.

## Reopening an issue

If a fix is reverted or no longer holds:

- Add the ID back to the `open:` line in `# META`.
- Change its `# SUMMARY` prefix to `- [ ] <ID> - OPEN [<SEVERITY>] - `.
- Change the detail status back to `status:OPEN`.
- Add `reopened:<yyyy-mm-dd> - <reason and sha if known>` in the same detail record.
- If the issue was archived in `<ID>.md`, restore the full detail record inline under `# DETAILS`.
- If the issue was archived in `<ID>.md`, replace the archive link with the inline record.
- Remove the `archive:<ID>.md` marker from the `# SUMMARY` item when the issue is unarchived or reopened.

## Re-checking after a push or rebase

- Pull the latest code.
- Read every inline detail record.
- Read every archived closed sibling detail file linked from `# DETAILS`.
- Re-verify every closed issue using its documented check.
- Reopen any closed issue whose fix was reverted.
- Re-check every not-closed issue listed in `open:`.
- Close any not-closed issue that is now fixed.
- Add new findings as new `# SUMMARY` items.
- Add new findings as new `# DETAILS` records.
- Update the flat issue list under `# SUMMARY`.

## Archiving closed details into files

- Archive closed issue details into sibling files only when `review.md` becomes too large.
- Archive closed issue details only if the review tracks more than 15 issue IDs.
- Count issue IDs in `# SUMMARY`.
- Exclude `- none` from the issue count.
- Do not archive details when the count is 15 or fewer.
- Select only verified-closed issues with `status:CLOSED verified:<yyyy-mm-dd>`.
- Create one sibling archive file per selected closed issue.
- Name each archive file `<ID>.md`.
- Move the full existing `## <ID>` record into the archive file.
- Do not rewrite issue history during archive.
- Preserve description, evidence, fix, reverify, commit, and fixed fields.
- Replace the inline record in `review.md` `# DETAILS` with `- [<ID>](<ID>.md)`.
- Add `archive:<ID>.md` to the matching `# SUMMARY` item in `review.md`.
- Preserve `# META` as the state index.
- Preserve `# SUMMARY` as the state index.
- Re-check every archived `# SUMMARY` marker has one matching `# DETAILS` link.
- Re-check every archived `# SUMMARY` marker has one sibling archive file.
- Re-check every `# SUMMARY` item has exactly one linked archive file or inline detail record.
- Archive migration is allowed only for file size.
- Archive migration is not a state change.
- Archive migration must not archive not-closed issues.
- Archive migration must not delete closed issues.

## Structural rules

- Never rewrite the review directory from scratch.
- Never cut-and-paste issue bodies during state changes.
- Never archive not-closed issues into `<ID>.md`.
- Never archive closed issues into `<ID>.md` unless the review tracks more than 15 issue IDs.
- Never move `# SUMMARY` out of `review.md`.
- Never remove an issue from `# SUMMARY` because its detail record was archived.
- Never archive an issue without adding `archive:<ID>.md` to its `# SUMMARY` item.
- Never leave `archive:<ID>.md` on a summary item whose detail record is inline or reopened.
- Never truncate an archived detail file to a metadata-only stub.
- Never delete archived issue content just because the issue closed.
- Never create index sections beyond `# META`, `# SUMMARY`, and `# DETAILS`.
- Do not create a separate cross-PR tracking section. Cross-PR parent/child context belongs in each issue's `pr:` field.
- Multiple agents work with this file concurrently. Structural changes break their references.
- State must match across all three places:
  - `open:` in `# META`
  - checkboxes and status tokens in `# SUMMARY`
  - statuses in inline detail records or archived closed sibling `<ID>.md` detail files

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

This is the only sample layout. The archived closed issue is valid only when the review tracks more than 15 issue IDs.

````md
reviews/<repo>-pr-<number>/
  review.md
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
reviewed:<yyyy-mm-dd>
open:B1

# SUMMARY
- [ ] B1 - OPEN [HIGH] - One-line summary and some key `path/file.ts:10`
- [x] B2 - CLOSED verified:2026-06-11 [MEDIUM] - Closed summary and some key `path/file.ts:42` archive:B2.md

# DETAILS
- [B2](B2.md)

## B1
ID:B1
type:BUG
severity:HIGH
summary:One-line summary
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
summary:Closed summary
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
