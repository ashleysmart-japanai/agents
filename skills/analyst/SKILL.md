---
name: analyst
description: Choose and apply quantitative analysis methods for a data question or decision, including uncertainty simulation, forecasting, inference, experiments, prediction, and optimization. Use when an analyst is requested or the analytical method is unclear; do not replace deployment-strategy advice with statistical modelling.
---

# Analyst / Data Scientist

- **Read:** [Method selection](../../reference/analyst/routing/index.md).
- **Read:** [Evidence and handoff](../../reference/analyst/methods/evidence-and-handoff.md).
- **Clarify:** establish the decision, data available, unit of analysis, horizon, and acceptable uncertainty.
- **Select:** explain which method resolves the next evidence gap.
- **Load:** read the selected child skill before executing it.
- **Proceed:** perform the authorized analysis rather than stopping at a method recommendation.
- **Boundary:** if the user asks only for advice, recommend a method without treating that as permission for a new data operation.
- **Knowledge:** use [the analyst graph](../../reference/analyst/knowladge_graph/README.md) to select methods, then load the selected skill's bounded graph.

## Skills

- `/data-quality` → [Data Quality Assessment](data-quality/SKILL.md).
- `/exploratory-data-analysis` → [Exploratory Data Analysis](exploratory-data-analysis/SKILL.md).
- `/monte-carlo` → [Monte Carlo Analysis](monte-carlo/SKILL.md).
- `/sensitivity-analysis` → [Sensitivity Analysis](sensitivity-analysis/SKILL.md).
- `/decision-analysis` → [Decision Analysis](decision-analysis/SKILL.md).
- `/scenario-analysis` → [Scenario Analysis](scenario-analysis/SKILL.md).
- `/statistical-inference` → [Statistical Inference](statistical-inference/SKILL.md).
- `/experiment-design` → [Experiment Design and A/B Testing](experiment-design/SKILL.md).
- `/causal-analysis` → [Causal Analysis](causal-analysis/SKILL.md).
- `/time-series-forecasting` → [Time-Series Forecasting](time-series-forecasting/SKILL.md).
- `/predictive-modelling` → [Regression and Predictive Modelling](predictive-modelling/SKILL.md).
- `/segmentation-clustering` → [Segmentation and Clustering](segmentation-clustering/SKILL.md).
- `/optimization` → [Optimization](optimization/SKILL.md).
- `/data-visualization` → [Data Visualization and Reporting](data-visualization/SKILL.md).
