# Codex Review Skill

## Purpose

Use this skill when the user wants a PR/code review performed by Codex directly, while still requiring the persisted review document to follow the tracking and formatting rules in:

- `/Users/ashley-smart/agents/REVIEWER.md`
- `/Users/ashley-smart/agents/review/ISSUE_TRACKING.md`
- `/Users/ashley-smart/agents/review/CHECKLIST.md`

This skill separates:

1. **Review logic**: done by Codex from the actual code, diff, tests, and behavior.
2. **Review document contract**: governed by the `~/agents/...` review docs.

Do **not** treat `~/agents/...` as the source of findings. Treat them as the required schema for how findings are tracked and written down.

## Operating rules

- Review the code yourself.
- Do not delegate the actual judgment to `~/agents/REVIEWER.md`.
- Do not invent ad hoc review sections if the existing review tracking format already has a place for the information.
- Persisted review state lives in `<working-directory>/reviews/<repo>-pr-<number>/`.
- The review index at `review.md` uses exactly three top-level sections: `# META`, `# SUMMARY`, and `# DETAILS`.
- `review.md` must start with the exact warning line `** WARNING do not delete review entries ever **` before `# META`.
- The `# SUMMARY` section must remain in `review.md` and must contain every issue item, including archived closed issues.
- Open issue detail records stay inline under `# DETAILS`.
- Verified-closed issue detail records may be archived into sibling `<ID>.md` files linked from `# DETAILS` only when the review tracks more than 15 issue IDs.
- Archived closed issues must keep their `# SUMMARY` item in `review.md` with a grepable `archive:<ID>.md` marker.
- Keep the `open:` line in `# META`, `# SUMMARY` issue list checkboxes, and issue detail statuses consistent with each other.
- Preserve review history. Never delete prior issue history when updating an existing review file.
- Do not move issue bodies when opening or closing issues. Reopening an archived issue may unarchive the body from `<ID>.md` back into `review.md` `# DETAILS`.
- Do not create review index sections beyond `# META`, `# SUMMARY`, and `# DETAILS`.
- Cross-PR parent/child context belongs in each issue's `pr:` field, not in a separate section.

## Required workflow

### 1. Read the live review context first

Before making claims or editing the persisted review file:

- Read the current review index at `reviews/<repo>-pr-<number>/review.md`
- If only a legacy `reviews/<repo>-pr-<number>-review.md` exists, read it and migrate it to the review directory without losing history
- Read every archived closed issue detail file linked from the index `# DETAILS` section
- Read:
  - `~/agents/REVIEWER.md`
  - `~/agents/review/ISSUE_TRACKING.md`
  - `~/agents/review/CHECKLIST.md`
- Summarize to yourself:
  - what the current issue IDs are
  - which issues are open vs closed according to the `open:` line in `# META`, `# SUMMARY` checkboxes, and detail record statuses
  - which entries include cross-PR parent/child context in `pr:`

### 2. Perform the review yourself

Use your own analysis of:

- `git diff main...HEAD --stat`
- `git diff main...HEAD`
- `git log --oneline main..HEAD`
- changed files
- callers and parallel paths
- lint / format / typecheck / tests as appropriate
- runtime and contract risks

The codebase is the source of truth for findings.

### 3. Map findings onto the tracking contract

Every finding must be reflected in all three tracking places:

- `# META`: add the ID to `open:` when the issue is open, or remove it when closed.
- `# SUMMARY`: add or update exactly one item in the flat list. The required prefix is `- [ ] <ID> <TYPE> [<SEVERITY>] - ` or `- [x] <ID> <TYPE> [<SEVERITY>] - `; the rest is freeform summary text with relevant backticked location keys. If a closed issue is archived, the summary text must include `archive:<ID>.md`.
- Detail record: add or update exactly one full issue entry titled `## <ID>` with evidence and re-verification instructions. Open issues must be inline under index `# DETAILS`. Verified-closed issues may be inline or archived in sibling file `<ID>.md` only when the review tracks more than 15 issue IDs.

If a verified-closed issue is archived in a sibling file, the index `# DETAILS` section must contain exactly one link for that issue:

```md
# DETAILS
- [B2](B2.md)
```

Do not put open issues in `<ID>.md`. Do not archive closed issues while the review tracks 15 or fewer issue IDs. Do not keep duplicate copies of the same detail record inline and in an archive file.

