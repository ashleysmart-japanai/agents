# Scenario Analysis

- **View:** this diagram renders in a Markdown viewer with Mermaid support.
- **Data:** [scenario-analysis.json](scenario-analysis.json).
- **Boundary:** converted source slides/notes are excluded from this skill context.

```mermaid
flowchart TD
  n0["Analytical Evidence and Handoff"]
  n1["Scenario Analysis"]
  n2["Scenario Analysis [skill]"]
  n1 -->|derived_from| n0
  n2 -->|derived_from| n0
  n2 -->|derived_from| n1
```

## Knowledge pages

- [Analytical Evidence and Handoff](../methods/evidence-and-handoff.md).
- [Scenario Analysis](../scenario-analysis/index.md).
- [Scenario Analysis [skill]](../../../skills/analyst/scenario-analysis/SKILL.md).
