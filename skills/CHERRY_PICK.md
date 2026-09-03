---
name: cherry-pick
description: Slash command /cherry-pick. Fetch and prune, identify the parent PR and child PR, state the cherry-pick scope, then copy relevant scoped changes from the parent PR into the child PR. Stop and ask if parent PR, child PR, or child scope is unknown.
---

# Cherry Pick Parent Into Child

Use this skill when the user asks to cherry-pick a parent PR, pull parent changes into a child PR, update a stacked child PR from its parent, or run `/cherry-pick`.

## Workflow

1. Fetch and prune before trusting branch state:
   - `git fetch --all --prune`
2. Check local state:
   - `git status --short --branch`
   - `git branch --show-current`
   - If a merge, rebase, or cherry-pick is already in progress, stop and report it.
   - If unrelated local changes exist, report them and do not overwrite or stage them.
3. Identify the current PR context:
   - `gh pr view --json number,title,url,headRefName,baseRefName,state,body`
   - If `gh pr view` fails, try `gh pr list --head <current-branch> --json number,title,url,headRefName,baseRefName,state`.
4. Identify both PRs:
   - Child PR: the PR whose branch should receive the copied changes.
   - Parent PR: the PR whose branch is the source of the changes.
   - For stacked PRs, the child PR usually has `baseRefName` equal to the parent branch; resolve the parent with `gh pr list --head <baseRefName> --json number,title,url,headRefName,baseRefName,state`.
   - If the parent PR number, child PR number, or source/target branch is not known, stop and ask.
5. Identify and state the child scope before editing:
   - Use the user request, PR title/body, branch name, changed files, and commit messages to summarize the child scope in one or two sentences.
   - If the child scope is unclear, stop and ask.
6. State the plan before copying:
   - Parent PR number, title, branch, and URL.
   - Child PR number, title, branch, and URL.
   - Direction: copy scoped changes from parent branch into child branch.
   - Scope: the child-specific behavior/files being updated.
7. Check out the child branch:
   - `git checkout <child-branch>`
   - Confirm `git status --short --branch`.
8. Find parent changes missing from the child:
   - `git log --oneline <child-branch>..<parent-branch>`
   - `git diff --stat <child-branch>..<parent-branch>`
   - Inspect diffs enough to separate relevant scoped changes from unrelated parent work.
9. Copy only relevant parent changes into the child:
   - Prefer commit-by-commit `git cherry-pick <sha>` only when the whole commit is relevant to the child scope.
   - If only part of a parent commit is relevant, manually transplant the relevant hunks with normal editing tools and cite the source commit in the new commit message.
   - Do not copy unrelated refactors, generated churn, docs, or tooling unless they are required by the child scope.
10. Resolve conflicts carefully:
    - Preserve child-specific behavior unless the parent fix intentionally changes it.
    - Re-read the surrounding code and tests before choosing either side.
    - Never resolve by blindly taking `--ours` or `--theirs`.
11. As each issue is fixed, check in:
    - Run focused validation for the touched area.
    - Stage only files belonging to the current copied fix.
    - Commit one coherent fix at a time using repository commit style.
    - Report the commit hash and tests run.
12. After all scoped changes are copied:
    - Run broader validation appropriate to the touched modules.
    - Show `git status --short --branch`.
    - Report copied commits/changes, skipped parent changes with reasons, and verification results.
    - Do not push unless the user explicitly asked.

## Rules

- First command must be a fetch/prune command.
- Never proceed unless parent PR, child PR, target child branch, source parent branch, and child scope are known.
- The target is the child PR branch; the source is the parent PR branch.
- "Cherry-pick" means copy relevant code changes, not necessarily replay every source commit verbatim.
- Keep the child PR focused. Skip parent changes outside the child scope and explain why.
- Do not overwrite, revert, or stage unrelated local changes.
- Do not commit generated files unless they are required and reproducible.
- Do not push without explicit user approval.
