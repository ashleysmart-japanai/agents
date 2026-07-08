---
name: squash-rebase
description: Slash command /squash-rebase, also /rebase-squash. Squash a PR branch to one commit, verify the diff is unchanged, then rebase it onto origin/main. Use when the user wants a clean one-commit PR with safety checks.
---

# Git Rebase Squash

**DO NOT hand-run git commands for this.** A hand-run squash-rebase once left the branch's
merge-base behind `main`, which poisoned the PR diff with ~2000 lines of already-merged code
and tripped a scope-mixing bot. The safe procedure is codified in a script that enforces the
merge-base gate and the anti-poison diff gate deterministically. Run the script; do not
reimplement it inline.

## Procedure

1. Confirm you are on (or know) the PR branch, and that `origin/main` is the target base.
2. Run the script from the repo (it fetches, records the intended three-dot diff, rebases
   `--onto origin/main`, squashes to one commit, and verifies both safety gates):

   ```bash
   python3 ~/agents/skills/squash_rebase.py --repo <repo-path> [--branch <name>]
   ```

   Without `--push` it stops **right before** the push and prints the exact push command —
   this is the safe default. Add `--dry-run` to rebase/squash locally and stop before push
   while still running every gate. Use `--message`/`--message-file` to set the squash commit
   message; otherwise it derives one from the existing commit subjects.

3. Read the script output. It prints, in order:
   - branch, `origin/main` tip, old merge-base, and whether the branch was stale.
   - the intended file count and `--stat` summary.
   - `[GATE A ok]` merge-base advanced to equal `origin/main` (the check that was skipped
     originally — a stale merge-base is what poisons the diff).
   - `[GATE B ok]` post-rebase file list matches the pre-recorded three-dot list (no
     main changes leaked in, no main files got reverted).
   - `[squash ok]` exactly one commit above main and the tree is byte-identical (squash
     changed only history, not content).
4. If any gate fails, the script aborts with exit 1 and **restores the branch to its original
   tip** — nothing is pushed. Report the failure; do not try to "fix it up" by hand.
5. To push, re-run with `--push` (the skill invocation is approval to force-push — see Rules).

## Recovery

The script prints a `[recovery]` line with the exact `reset --hard <original-tip>` command
before it rewrites anything. If a run is interrupted, use that line to restore the branch.

## Rules

- **Never reimplement the rebase/squash inline.** Use `squash_rebase.py`. It exists because
  the manual version is easy to get wrong in a way that silently poisons the PR diff.
- Never use `git reset --soft origin/main` to squash while the merge-base is stale — that
  stages the two-dot delta and reverts main's own files. The script only does the soft-reset
  squash *after* Gate A proves merge-base == main.
- Do not discard local work. The script refuses to run with untracked files, stashes, or
  uncommitted changes present. STOP AND REPORT if it does.
- Do not use `main` for comparisons until after `git fetch --prune` (the script does this
  unless `--no-fetch`).
- Do not push without approval. When the user explicitly asks to use `squash-rebase`,
  `/squash-rebase`, `rebase-squash`, or `/rebase-squash`, that is approval to finish with
  `--push` (which runs `git push --force-with-lease`) unless they say not to push.
- Do not stop to ask for a second chat-level confirmation before the final push. If the
  runtime requires a separate execution approval, use that mechanism directly.
