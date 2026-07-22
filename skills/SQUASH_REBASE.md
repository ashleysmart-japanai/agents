---
name: squash-rebase
description: Slash command /squash-rebase, also /rebase-squash. Squash a PR branch to one commit on its own merge-base, verify the diff is a 100% match, then rebase the single commit onto origin/main. Use when the user wants a clean one-commit PR with safety checks.
---

# Git Squash Rebase

**DO NOT hand-run git commands for this.** A hand-run squash-rebase once left the branch's merge-base behind `main`, which poisoned the PR diff with ~2000 lines of already-merged code. The safe procedure is codified in `squash_rebase.py`. Run the script; do not reimplement it inline.

## What the skill does (textual procedure)

1. Check the PR: identify the PR branch and the target base branch (`origin/main`).
2. Locate the root of the branch in the target branch's commit history — the merge-base. This is the **squash hash**.
3. Squash all branch commits down to the squash hash. This can never conflict. Before and after the squash, the changed files and line counts are checked — they must be a **100% match** or the branch is restored and the run aborts.
4. Rebase the squashed single commit onto the HEAD of the target branch. This gives at most **one** conflict round instead of one per commit.
5. After the rebase, check and **report** the file/line changes the rebase itself caused (e.g. from conflict resolution), then push.

Squash comes **before** rebase. Rebasing first replays every commit onto the moved main and multiplies the conflict opportunities.

## Running it

```bash
python3 ~/agents/skills/squash_rebase.py --repo <repo-path> [--branch <name>] [--push] [--yes]
```

- Without `--push` it stops right before the push and prints the exact push command (safe default).
- `--message` / `--message-file` set the squash commit message; otherwise it derives one from the existing commit subjects.
- Exit codes: `0` ok · `1` check failed (branch restored, nothing pushed) · `2` bad usage/state · `3` rebase conflict.

## On failure

- **Exit 3 — rebase conflict. This is expected, not a bug.** A conflict just means main touched the same files. The rebase is left in progress. Do this:
  1. Resolve the conflicts in the listed files.
  2. `git -C <repo> add <files>` then `git -C <repo> rebase --continue`.
  3. Re-run the script. It picks up the pre-squash record from `.git/squash-rebase-intent.json`, verifies the result, reports the file/line drift your resolution caused, and pushes.
- Do NOT abandon the task, `rebase --abort`, or hand-rebuild history just because the script printed a conflict. Only abort if the user says to, using the recovery command the script printed.
- **Exit 1 — a safety check failed.** The branch was restored to its original tip and nothing was pushed. Report the failure to the user; do not "fix it up" by hand.
- **Drift report.** After a conflict resolution the post-rebase diff will legitimately differ from the pre-squash record. The script prints exactly which files/line counts changed — include that report when telling the user what happened, and confirm before pushing if drift exists.

## Recovery

The script prints a `recovery` line (`git reset --hard <original-tip>`) before rewriting anything. If a run is interrupted, use that line to restore the branch.

## Rules

- Never reimplement the squash/rebase inline — use `squash_rebase.py`.
- Do not discard local work. The script refuses to run with untracked files, stashes, or uncommitted changes. STOP AND REPORT if it does.
- Do not compare against `main` before fetching (the script fetches with `--prune` unless `--no-fetch`).
- Invoking `squash-rebase` / `/squash-rebase` / `rebase-squash` / `/rebase-squash` is approval to finish with `--push` (`git push --force-with-lease`) unless the user says not to push.
- Do not stop to ask for a second chat-level confirmation before the final push. If the runtime requires a separate execution approval, use that mechanism directly.
