# Choosing an Analytical Method

- **Foundation:** [Analytical evidence and handoff](../methods/evidence-and-handoff.md).
- **Start:** identify the decision and the evidence gap before choosing a technique.
- **Sequence:** check data fitness before exploration or modelling when the result depends on data quality.
- **Selection:** distinguish describing data, predicting outcomes, estimating causal effects, simulating uncertainty, and choosing actions.
- **Scope:** run the smallest useful set of methods; do not execute the whole catalogue for every request.
- **Routing:** respect an explicitly selected suitable method.
- **Role:** this analyst supports quantitative work; DS elsewhere in this repository means deployment strategist.
- **Boundary:** each method's default context is its curated reference subset, not the full repository.

## Select a method

- **Data Quality Assessment:** [data-quality](../../../skills/analyst/data-quality/SKILL.md) — Assess whether a dataset is fit for an analysis or decision; use for missingness, duplicate records, schema inconsistencies, and suspect measurements.
- **Exploratory Data Analysis:** [exploratory-data-analysis](../../../skills/analyst/exploratory-data-analysis/SKILL.md) — Explore a dataset to understand distributions, relationships, outliers, and promising hypotheses before formal modelling.
- **Monte Carlo Analysis:** [monte-carlo](../../../skills/analyst/monte-carlo/SKILL.md) — Simulate uncertain inputs to estimate outcome distributions, threshold probabilities, and risk for a specified model.
- **Sensitivity Analysis:** [sensitivity-analysis](../../../skills/analyst/sensitivity-analysis/SKILL.md) — Identify which uncertain inputs or assumptions drive a model output or change a decision.
- **Decision Analysis:** [decision-analysis](../../../skills/analyst/decision-analysis/SKILL.md) — Compare actions under uncertainty using expected outcomes, risk preferences, and the value of further information.
- **Scenario Analysis:** [scenario-analysis](../../../skills/analyst/scenario-analysis/SKILL.md) — Compare coherent baseline, upside, downside, and stress futures when probabilities are unavailable or structural changes matter.
- **Statistical Inference:** [statistical-inference](../../../skills/analyst/statistical-inference/SKILL.md) — Estimate population effects and uncertainty or test a specified statistical hypothesis from sampled data.
- **Experiment Design and A/B Testing:** [experiment-design](../../../skills/analyst/experiment-design/SKILL.md) — Design or analyze a controlled experiment with an explicit assignment unit, outcome, sample size, and decision rule.
- **Causal Analysis:** [causal-analysis](../../../skills/analyst/causal-analysis/SKILL.md) — Evaluate whether an intervention caused an outcome using a defensible experimental or observational identification strategy.
- **Time-Series Forecasting:** [time-series-forecasting](../../../skills/analyst/time-series-forecasting/SKILL.md) — Forecast time-indexed outcomes with out-of-time evaluation and uncertainty over a specified horizon.
- **Regression and Predictive Modelling:** [predictive-modelling](../../../skills/analyst/predictive-modelling/SKILL.md) — Build and evaluate regression or classification models for prediction; use for supervised outcomes rather than causal-effect claims.
- **Segmentation and Clustering:** [segmentation-clustering](../../../skills/analyst/segmentation-clustering/SKILL.md) — Discover useful groups in customers, behaviours, or operations without assuming that clusters are true or causal categories.
- **Optimization:** [optimization](../../../skills/analyst/optimization/SKILL.md) — Choose feasible actions or allocate resources by optimizing an explicit objective under constraints.
- **Data Visualization and Reporting:** [data-visualization](../../../skills/analyst/data-visualization/SKILL.md) — Turn analytical evidence into accurate charts, tables, and decision briefs; use when presenting results or designing analytical reports.
