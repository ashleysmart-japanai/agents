# Analyst / Data Scientist Skills

- **Goal:** add reusable analytical skills for evidence-based decisions.
- **Status:** 14 grouped skills and the analyst router are authored; numerical workflow evaluations remain pending.

## First implementation group

- [x] **Data quality assessment:** assess completeness, consistency, duplicates, and reliability.
- [x] **Exploratory data analysis:** investigate distributions, patterns, outliers, and missing data.
- [x] **Monte Carlo analysis:** simulate uncertain inputs to estimate outcome probabilities and ranges.
- [x] **Sensitivity analysis:** identify the assumptions and inputs that most affect a result.
- [x] **Decision analysis:** compare options using expected value, risk, and the value of additional information.

## Additional skills

- [x] **Scenario analysis:** compare baseline, upside, downside, and stress cases.
- [x] **Statistical inference:** estimate effects and uncertainty using confidence intervals and hypothesis tests.
- [x] **Experiment design and A/B testing:** define controls, sample sizes, success metrics, and stopping rules.
- [x] **Causal analysis:** evaluate whether an intervention caused an observed outcome.
- [x] **Time-series forecasting:** forecast demand, workload, usage, or costs with uncertainty ranges.
- [x] **Regression and predictive modelling:** model relationships and predict outcomes.
- [x] **Segmentation and clustering:** identify meaningful groups of customers, behaviours, or operations.
- [x] **Optimization:** choose actions or allocate resources under explicit constraints.
- [x] **Data visualization and reporting:** communicate evidence through charts and decision briefs.

## Shared implementation work

- [x] **Routing:** add an analyst entrypoint that selects skills from the decision and available evidence.
- [x] **Inputs:** define required data, units, time horizons, and decision thresholds for each skill.
- [x] **Assumptions:** distinguish observed evidence from estimates and modelling assumptions.
- [x] **Uncertainty:** distinguish variability in outcomes from uncertainty in model parameters.
- [x] **Reproducibility:** retain data provenance, model specifications, code, and random seeds where relevant.
- [ ] **Validation:** check each method against a worked example with a known result or suitable benchmark.
- [x] **Handoff:** define outputs, limitations, and checks needed before acting on results.

## Created resources

- **Skills:** [Analyst entrypoint](skills/analyst/SKILL.md).
- **Knowledge:** [Curated analyst graph](reference/analyst/knowladge_graph/README.md).
- **Checks:** metadata and links validated; graph boundary and deterministic-generation tests pass.
- **Evaluation:** each method includes a validation probe; these are not claims that all numerical workflows have been executed.
