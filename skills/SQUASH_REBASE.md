---
name: squash-rebase
description: Slash command /squash-rebase, also /rebase-squash. Squash a PR branch to one commit, verify the diff is unchanged, then rebase it onto origin/main. Use when the user wants a clean one-commit PR with safety checks.
---

# Git Rebase Squash

1. Check for local/untracked files:
   - `git ls-files --others --exclude-standard`
   - Stop and report any local files before rewriting history.
2. Check for stashed work:
   - `git stash list`
   - Stop and report any stashes before rewriting history.
3. Check for uncommitted changes:
   - `git status --short`
   - `git diff --stat`
   - `git diff --cached --stat`
   - Stop and report any unstaged or staged changes before rewriting history.
4. Always fetch and prune before trusting `main`:
   - `git fetch --prune origin`
   - Never assume local `main` is up to date.
5. Check out `main` and pull latest `origin/main`.
6. Report the current `main` commit hash after updating it:
   - `git rev-parse main`
   - If `origin/main` exists, also report `git rev-parse origin/main` when it differs.
7. Check out the PR branch.
8. Find the branch cut point from the freshly fetched and updated `main`.
9. Write a `/tmp` report with the changed file list and line summary.
10. Squash all PR commits into one commit at the branch cut point.
11. Confirm the squash changed nothing except commit history.
12. Rebase the PR branch onto `origin/main`.
13. Confirm the final file list and line summary still match the `/tmp` report so `main` changes did not poison the PR.
14. Show the final graph summary:
   - `git log --graph --oneline | head -n 10`

## Rules

- Do not discard local work. STOP WHEN YOU FIND IT and REPORT IT
- Do not use `main` for comparisons until after `git fetch --prune origin` has completed.
- Always include the updated `main` commit hash in the report.
- Do not push without approval.
- When the user explicitly asks to use this `squash-rebase`, `/squash-rebase`, `rebase-squash`, or `/rebase-squash` skill, treat that request as approval to finish the workflow with `git push --force-with-lease` for the rewritten branch unless they explicitly say not to push.
- Do not stop to ask for a second chat-level confirmation before that final `git push --force-with-lease`. If the runtime requires a separate execution approval, use that mechanism directly.
