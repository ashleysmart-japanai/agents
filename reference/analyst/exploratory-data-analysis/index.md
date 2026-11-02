# Exploratory Data Analysis

- **Basis:** authored method guidance; validate suitability against the task evidence.
- **Shared method:** [Analytical evidence and handoff](../methods/evidence-and-handoff.md).

## Inputs

- Data snapshot, variable definitions, row grain, target question, population, and available grouping or time fields.

## Method

- Check data quality and sampling coverage before interpreting patterns.
- Summarize distributions with counts, missingness, quantiles, and appropriate measures of spread.
- Plot skew, multimodality, extreme values, and time structure rather than relying on averages.
- Compare relationships within meaningful cohorts to expose aggregation effects.
- Inspect outliers in source context before excluding them.
- Label discovered associations and post-hoc hypotheses as exploratory.
- Separate exploratory data from any holdout reserved for later confirmation.
- Choose a small set of hypotheses and the evidence needed to test each.

## Deliverable

- Exploratory report with reproducible summaries, labeled charts, observed patterns, competing explanations, and follow-up questions.

## Validation probe

- Use grouped data with a reversed aggregate trend; report the within-group and aggregate relationships separately.
