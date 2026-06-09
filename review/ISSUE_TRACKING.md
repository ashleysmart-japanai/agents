# Issue Tracking

Review output is persisted under `<working-directory>/reviews/<repo>-pr-<number>/` (relative to where the reviewer agent is running, not the agents directory). The required index file is `review.md`. Issues are tracked across re-checks in the index plus any archived closed sibling `<ID>.md` detail files so nothing gets lost between iterations.

Legacy single-file reviews at `<working-directory>/reviews/<repo>-pr-<number>-review.md` may be migrated to the review directory. Preserve all issue history during migration.

The review index file, `review.md`, starts with this exact warning line:

```md
** WARNING do not delete review entries ever **
```

After the warning, `review.md` uses exactly three top-level sections, in this order:

1. `# META`
2. `# SUMMARY`
3. `# DETAILS`

Do not add other index sections. Do not create separate open/closed detail sections. Do not move issue bodies for ordinary state changes. The only allowed body moves are archiving verified-closed details to `<ID>.md` and unarchiving reopened details back into `review.md`.

## Review directory layout

Use this layout:

```text
reviews/<repo>-pr-<number>/
  review.md
  B2.md
  SEC-2.md
```

Open issue detail records must stay inline under `review.md` `# DETAILS`. If the review tracks more than 15 issue IDs, verified-closed detail records may be archived into sibling files named `<ID>.md`, for example `B2.md` or `SEC-2.md`, and linked from `review.md` `# DETAILS`.

Count tracked issue IDs by the issue items in `# SUMMARY`, excluding `- none`. Do not archive any issue while the review tracks 15 or fewer issue IDs.

Use one detail record per issue ID. Do not keep duplicate copies of the same issue detail both inline and in an archive file.

## META section

`# META` is the stable, grepable metadata block for the review. It comes immediately after the required warning line.

Required lines:

````md
** WARNING do not delete review entries ever **

# META
repo:<repo>
pr:<number>
branch:<branch>
base:<base-branch>
head:<head-sha>
reviewed:<yyyy-mm-dd>
open:<ID>,<ID>,<ID>
````

Rules:

- `open:` contains only currently open issue IDs, comma-separated with no spaces, for example `open:B1,SEC-1,I2`.
- If there are no open issues, write `open:none`.
- Update `open:` when an issue opens, closes, or reopens.
- Do not list closed IDs in `open:`.
- Add other grepable metadata only as `key:value` lines under `# META`.

## SUMMARY section

`# SUMMARY` is one flat checkbox list. Do not add headings, tables, verdicts, checks, or prose inside persisted `# SUMMARY`.

Every issue must have exactly one list item. The parseable part is only the prefix; the text after the dash is freeform summary text and may include one or more backticked location keys. The item may wrap, but it remains one checkbox item.

`# SUMMARY` must always remain in `review.md`. It is the authoritative compact issue list for every issue ID, including closed issues archived into sibling `<ID>.md` files. Do not move summary items into archive files.

Archived closed issues must include a grepable marker in their `# SUMMARY` item:

```md
archive:<ID>.md
```

For example:

```md
# SUMMARY
- [ ] B1 BUG [HIGH] - Example open bug and some key `src/file.ts:10`
- [x] B2 BUG [MEDIUM] - Example archived closed bug, fixed with key `src/file.ts:42` archive:B2.md
- [ ] SEC-1 SECURITY [HIGH] - Example security issue affecting auth setup key `src/auth.ts:8`
- [ ] D1 DESIGN [MEDIUM] - Example design anti-pattern and some key `src/design.ts:12`
- [ ] T1 TEST [MEDIUM] - Example test gap and some key `src/file.test.ts:7`
```

Rules:

- `- [ ]` means the issue is open.
- `- [x]` means the issue is closed and verified.
- Use this prefix: `- [ ] <ID> <TYPE> [<SEVERITY>] - ` or `- [x] <ID> <TYPE> [<SEVERITY>] - `.
- After the prefix, write human summary text. Include relevant backticked keys in that text, for example `` `path/file.ts:19` ``.
- Type values are `BUG`, `SECURITY`, `ISSUE`, `SCOPING_AUTH`, `OPTIMIZATION`, `DESIGN`, `TEST`, and `MINOR`.
- Keep items sorted by type in this order: `BUG`, `SECURITY`, `ISSUE`, `SCOPING_AUTH`, `OPTIMIZATION`, `DESIGN`, `TEST`, `MINOR`; then by issue ID.
- If the review has never recorded any issues, write `- none`.
- If a closed issue is archived in `<ID>.md`, include `archive:<ID>.md` in that issue's `# SUMMARY` item.
- If an archived issue is unarchived or reopened, remove `archive:<ID>.md` from that issue's `# SUMMARY` item.
- Keep the checkbox state aligned with the `open:` line in `# META` and the matching `# DETAILS` record.
- Never move an issue item between open/closed sections; there are no open/closed sections.
- Never remove a `# SUMMARY` item just because its detail body was archived.

## DETAILS section

`# DETAILS` points to one stable full record for every issue, open and closed. Do not move these records for ordinary state changes; only the explicit archive and unarchive operations below may move a detail body.

Open issues must be full inline records under `# DETAILS`.

Verified-closed issues may stay inline. If the review tracks more than 15 issue IDs, verified-closed issues may instead be archived into sibling `<ID>.md` files and linked from `# DETAILS`.

Inline details use full issue records directly under `# DETAILS`:

````md
# DETAILS

## B1
ID:B1
type:BUG
severity:HIGH
summary:Example issue
file:`src/file.ts:10`
pr:`#123`
status:OPEN

description:
<description of the issue>

evidence:
```evidence
<code snippet or command output showing the problem>
```

fix:<what needs to change>
reverify:<exact grep/read/test command or file:line to check>
````

Archived closed details use one link per archived issue under `# DETAILS`, with each detail record in a sibling `<ID>.md` file:

```md
# DETAILS
- [B2](B2.md)
- [SEC-2](SEC-2.md)
```

If the review has never recorded any issues, write `- none` under `# DETAILS`.

The sibling archive file contains the same full closed issue record that would otherwise be inline. Do not replace the body with a metadata-only stub.

````md
## B2
ID:B2
type:BUG
severity:MEDIUM
summary:Example closed issue
file:`src/file.ts:42`
pr:`#123`
status:CLOSED verified:<yyyy-mm-dd>
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
````

## Opening an issue

Every finding gets a unique ID and is documented with enough context to re-verify later. New and open issue detail records must be inline under `review.md` `# DETAILS`:

````md
## <ID>
ID:<ID>
type:BUG|SECURITY|ISSUE|SCOPING_AUTH|OPTIMIZATION|DESIGN|TEST|MINOR
severity:CRITICAL|HIGH|MEDIUM|LOW
summary:<one-line summary>
file:`path/to/file.ts:123`
pr:`#<number>` or `parent #<number> -> child #<number>`
status:OPEN

description:
<description of the issue>

evidence:
```evidence
<code snippet or command output showing the problem>
```

fix:<what needs to change>
reverify:<exact grep/read/test command or file:line to check>
````

- **ID format:** Category prefix + number: `B1`, `SEC-3`, `I6`, `S4`, `O2`, `D3`, `T1`, `M1`
  - `B` = Bug (will break)
  - `SEC` = Security
  - `I` = Issue (functional risk)
  - `S` = Issue (scoping/auth)
  - `O` = Optimization
  - `D` = Design anti-patterns and failures
  - `T` = Test gap or issues
  - `M` = Minor
- **Severity:** CRITICAL / HIGH / MEDIUM / LOW
- **Evidence:** Always include the actual code snippet or command output that proves the issue. Never open an issue without evidence.

When opening an issue:

- Add the ID to the `open:` line in `# META`.
- Add one unchecked `- [ ]` item to the flat list in `# SUMMARY`.
- Add one full inline detail record under `# DETAILS`.
- Do not create `<ID>.md` for a new or open issue.
- Include `pr:` in the detail record when the issue comes from cross-PR parent/child tracking.

## Closing an issue

When a fix is confirmed, do not move the detail record. Update the existing META, SUMMARY, and detail entries in place:

````md
## <ID>
ID:<ID>
type:BUG|SECURITY|ISSUE|SCOPING_AUTH|OPTIMIZATION|DESIGN|TEST|MINOR
severity:CRITICAL|HIGH|MEDIUM|LOW
summary:<one-line summary>
file:`path/to/file.ts:123`
pr:`#<number>` or `parent #<number> -> child #<number>`
status:CLOSED verified:<yyyy-mm-dd>
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
````

Closing rules:

- Remove the ID from the `open:` line in `# META`.
- Change its `# SUMMARY` checkbox from `- [ ]` to `- [x]`.
- Change `status:OPEN` to `status:CLOSED verified:<yyyy-mm-dd>`.
- Add `commit:`, `reverify:`, and `fixed:` if missing.
- Keep the original summary, description, file reference, PR reference, and evidence intact.
- Do not move the issue body as part of the close itself.
- If the review tracks more than 15 issue IDs, the verified-closed issue may be archived to sibling file `<ID>.md`; otherwise keep it inline.

## Reopening an issue

If a fix is reverted or no longer holds:

- Add the ID back to the `open:` line in `# META`.
- Change its `# SUMMARY` checkbox from `- [x]` to `- [ ]`.
- Change the detail status back to `status:OPEN`.
- Add `reopened:<yyyy-mm-dd> - <reason and sha if known>` in the same detail record.
- If the issue was archived in `<ID>.md`, unarchive it by restoring the full detail record inline under `# DETAILS` and replacing the archive link with that inline record.
- Remove the `archive:<ID>.md` marker from the `# SUMMARY` item when the issue is unarchived or reopened.

## Re-checking after a push or rebase

On each re-check:

1. Pull the latest code.
2. Read every inline detail record and every archived closed sibling detail file linked from `# DETAILS`.
3. Re-verify every closed issue using its documented check.
4. If a closed fix was reverted, reopen it in place.
5. Re-check every open issue listed in the `open:` line in `# META` and confirm it is still present or close it in place.
6. Add any new findings as new list items and new detail records.
7. Update the flat issue list under `# SUMMARY`.

## Archiving closed details into files

When `review.md` becomes too large, archive closed issue details into sibling files only if the review tracks more than 15 issue IDs:

1. Count issue IDs in `# SUMMARY`, excluding `- none`. If the count is 15 or fewer, do not archive details into files.
2. Select only verified-closed issues with `status:CLOSED verified:<yyyy-mm-dd>`.
3. Create one sibling archive file per selected closed issue, named `<ID>.md`.
4. Move the full existing `## <ID>` record into that file without rewriting its history, including description, evidence, fix, reverify, commit, and fixed fields.
5. Replace the inline record in `review.md` `# DETAILS` with `- [<ID>](<ID>.md)`.
6. Add `archive:<ID>.md` to the matching `# SUMMARY` item in `review.md`.
7. Preserve `# META` and `# SUMMARY` as the state index.
8. Re-check that every archived `# SUMMARY` marker has one matching `# DETAILS` link and one sibling archive file.
9. Re-check that every `# SUMMARY` item has exactly one linked archive file or inline detail record.

This archive migration is allowed for file size. It is not a state change, it must not archive open issues, and it must not delete closed issues.

## Structural rules

- Never rewrite the review directory from scratch.
- Never cut-and-paste issue bodies during state changes.
- Never archive open issues into `<ID>.md`.
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
  - checkboxes in `# SUMMARY`
  - statuses in inline detail records or archived closed sibling `<ID>.md` detail files

## Review file layout

Example with an archived closed issue. The archive link is valid only when the review tracks more than 15 issue IDs.

`review.md`:

````md
** WARNING do not delete review entries ever **

# META
repo:<repo>
pr:<number>
branch:<branch>
base:<base-branch>
head:<head-sha>
reviewed:<yyyy-mm-dd>
open:<ID>,<ID>,<ID>

# SUMMARY
- [ ] B1 BUG [HIGH] - One-line summary and some key `path/file.ts:10`
- [x] B2 BUG [MEDIUM] - Closed summary and some key `path/file.ts:42` archive:B2.md

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
````

`B2.md`:

````md
## B2
ID:B2
type:BUG
severity:MEDIUM
summary:Closed summary
file:`path/file.ts:42`
pr:`#<number>`
status:CLOSED verified:<yyyy-mm-dd>
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
````
