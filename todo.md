# Analyst / Data Scientist Skills

- **Goal:** add reusable analytical skills for evidence-based decisions.
- **Status:** planned skills; unchecked items are not implemented.

## First implementation group

- [ ] **Data quality assessment:** assess completeness, consistency, duplicates, and reliability.
- [ ] **Exploratory data analysis:** investigate distributions, patterns, outliers, and missing data.
- [ ] **Monte Carlo analysis:** simulate uncertain inputs to estimate outcome probabilities and ranges.
- [ ] **Sensitivity analysis:** identify the assumptions and inputs that most affect a result.
- [ ] **Decision analysis:** compare options using expected value, risk, and the value of additional information.

## Additional skills

- [ ] **Scenario analysis:** compare baseline, upside, downside, and stress cases.
- [ ] **Statistical inference:** estimate effects and uncertainty using confidence intervals and hypothesis tests.
- [ ] **Experiment design and A/B testing:** define controls, sample sizes, success metrics, and stopping rules.
- [ ] **Causal analysis:** evaluate whether an intervention caused an observed outcome.
- [ ] **Time-series forecasting:** forecast demand, workload, usage, or costs with uncertainty ranges.
- [ ] **Regression and predictive modelling:** model relationships and predict outcomes.
- [ ] **Segmentation and clustering:** identify meaningful groups of customers, behaviours, or operations.
- [ ] **Optimization:** choose actions or allocate resources under explicit constraints.
- [ ] **Data visualization and reporting:** communicate evidence through charts and decision briefs.

## Shared implementation work

- [ ] **Routing:** add an analyst entrypoint that selects skills from the decision and available evidence.
- [ ] **Inputs:** define required data, units, time horizons, and decision thresholds for each skill.
- [ ] **Assumptions:** distinguish observed evidence from estimates and modelling assumptions.
- [ ] **Uncertainty:** distinguish variability in outcomes from uncertainty in model parameters.
- [ ] **Reproducibility:** retain data provenance, model specifications, code, and random seeds where relevant.
- [ ] **Validation:** check each method against a worked example with a known result or suitable benchmark.
- [ ] **Handoff:** define outputs, limitations, and checks needed before acting on results.
