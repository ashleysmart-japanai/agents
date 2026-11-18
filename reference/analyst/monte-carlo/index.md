# Monte Carlo Analysis

- **Basis:** authored method guidance; validate suitability against the task evidence.
- **Shared method:** [Analytical evidence and handoff](../methods/evidence-and-handoff.md).

## Inputs

- Outcome equation or simulator, input units, bounds, distributions or data, dependencies, horizon, and decision thresholds.

## Method

- Write the deterministic model and test its units and limiting cases before sampling.
- Document the evidence for each distribution; label elicited ranges as assumptions.
- Use distributions with appropriate support; do not assign an unbounded normal to a strictly positive input without justification.
- Represent dependencies explicitly; preserve time structure or joint observations when resampling.
- Separate variability in outcomes from uncertainty about parameters and model structure.
- Use a recorded random seed and retain code, configuration, input snapshot, and dependency versions.
- Increase draws until the decision-relevant quantities stabilize to a stated tolerance across independent runs.
- Report Monte Carlo estimation error separately from the spread of simulated outcomes.
- Estimate threshold probabilities and relevant quantiles; do not interpret zero observed failures as impossible failure.
- Compare alternative plausible distribution and dependence assumptions.
- Use paired random draws when comparing options under the same uncertain future.

## Deliverable

- Reproducible simulation code, assumption table, outcome quantiles, threshold probabilities with estimation uncertainty, convergence evidence, and decision limitations.

## Validation probe

- For X uniform on [0,1] and Y=2X, recover mean 1, P(Y>1.5)=0.25, and the 95th percentile 1.9 within declared Monte Carlo tolerances.
