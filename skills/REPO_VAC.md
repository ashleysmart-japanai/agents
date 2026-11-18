---
name: repo-vac
description: Slash command /repo-vac. Dry-run report first, then on confirmation discard all local work, check out and update main, prune local tracking refs, delete stale local branches (upstream gone, local backup branches older than 2 months, tracked branches older than 2 months), clear stashes, run git gc, and report the cleanup. Use when the user wants a checkout reset to a clean main with stale branches removed.
---

# Repo Vac

Use this skill when the user asks to run `/repo-vac` or clean up a local checkout.

## Terms

- **Age**: time since the branch tip's committer date.
- **Stale**: age greater than 2 months.
- **Gone branch**: a local branch whose upstream was deleted on the remote (`[gone]`, or its upstream is in the prune list).
- **Backup branch**: a local branch with no upstream, or one with commits its upstream lacks (track shows `ahead`); kept to save a change.
- **Tracked branch**: a local branch with an upstream and no unpushed commits (track is empty or `behind` only).

## Phase 1: Dry run

Phase 1 changes no local branch, file, stash, or log.

1. Fetch without pruning:
   - `git -C <repo> fetch --all`
2. List tracking refs that prune would drop:
   - `git -C <repo> fetch --all --prune --dry-run`
3. List uncommitted tracked changes:
   - `git -C <repo> status --short`
4. List untracked files that clean would remove:
   - `git -C <repo> clean -nd`
5. List commits main would pull:
   - `git -C <repo> log --oneline main..origin/main`
6. List local branches with upstream, track state, and age:
   - `git -C <repo> for-each-ref --format='%(refname:short)|%(upstream:short)|%(upstream:track)|%(committerdate:unix)' refs/heads`
   - Stale cutoff: `date -v-2m +%s` on macOS, `date -d '2 months ago' +%s` on Linux.
7. Classify each branch except `main`:
   - **Gone branch** → delete.
   - **Backup branch**, stale → delete.
   - **Backup branch**, not stale → keep.
   - **Tracked branch**, stale → delete the local copy.
   - **Tracked branch**, not stale → keep.
8. List stashes:
   - `git -C <repo> stash list --format='%H %gd %s'`
9. List recovery logs older than 1 month:
   - `find /tmp -maxdepth 1 -name 'repo-vac-*.log' -mtime +30 -print`
10. Record the repo size:
    - `git -C <repo> count-objects -vH`
11. Print the dry-run report, one section per item, with "none" for an empty section:
    - **Would prune tracking refs**: each `origin/*` ref from step 2.
    - **Would discard changes**: each line from step 3.
    - **Would remove untracked files**: each line from step 4.
    - **Main would pull**: each commit from step 5, or "already up to date".
    - **Would delete branches**: branch, class, age, tip SHA.
    - **Would keep branches**: branch, class, age, reason.
    - **Would clear stashes**: each stash from step 8.
    - **Would delete old logs**: each path from step 9.
    - **Repo size**: from step 10.
12. Ask the user to confirm before Phase 2.
    - Stop when the user declines.

## Phase 2: Clean up

1. Write a recovery log before any deletion:
   - `LOG=$(mktemp /tmp/repo-vac-XXXXXX.log)`
   - `git -C <repo> for-each-ref --format='%(objectname) %(refname:short)' refs/heads >> "$LOG"`
   - `git -C <repo> stash list --format='%H %gd %s' >> "$LOG"`
   - `git -C <repo> status --short >> "$LOG"`
2. Prune local tracking refs:
   - `git -C <repo> fetch --all --prune`
3. Discard uncommitted changes and untracked files:
   - `git -C <repo> reset --hard`
   - `git -C <repo> clean -fd`
4. Check out and update main:
   - `git -C <repo> checkout main`
   - `git -C <repo> pull --ff-only origin main`
5. Delete each branch the dry run marked delete:
   - `git -C <repo> branch -D <branch>`
6. Clear stashes:
   - `git -C <repo> stash clear`
7. Run garbage collection:
   - `git -C <repo> gc`
8. Delete recovery logs older than 1 month:
   - `find /tmp -maxdepth 1 -name 'repo-vac-*.log' -mtime +30 -print -delete`
9. Report the cleanup with the dry-run sections in past tense, from the command output:
   - **Repo size**: before and after `git gc`, from `count-objects -vH`.
   - **Recovery log**: path of this run's log.
   - **Final state**: `git -C <repo> status --short --branch` and `git -C <repo> log --graph --oneline -n 10`.
   - Flag any difference from the dry-run report.

## Rules

- Run Phase 1 before Phase 2 on every invocation.
- When the user confirms the dry-run report, treat that as approval to discard uncommitted changes, untracked files, stashes, and the branches classified for deletion.
- Write the recovery log before Phase 2 step 2.
- Recovery logs live for 1 month; each run deletes logs past that age.
- Never delete `main`.
- Every deletion targets local branches.
- Never delete, prune, or modify branches on the remote.
  - `git fetch --prune` drops stale local `origin/*` tracking refs only; it does not change the remote.
- Never run `git push`, `git push --delete`, or `git remote prune` against a remote.
- Keep ignored files: use `git clean -fd`, not `git clean -fdx`.
  - Ignored files hold local config such as `.env`.
- Run `git gc` without `--prune=now`.
  - The default prune window keeps deleted branch and stash objects recoverable from the recovery log SHAs for 2 weeks.
- If `main` does not exist locally, create it from `origin/main`.
- If `origin/main` does not exist, stop and report the default branch from `git remote show origin`.
