# Construction Equipment Cost Estimation

Time series forecasting of acquisition costs for two construction equipment units over a 3-year project horizon (2025–2027), based on historical raw material price data.

## Problem

The goal is to estimate the total rental cost for two pieces of construction equipment over a 36-month project. Equipment prices are derived from a base-price formula that depends on the daily prices of three raw materials (X, Y, Z), for which historical time series data is available.

## Approach

Rather than forecasting each material individually (which would compound uncertainty through the base-price formula), the equipment base prices are computed from historical material data first and forecasting is applied directly to those aggregated series. This produces tighter uncertainty intervals.

[Facebook Prophet](https://facebook.github.io/prophet/) was selected as the forecasting model for its ability to handle trend, seasonality, and changepoints with minimal tuning — a solid starting point for time series with irregular behavior.

The data is aggregated to monthly resolution before fitting. Daily-scale forecasts produced exploding confidence intervals over the 3-year (1095-day) horizon; monthly aggregation significantly improved bound behavior. Monthly values are computed as the sum of daily prices, consistent with a daily rental cost model.

The COVID-19 period (2020–2022) is excluded from model fitting as an anomalous regime that would degrade forecast quality.

## Notebooks

Run in order:

1. `notebooks/01_EDA.ipynb` — Exploratory analysis and preprocessing. Writes cleaned data to `data/processed/`.
2. `notebooks/02_forecasting.ipynb` — Prophet model fitting and cost projections. Reads from `data/processed/`.

## Results

**Equipment 1 — 3-year total (2025–2027):**

| Scenario | Estimated cost |
|---|---|
| Base | $398,237.80 |
| Optimistic (lower bound) | $309,725.27 |
| Pessimistic (upper bound) | $486,177.13 |

**Equipment 2 — 3-year total (2025–2027):**

| Scenario | Estimated cost |
|---|---|
| Base | $659,765.24 |
| Optimistic (lower bound) | $531,410.41 |
| Pessimistic (upper bound) | $786,732.04 |

Per-year breakdowns are available in the forecasting notebook. See [report/report.md](report/report.md) for the full analysis with charts.

## Potential improvements

- **EDA:** Add autocorrelation, seasonality decomposition, and cross-series correlation analysis between materials.
- **Forecasting:** Benchmark against a simple mean baseline; add a pandemic-period regressor; evaluate with train/test RMSE; compare against SARIMA or tree-based regressors.
- **Data:** Experiment with forecasting on the individual material series, some of which extend further back in time (X goes back to 1988), to assess whether additional history improves accuracy.
- **Code:** Modularize preprocessing and forecasting into reusable utilities if similar analyses become recurring.
