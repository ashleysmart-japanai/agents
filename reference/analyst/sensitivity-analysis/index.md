# Sensitivity Analysis

- **Basis:** authored method guidance; validate suitability against the task evidence.
- **Shared method:** [Analytical evidence and handoff](../methods/evidence-and-handoff.md).

## Inputs

- Executable model, input ranges or joint distributions, baseline, output metric, and decision threshold.

## Method

- Distinguish local derivatives, one-at-a-time scenarios, and global sensitivity to a joint uncertainty model.
- Set meaningful input ranges and preserve feasibility constraints when perturbing inputs.
- Use one-at-a-time analysis for local questions; disclose that it can miss interactions.
- Choose a global method when nonlinearities or interactions matter.
- Use independent-input variance decompositions only when independence is justified; otherwise use a dependence-aware method or conditional scenario analysis.
- Separate parameter influence from parameter uncertainty.
- Use common random numbers where helpful to reduce simulation noise between comparisons.
- Check ranking stability under resampling and plausible input-range changes.
- Locate break-even thresholds where the preferred action changes.

## Deliverable

- Influence ranking with units and ranges, interaction caveats, ranking stability, and decision-switch thresholds.

## Validation probe

- For Y=X1*X2 near (0,0), show that one-at-a-time changes miss the interaction revealed by jointly varying both inputs.
