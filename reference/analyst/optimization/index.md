# Optimization

- **Basis:** authored method guidance; validate suitability against the task evidence.
- **Shared method:** [Analytical evidence and handoff](../methods/evidence-and-handoff.md).

## Inputs

- Decision variables, objective, units, hard and soft constraints, variable bounds, integrality, uncertainty, and operational tolerances.

## Method

- Translate the decision into variables, an objective, and constraints with consistent units.
- Distinguish hard feasibility requirements from preferences expressed as penalties.
- Check whether a simple feasible baseline exists.
- Choose a solver suited to linearity, nonlinearity, discreteness, and problem scale.
- Report solver status, time limits, and optimality gap where available.
- Independently recompute the objective and constraint violations from the returned solution.
- Do not label a feasible time-limited solution globally optimal without evidence.
- Diagnose infeasibility before relaxing constraints; name any proposed relaxation explicitly.
- Evaluate sensitivity and robustness to uncertain inputs.
- Expose trade-offs when objectives conflict instead of inventing stakeholder weights.

## Deliverable

- Model specification, feasible allocation, objective value, constraint residuals, solver status or gap, and sensitivity to assumptions.

## Validation probe

- For maximize 3x+2y with x+y<=4, x<=2, x,y>=0, recover x=2, y=2 and objective 10; an infeasible variant should be reported as infeasible.
