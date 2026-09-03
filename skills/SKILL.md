---
name: local-agent-skills
description: Load and use Ashley's local single-file agent skills from ~/agents/skills. Use when the user references @~/agents/skills, asks to read/install/use local skills, invokes slash commands such as /clean-check, /acs-review, /update-main, /cherry-pick, /squash-rebase, /rebase-squash, or names the corresponding commands without a slash.
---

# Local Agent Skills

Treat every Markdown file in `~/agents/skills/` as a usable local skill, not only files named `SKILL.md`.

## Discovery

When the user asks to read, install, or use `@~/agents/skills`, run:

```bash
rg --files ~/agents/skills
```

Read the relevant `.md` skill file completely before executing its workflow. If the user asks to read all skills, read every `.md` file in that directory.

## Command Map

Use these aliases:

- `/clean-check` or `clean-check` -> `CLEAN_CHECKS.md`
- `/acs-review` -> `ACS_REVIEW.md`
- `/acs-review-code` -> `ACS_REVIEW_CODE.md`
- `/acs-review-security` -> `ACS_REVIEW_SECURITY.md`
- `/acs-review-design` -> `ACS_REVIEW_DESIGN.md`
- `/update-main` or `update-main` -> `MAIN_UPDATE.md`
- `/cherry-pick` or `cherry-pick` -> `CHERRY_PICK.md`
- `/squash-rebase`, `/rebase-squash`, or `squash-rebase` -> `SQUASH_REBASE.md`
- `/review-triage` or `review-triage` -> `REVIEW_TRIAGE.md`

## Execution Rules

- Follow the target skill file's frontmatter and workflow instructions.
- Prefer the local skill file over similarly named built-in or repo-generated command files when the user references `~/agents/skills`.
- Treat explicit slash-command usage as approval for any action that the selected local skill says is approved by that slash command, while still using runtime approval mechanisms when required.
- Do not infer that a command is unavailable just because it is not represented as a `SKILL.md` folder; this directory uses single-file skills.
- If a requested local skill is missing, report the missing file and continue only with the closest safe fallback.
