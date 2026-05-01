# Create Pull Request Skill

## Pre-flight

1. **Ensure clean state** — run in parallel:
   - `git status` (no unexpected changes)
   - `git log --oneline main..HEAD` (commits to include)
   - `git diff main...HEAD --stat` (files changed)

2. **Run all checks** — detect language from changed files, run in parallel. See `tooling/TOOLING.md` / `tooling/TOOLING_<lang>.md` for per-language commands.
   - Lint
   - Format — if it fails, auto-fix and commit the result
   - Typecheck — ignore pre-existing errors in untouched files
   - Tests

3. **Fix before proceeding** — do NOT create the PR if lint, format, or tests fail on changed files.

## Branch prep

1. **Rebase on main**:
   ```bash
   git fetch --prune
   git checkout main && git pull origin main
   git checkout <branch> && git rebase main
   ```
   - Resolve conflicts: prefer main's version for files with no intentional changes. For files we changed, merge carefully.
   - Re-run checks after rebase.

2. **Squash if requested** — `git reset --soft main && git commit -m "message"`

3. **Push**:
   - First push: `git push -u origin <branch>`
   - After rebase/squash: `git push --force-with-lease origin <branch>`
   - Never force push without `--force-with-lease`
   - Never push to main/master

## PR description

**Template selection:** Check the repo's AGENTS.md and `.github/pull_request_template.md` (or `.github/PULL_REQUEST_TEMPLATE/`) for a repo-specific PR template. If one exists, use it. Otherwise, fall back to `~/agents/PR_TEMPLATE.md`.

Use a HEREDOC via `mktemp` (never hardcode `/tmp` paths — multiple agents run concurrently):

```bash
TMPFILE=$(mktemp /tmp/pr-XXXXXX.md)
cat <<'PREOF' > "$TMPFILE"
<body content>
PREOF
gh pr create --title "title" --body-file "$TMPFILE"
rm "$TMPFILE"
```

### Title conventions
- Under 70 characters
- Format: `type(scope): description`
- Types: `fix`, `feat`, `refactor`, `docs`, `test`, `chore`
- Use description for details, not the title

### Description rules
- Lead with WHY, not WHAT
- List all changed files/endpoints/components in a structured table if the PR is large
- Explicitly list what was NOT changed and why (scope boundaries)
- If there are pre-existing issues in untouched files, note them as out of scope
- Link to spec if one exists
- Update the description when the PR changes — stale descriptions cause review friction

## Updating an existing PR

```bash
TMPFILE=$(mktemp /tmp/pr-body-XXXXXX.md)
gh pr view <number> --json body --jq .body > "$TMPFILE"
# edit $TMPFILE
gh pr edit <number> --body-file "$TMPFILE"
rm "$TMPFILE"
```

- Use `sed` for targeted replacements
- Re-read and verify after updating — `gh pr view <number> --json body --jq .body | grep "<term>"`

## Commit conventions

### Message format
```
type(scope): concise description of why

Optional body with details.

```

Always use HEREDOC for multi-line messages:
```bash
git commit -m "$(cat <<'EOF'
type(scope): description

Body text here.

)"
```

### Staging rules
- `git add <specific-files>` — never `git add -A` or `git add .`
- Only commit files relevant to the change
- Never commit `.env`, credentials, or large binaries

### Amend vs new commit
- Amend: only when squashing into a single commit (user requested)
- New commit: default — separate logical changes get separate commits
- After pre-commit hook failure: always NEW commit (the failed commit didn't happen, amending would modify the previous commit)

## Post-creation

1. Verify the PR was created: `gh pr view <number> --json url --jq .url`
2. Return the PR URL to the user
3. Do NOT merge unless explicitly asked

## Rules

- Never push without user approval
- Never force push to main/master
- Never skip hooks (`--no-verify`)
- Never create empty commits
- Always run lint + format + typecheck + tests before creating/updating a PR
- Always use `mktemp` for temp files — never hardcode `/tmp/` paths
- Keep the PR description in sync with the actual code — update it when changes are made
- If the PR description references endpoints, components, or features, verify they exist in the diff
