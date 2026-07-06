---
name: clean-check
description: Slash command /clean-check. Run a repository clean-state and verification pass, fetch/prune remotes, run lint, typecheck, build, format check, tests, changed-file coverage, pre-commit hooks, push the current branch, then show the final git graph if successful. Use before calling a branch clean, ready, mergeable, or safe to hand off.
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
8. Run a build of the changed/affected projects:
   - For Nx repositories, prefer `nx build <project>` scoped to affected projects.
   - For other repositories, use the repository's native build command.
   - A build failure (e.g., webpack `ERROR in` lines, non-zero exit code) is a verification failure — stop and report.
   - This catches type errors that standalone `tsc --noEmit` misses, such as stricter type narrowing in bundler compilation or generated-type mismatches.
9. Run format checks.
10. Run test cases.
11. Generate a coverage report for changed files:
   - Determine the comparison base. Prefer the PR base branch when known; otherwise use `origin/main` when available.
   - List changed files with the merge base, for example `git diff --name-only "$(git merge-base HEAD origin/main)" HEAD`.
   - Filter to changed production files. Exclude deleted files, test files, generated files, docs, fixtures, and config-only changes unless the repo treats them as coverable code.
   - Run the repository's native coverage command. See `tooling/TOOLING.md` / `tooling/TOOLING_<lang>.md` for language-specific coverage commands.
   - Report per-file coverage for every changed production file.
   - If the coverage tool cannot produce changed-file coverage, report the closest available coverage summary and explicitly list which changed production files could not be reported.
   - If there are no changed production files, report coverage as N/A with the reason.
12. Run pre-commit hooks.
13. Reviewer-bait check:
   - Read the full diff for the branch: `git diff "$(git merge-base HEAD origin/main)" HEAD`.
   - Scan every changed hunk for reviewer bait — text that says something the code does not actually do. Common forms:
     - Comments describing logic that was deleted, never implemented, or does something different from what the comment says.
     - Docstrings or JSDoc whose parameter lists, return types, or behavior descriptions don't match the actual function signature or body.
     - Log/error messages that name an operation, entity, or condition that doesn't correspond to what the surrounding code handles.
     - Variable or function names that imply a purpose the implementation doesn't fulfill (e.g., `validateInput` that never validates).
     - TODO/FIXME markers on code that was supposedly just fixed in this branch.
     - Leftover boilerplate strings (e.g., "handles X gracefully") copied from a template but never made true.
   - For each finding, quote the bait text and the contradicting code. Report as a verification failure.
   - If no reviewer bait is found, report the step as passed.
14. Re-check that the working tree is clean:
   - `git status --short --branch`
   - If the checks or hooks created changes, stop and report them instead of pushing.
15. Push the current branch:
   - If an upstream exists, run `git push`.
   - If no upstream exists and `origin` exists, run `git push -u origin "$(git branch --show-current)"`.
   - Stop and report if the remote or branch target is ambiguous.
16. Report the push result.
17. If the push succeeds, show the final graph summary:
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
3. Verification results: lint, typecheck, build, format check, tests, changed-file coverage, pre-commit hooks, reviewer-bait check.
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
