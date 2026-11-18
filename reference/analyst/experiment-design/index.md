# Experiment Design and A/B Testing

- **Basis:** authored method guidance; validate suitability against the task evidence.
- **Shared method:** [Analytical evidence and handoff](../methods/evidence-and-handoff.md).

## Inputs

- Hypothesis, assignment unit, eligible population, baseline outcome variation, minimum relevant effect, exposure period, and guardrails.

## Method

- Choose randomization at a unit that limits spillover and contamination.
- Specify primary outcome, estimand, practical effect threshold, and guardrails before inspecting treatment effects.
- Compute sample size or power from the design assumptions; account for clustering and attrition.
- Specify fixed-horizon or valid sequential analysis and its stopping rules in advance.
- Check allocation integrity, sample-ratio mismatch, logging, and differential missingness.
- Use intention-to-treat as the primary assignment-based analysis when appropriate.
- Handle multiple variants and metrics with a declared multiplicity policy.
- Report effect sizes and intervals alongside guardrail outcomes.
- Separate a statistically detectable effect from a worthwhile operational change.

## Deliverable

- Experiment protocol or results report with assignment, sample-size rationale, stopping rule, integrity checks, effect estimates, and decision criteria.

## Validation probe

- A deliberately skewed allocation should trigger investigation before interpreting treatment lift; repeated unadjusted significance checks should fail the design review.
