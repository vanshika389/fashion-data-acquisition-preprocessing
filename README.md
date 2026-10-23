# Predictive Analytics for Fashion Trend Forecasting

This repository section demonstrates a reproducible forecasting workflow for fashion trend signals using monthly time-series data.

## Contents
- `reports/Fashion_Predictive_Analytics_Forecasting_Report.docx` — detailed methodology report.
- `notebooks/fashion_trend_forecasting.ipynb` — notebook demonstrating baseline forecasting, chronological holdout evaluation, MAE/RMSE, and a forecast chart.
- `data/fashion_search_interest_demo.csv` — synthetic monthly data used only to demonstrate the code.
- `scripts/forecast_demo.py` — runnable Python script for baseline forecasts and evaluation.
- `requirements.txt` — Python dependencies.

## Run the notebook
```bash
pip install -r requirements.txt
jupyter notebook
```
Open `notebooks/fashion_trend_forecasting.ipynb` and run all cells.

Or run the script:
```bash
python scripts/forecast_demo.py
```

## Important data limitation
The bundled dataset is **synthetic demonstration data**, not actual Google Trends observations, retailer sales, or market evidence. It is intended to make the workflow runnable. For real analysis, download a consistent public series from Google Trends or another permitted source, document the query/geography/date range and terms, and replace the CSV after checking its licence and limitations.

## Forecasting design
- Forecast target: monthly relative search-interest index.
- Horizon: next 3 months.
- Baseline: seasonal-naive (same month in the prior year) when history permits; fallback to last observed value for short history.
- Validation: chronological holdout, never random shuffle.
- Metrics: MAE and RMSE.
- Next step: use rolling-origin validation and compare ETS/SARIMA only after verifying sufficient history and seasonality.
