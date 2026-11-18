# Causal Analysis

- **Basis:** authored method guidance; validate suitability against the task evidence.
- **Shared method:** [Analytical evidence and handoff](../methods/evidence-and-handoff.md).

## Inputs

- Treatment, outcome, target population, causal estimand, timing, assignment mechanism, potential confounders, and data.

## Method

- Draw the causal assumptions and time ordering before selecting adjustment variables.
- Distinguish prediction from identification of an intervention effect.
- Prefer randomized evidence where available; otherwise justify the observational design.
- State assumptions such as exchangeability, overlap, consistency, and limited interference where relevant.
- Avoid adjusting for colliders or post-treatment variables when estimating a total effect.
- For difference-in-differences, investigate pre-trends and treatment timing; a non-significant pre-trend test does not prove parallel trends.
- For instrumental variables or discontinuity designs, state their specific identifying assumptions and applicable population.
- Assess overlap, balance, uncertainty, placebo tests, and sensitivity to unmeasured confounding as appropriate.
- Downgrade conclusions when the design cannot separate intervention effects from competing causes.

## Deliverable

- Causal question, assumption diagram, identification argument, effect with uncertainty, diagnostics, and explicit limits on causal interpretation.

## Validation probe

- A simple before/after change with a simultaneous external shock should not be reported as an identified treatment effect.
