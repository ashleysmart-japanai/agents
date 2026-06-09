---
name: clean-check
description: Slash command /clean-check. Run a repository clean-state and verification pass, fetch/prune remotes, run lint, typecheck, format check, tests, changed-file coverage, pre-commit hooks, push the current branch, then show the final git graph if successful. Use before calling a branch clean, ready, mergeable, or safe to hand off.
---

# Clean Check

Use this skill when the user asks for a clean check, readiness check, pre-merge verification, or a final pass over branch hygiene.

## Workflow

1. Check the current git context:
   - `git branch --show-current`
   - `git status --short --branch`
2. Check for stashed work:
   - `git stash list`
   - If stashes exist, report them. Do not apply, drop, or modify stashes unless the user asks.
3. Check for local/untracked files:
   - `git ls-files --others --exclude-standard`
   - Report untracked files separately from tracked changes.
4. Check for uncommitted tracked changes:
   - `git diff --stat`
   - `git diff --cached --stat`
   - `git status --short`
   - Do not stage, commit, discard, or stash changes unless the user asks.
5. Fetch and prune:
   - Prefer `git fetch --prune origin`.
   - Use `git fetch --all --prune` only when multiple remotes matter for the task.
6. Run lint.
7. Run typechecks.
8. Run format checks.
9. Run test cases.
10. Generate a coverage report for changed files:
   - Determine the comparison base. Prefer the PR base branch when known; otherwise use `origin/main` when available.
   - List changed files with the merge base, for example `git diff --name-only "$(git merge-base HEAD origin/main)" HEAD`.
   - Filter to changed production files. Exclude deleted files, test files, generated files, docs, fixtures, and config-only changes unless the repo treats them as coverable code.
   - Run the repository's native coverage command. See `tooling/TOOLING.md` / `tooling/TOOLING_<lang>.md` for language-specific coverage commands.
   - Report per-file coverage for every changed production file.
   - If the coverage tool cannot produce changed-file coverage, report the closest available coverage summary and explicitly list which changed production files could not be reported.
   - If there are no changed production files, report coverage as N/A with the reason.
11. Run pre-commit hooks.
12. Re-check that the working tree is clean:
   - `git status --short --branch`
   - If the checks or hooks created changes, stop and report them instead of pushing.
13. Push the current branch:
   - If an upstream exists, run `git push`.
   - If no upstream exists and `origin` exists, run `git push -u origin "$(git branch --show-current)"`.
   - Stop and report if the remote or branch target is ambiguous.
14. Report the push result.
15. If the push succeeds, show the final graph summary:
   - `git log --graph --oneline | head -n 10`

## Command Selection

- Prefer repository-native scripts over ad hoc commands.
- For Nx repositories, prefer `nx` commands when available and choose the narrowest useful scope.
- Inspect `package.json`, `project.json`, or documented repo instructions before guessing command names.
- Prefer coverage commands that can map line or branch coverage back to changed files.
- For changed-file coverage, use structured coverage output when available rather than eyeballing terminal summaries.
- If coverage output exists but changed-file extraction is not supported, still include the changed production file list and the nearest coverage summary.
- If a verification command is missing, report that it was unavailable instead of inventing a substitute.

## Reporting

Report in this order:

1. Git state: branch, stashes, untracked files, unstaged changes, staged changes.
2. Fetch/prune result.
3. Verification results: lint, typecheck, format check, tests, changed-file coverage, pre-commit hooks.
4. Push result.
5. Final graph summary, only after a successful push.
6. Any blockers or commands that could not be run.

## Rules

- This skill is a verification-then-push workflow.
- Never discard local work.
- Never auto-apply or drop stashes.
- When the user explicitly asks to use `clean-check` or `/clean-check`, treat that request as approval to push the current branch at the end unless they explicitly say not to push.
- Never push if verification fails or the working tree is dirty after checks.
- If changed production files exist and no changed-file coverage report can be produced, stop before pushing and report the coverage blocker.
- Never force push.
- If the runtime requires a separate execution approval for `git push`, use that mechanism directly.
- If verification fails, stop and report the failing command plus the first actionable error.
