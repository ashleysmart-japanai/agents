---
name: update-main
description: Slash command /update-main. Fetch and prune all remotes, record the current PR or branch, inspect local files, stashes, and uncommitted changes, commit pending work when needed, update main, show the main graph, return to the original branch, then show the branch graph.
---

# Main Update

Use this skill when the user asks to run `/update-main` or update local `main` while preserving the current PR branch context.

## Workflow

1. Fetch and prune all remotes before trusting branch state:
   - `git fetch --all --prune`
2. Note the current branch and PR context:
   - `git branch --show-current`
   - `git status --short --branch`
   - If `gh` is available, run `gh pr view --json number,title,url,headRefName,baseRefName,state`.
   - If no PR is found or `gh` is unavailable, report the branch name and upstream instead.
3. Check for local/untracked files:
   - `git ls-files --others --exclude-standard`
   - Report untracked files separately from tracked changes.
4. Check for stashed work:
   - `git stash list`
   - Report stashes. Do not apply, drop, pop, or modify stashes unless the user explicitly asks.
5. Check for uncommitted changes:
   - `git status --short`
   - `git diff --stat`
   - `git diff --cached --stat`
6. If uncommitted work exists, commit it before leaving the branch:
   - Inspect the diff enough to write a meaningful commit message.
   - Stage the pending work that belongs to the current branch.
   - Commit with a concise message that matches the repository style.
   - Report the new commit hash and subject.
7. Check out `main`:
   - `git checkout main`
8. Pull the latest `main`:
   - Prefer `git pull --ff-only origin main`.
   - If the repository uses a different primary remote, use that remote and report it.
9. Show the updated `main` graph:
   - `git log --graph --oneline | head -n 10`
10. Check out the original PR branch:
    - `git checkout <original-branch>`
11. Show the graph again on the PR branch:
    - `git log --graph --oneline | head -n 10`
12. Report the final branch and status:
    - `git branch --show-current`
    - `git status --short --branch`

## Rules

- Never discard local work.
- Never auto-apply, pop, drop, or rewrite stashes.
- When the user explicitly asks to use `/update-main` or this `update-main` skill, treat that request as approval to create a normal commit for pending branch work before updating `main`.
- Do not commit generated, temporary, or unrelated untracked files unless they clearly belong to the current work.
- If the branch has no name, such as a detached HEAD, stop after reporting the state.
- If `main` does not exist locally, create it from the fetched default remote branch only when the remote target is unambiguous.
- Use `git pull --ff-only` for `main`; do not create a merge commit on `main`.
- Do not push unless the user explicitly asks.