When archiving a closed issue, move the full original detail record into `<ID>.md`, including description, evidence, fix, reverify, commit, and fixed fields. Do not replace it with a metadata-only stub. Add `archive:<ID>.md` to the matching `# SUMMARY` item. When unarchiving or reopening it, remove that marker.

#### Opening an issue

Add a new issue without moving existing list items or bodies. New and open issue details must be inline under index `# DETAILS`.

````md
## <ID>
ID:<ID>
type:BUG|SECURITY|ISSUE|SCOPING_AUTH|OPTIMIZATION|DESIGN|TEST|MINOR
severity:CRITICAL|HIGH|MEDIUM|LOW
summary:<one-line summary>
file:`path/to/file:line`
pr:`#<number>` or `parent #<number> -> child #<number>`
status:OPEN

description:
<description>

evidence:
```evidence
<proof snippet or command output>
```

fix:<what needs to change>
reverify:<exact command or file:line>
````

Also add the matching unchecked `# SUMMARY` list item and add the ID to the `open:` line in `# META`.

#### Closing an issue

When verified fixed, update the existing issue in place:

- Remove the ID from the `open:` line in `# META`.
- Change the `# SUMMARY` list item checkbox from `- [ ]` to `- [x]`.
- Change the detail record status to `status:CLOSED verified:<yyyy-mm-dd>`.
- Add `commit:`, `reverify:`, and `fixed:` if missing.
- Preserve the original summary, file reference, PR reference, description, and evidence.

Never move the issue to a closed section. There is no closed section. After an issue is verified closed, it may be archived to `<ID>.md` for file size only if the review tracks more than 15 issue IDs, with the index `# DETAILS` entry replaced by a link.

#### Reopening an issue

When a fix no longer holds, update the existing issue in place:

- Add the ID back to the `open:` line in `# META`.
- Change the `# SUMMARY` list item checkbox from `- [x]` to `- [ ]`.
- Change the detail record status back to `status:OPEN`.
- Add `reopened:<yyyy-mm-dd> - <reason and sha if known>` in the same detail entry.
- If the issue was archived in `<ID>.md`, unarchive it by restoring the full detail record inline under `# DETAILS` and removing the archive link.
- Remove any `archive:<ID>.md` marker from the `# SUMMARY` item when the issue is unarchived.

### 4. Update the compact state correctly

Treat the `open:` line in `# META` plus the flat `# SUMMARY` list as the compact state summary.

When re-checking a PR:

- keep the `open:` line in `# META` aligned with the detailed issue statuses, whether details are inline or archived closed files
- keep each summary item aligned with its detail entry
- never move `# SUMMARY` items out of `review.md`
- keep any archived issue's `archive:<ID>.md` marker in its `# SUMMARY` item
- do not add a new issue ID to `# META` or `# SUMMARY` without also adding its full detail entry
- do not remove an issue item, detail entry, archive file, or index link just because it closed
- do not archive open issues
- do not archive closed issues unless the review tracks more than 15 issue IDs
- do not truncate archived detail files to metadata-only records
- keep items sorted by type, then ID

### 5. Keep state aligned

Do not leave stale list items claiming an issue is open if the issue was later closed and verified.

## Behavioral guardrails

- Do not answer narrow formatting questions by searching for literal keywords only.
- Infer the document's state model from the current review file structure.
- If the user says "find the list", inspect the actual review file structure first. In this review system, the primary state list is the flat checkbox list under `# SUMMARY`.
- If you add a new issue ID, also add its detailed issue body inline under `# DETAILS`.
- If you change severity or wording in a summary list item, reflect the same change in the detailed issue entry.

## Done criteria

A review update is only complete when all of the following are true:

- the review conclusions came from Codex's own code review
- the persisted review directory follows the `~/agents/...` contract
- the `open:` line in `# META` matches `# SUMMARY` checkboxes and detail statuses
- any state changes are visible in the existing tracker and detailed entries
- no issue body was moved except for an allowed closed-issue archive or reopened-issue unarchive
- no freeform addendum was used where the existing review structure already covered the need

## Recommended user prompt

```text
Do a self-directed review. Use ~/agents/REVIEWER.md, ~/agents/review/ISSUE_TRACKING.md, and ~/agents/review/CHECKLIST.md only as the review-document contract, not as the reviewer. Then update the persisted review file to match that contract exactly.
```
