# Statistical Inference

- **Basis:** authored method guidance; validate suitability against the task evidence.
- **Shared method:** [Analytical evidence and handoff](../methods/evidence-and-handoff.md).

## Inputs

- Estimand, population, sampling mechanism, observational unit, dependence structure, sample, and practical effect threshold.

## Method

- Define the estimand and hypothesis before choosing a test.
- Identify paired, clustered, repeated, or time-dependent observations.
- Check sampling bias and measurement limitations that uncertainty intervals cannot fix.
- Choose a model or resampling method compatible with the data and sampling design.
- Report effect size and uncertainty in meaningful units alongside any p-value.
- Distinguish confidence intervals, prediction intervals, and Bayesian credible intervals.
- Account for multiple comparisons and exploratory selection when interpreting evidence.
- Do not treat a non-significant result as proof of equality; use an appropriate equivalence design for that claim.
- Check robustness to influential observations and plausible modelling choices.

## Deliverable

- Estimand, method justification, effect and interval, assumptions, diagnostic evidence, and practical interpretation.

## Validation probe

- Repeated observations from the same person should use the person-level dependence structure rather than falsely treating every row as independent.
