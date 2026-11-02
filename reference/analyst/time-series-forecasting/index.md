# Time-Series Forecasting

- **Basis:** authored method guidance; validate suitability against the task evidence.
- **Shared method:** [Analytical evidence and handoff](../methods/evidence-and-handoff.md).

## Inputs

- Timestamped history, frequency, horizon, target, available-at-prediction covariates, calendar effects, and forecast decision costs.

## Method

- Resolve timestamps, timezones, frequency, gaps, and revisions before modelling.
- Distinguish missing observations from genuine zero activity.
- Compare against naive and seasonal-naive forecasts where applicable.
- Use rolling-origin or expanding-window evaluation aligned to the actual prediction horizon.
- Fit transformations and models using training information only.
- Use future covariates only when they will be known at prediction time; otherwise forecast or scenario-model them.
- Check residual dependence and structural breaks.
- Report horizon-specific errors and prediction-interval coverage.
- Choose error measures compatible with zeros, scale, and decision costs.
- Separate expected future observations from uncertainty about the expected mean.

## Deliverable

- Forecast table with dates and intervals, backtest against baselines, assumptions about future drivers, and refresh or failure triggers.

## Validation probe

- A seasonal series should be evaluated against a seasonal-naive baseline; a random train/test split should be rejected for future forecasting.
