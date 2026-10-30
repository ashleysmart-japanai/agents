---
name: local-agent-skills
description: Load and use local single-file agent skills from ~/agents/skills. Use when the user references @~/agents/skills, asks to read/install/use local skills, invokes slash commands such as /clean-check, /acs-review, /update-main, /cherry-pick, /squash-rebase, /rebase-squash, /check-spec, or names the corresponding commands without a slash. Also route FDE/DS work requests through the work-skill command map, including advise_me, murderboard, ontology design, discovery, scoping, steering, and product opportunities.
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
- `/check-spec` or `check-spec` -> `CHECK_SPEC.md`

## Execution Rules

- Follow the target skill file's frontmatter and workflow instructions.
- Prefer the local skill file over similarly named built-in or repo-generated command files when the user references `~/agents/skills`.
- Treat explicit slash-command usage as approval for any action that the selected local skill says is approved by that slash command, while still using runtime approval mechanisms when required.
- Do not infer that a command is unavailable just because it is not represented as a `SKILL.md` folder; this directory uses single-file skills.
- If a requested local skill is missing, report the missing file and continue only with the closest safe fallback.

## FDE / DS work skills

- `/advise_me` or `advise_me` → [ADVISE_ME.md](ADVISE_ME.md).
- `/advise-me` or `advise-me` → [ADVISE_ME.md](ADVISE_ME.md).
- `/deployment-planner` or `deployment-planner` → [DEPLOYMENT_PLANNER.md](DEPLOYMENT_PLANNER.md).
- `/murderboard` or `murderboard` → [MURDERBOARD.md](MURDERBOARD.md).
- `/problem-value` or `problem-value` → [PROBLEM_VALUE.md](PROBLEM_VALUE.md).
- `/steering-escalation` or `steering-escalation` → [STEERING_ESCALATION.md](STEERING_ESCALATION.md).
- `/decision-advisor` or `decision-advisor` → [DECISION_ADVISOR.md](DECISION_ADVISOR.md).
- `/ontology-designer` or `ontology-designer` → [ONTOLOGY_SKETCHER.md](ONTOLOGY_SKETCHER.md).
- `/ontology-sketcher` or `ontology-sketcher` → [ONTOLOGY_SKETCHER.md](ONTOLOGY_SKETCHER.md).
- `/builder-wizard` or `builder-wizard` → [BUILDER_WIZARD.md](BUILDER_WIZARD.md).
- `/production-readiness` or `production-readiness` → [PRODUCTION_READINESS.md](PRODUCTION_READINESS.md).
- `/customer-conversation` or `customer-conversation` → [CUSTOMER_CONVERSATION.md](CUSTOMER_CONVERSATION.md).
- `/discovery-interviewer` or `discovery-interviewer` → [DISCOVERY_INTERVIEWER.md](DISCOVERY_INTERVIEWER.md).
- `/ownership-handoff` or `ownership-handoff` → [OWNERSHIP_HANDOFF.md](OWNERSHIP_HANDOFF.md).
- `/product-opportunity` or `product-opportunity` → [PRODUCT_OPPORTUNITY.md](PRODUCT_OPPORTUNITY.md).
- `/account-growth` or `account-growth` → [ACCOUNT_GROWTH.md](ACCOUNT_GROWTH.md).
- `/scope-success` or `scope-success` → [SCOPE_SUCCESS.md](SCOPE_SUCCESS.md).
- `/ds-scope-checker` or `ds-scope-checker` → [DS_SCOPE_CHECKER.md](DS_SCOPE_CHECKER.md).
- `/stakeholder-conversation` or `stakeholder-conversation` → [STAKEHOLDER_CONVERSATION.md](STAKEHOLDER_CONVERSATION.md).

- Read the selected skill file before conducting the task.
- Use its linked digested knowledge and worksheet.
- Keep converted source slides and notes separate from default task guidance.
- A review command is not a substitute for a requested murderboard.

- Use `advise_me` when the user needs help choosing a work method.
- Respect an explicitly selected suitable skill rather than routing every request through the advisor.
