# Regression and Predictive Modelling

- **Basis:** authored method guidance; validate suitability against the task evidence.
- **Shared method:** [Analytical evidence and handoff](../methods/evidence-and-handoff.md).

## Inputs

- Target, prediction time, row or entity grain, features available at prediction, sample, error costs, and deployment population.

## Method

- Define the prediction event and prevent target or future-information leakage.
- Split by time, group, or entity according to the intended use.
- Fit preprocessing and feature selection inside training folds.
- Establish a simple baseline before tuning complex models.
- Choose metrics aligned with imbalance and decision costs.
- Use validation data for tuning and keep final test data untouched until model selection is complete.
- Inspect residuals or calibration and performance across meaningful subgroups.
- Report uncertainty or prediction intervals when appropriate.
- Distinguish coefficient associations and feature importance from causal effects.
- Identify unsupported extrapolation and distribution shifts.

## Deliverable

- Reproducible model pipeline, feature contract, baseline comparison, held-out results, calibration or residual diagnostics, and use limitations.

## Validation probe

- A feature recorded after the target event should be excluded even if it sharply improves validation accuracy.
