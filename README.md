# Fashion Data Acquisition & Preprocessing

A beginner-friendly, reproducible data-science project demonstrating how to acquire, profile, clean, validate, and prepare fashion product data for analysis.

## Project contents
- `data/raw/fashion_products_sample.csv` — small **synthetic demonstration dataset** containing intentional missing values, duplicate rows, inconsistent category labels, and invalid values.
- `scripts/preprocess.py` — reusable pandas preprocessing pipeline.
- `data/processed/` — output folder for cleaned data and a quality report.
- `data_dictionary.md` — column definitions and handling decisions.
- `Fashion_Data_Acquisition_Preprocessing_Guide.docx` — detailed methodology report (if included in the ZIP).
- `requirements.txt` — Python dependencies.

## Quick start
1. Install Python 3.10+.
2. In a terminal, install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run:
   ```bash
   python scripts/preprocess.py
   ```
4. Inspect `data/processed/fashion_products_cleaned.csv` and `data/processed/quality_report.txt`.

## Dataset note
The included rows are synthetic and are for demonstrating the workflow only. They are **not real retailer sales, customer records, or market evidence**. For a real analysis, replace the sample with a dataset whose licence and source are documented.

## Suggested public data sources
- Google Trends: https://trends.google.com/trends/
- UN Comtrade: https://comtradeplus.un.org/
- World Bank Open Data: https://data.worldbank.org/
- Eurostat: https://ec.europa.eu/eurostat/
- India Open Government Data: https://www.data.gov.in/
- Kaggle Datasets: https://www.kaggle.com/datasets
- Hugging Face Datasets: https://huggingface.co/datasets
- Open-Meteo: https://open-meteo.com/

Always check terms, licence, permitted reuse, geographic coverage, and update dates. Use official downloads/APIs where available; do not bypass access controls.

## Pipeline steps
1. Load raw CSV and preserve it unchanged.
2. Standardise column names and text fields.
3. Parse price and rating as numeric.
4. Identify and remove exact duplicate rows.
5. Flag impossible/invalid values; convert invalid values to missing.
6. Impute numeric values with medians and categorical values with `Unknown`.
7. Engineer `discount_pct` and `price_band`.
8. Validate key fields and export cleaned data plus a quality report.

## Limitations
This is a preprocessing demonstration, not a production forecasting model. Imputation decisions must be reconsidered for each dataset and business question. For modelling, fit imputation/scaling steps on training data only to avoid data leakage.
