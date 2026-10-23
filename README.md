# Fashion EDA: Trend Exploration and Visualisation

This folder contains a reproducible exploratory data analysis (EDA) example for fashion trend analysis.

## Files
- `notebooks/fashion_eda.ipynb` — step-by-step EDA notebook with summary statistics, data-quality checks, trend lines, bar and pie charts, scatter plots, correlation, and IQR outlier checks.
- `data/fashion_eda_sample.csv` — synthetic example data.
- `reports/Fashion_Exploratory_Data_Analysis_Report.docx` — written report (add this file from the report download if not included).
- `requirements.txt` — Python dependencies.

## Run it
1. Install Python 3.10+.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start Jupyter:
   ```bash
   jupyter notebook
   ```
4. Open `notebooks/fashion_eda.ipynb` and run all cells.

## Data disclaimer
The bundled CSV is **synthetic demonstration data**, not actual market or retailer data. It is included to show the EDA workflow and charting techniques. Do not present its values as real fashion-industry findings. Before making market claims, replace it with a publicly available dataset and document the source, licence, retrieval date, geographic coverage, and limitations.

## Potential public sources
- Google Trends: https://trends.google.com/trends/
- UN Comtrade: https://comtradeplus.un.org/
- World Bank Open Data: https://data.worldbank.org/
- Eurostat: https://ec.europa.eu/eurostat/
- India Open Government Data: https://www.data.gov.in/
- Kaggle: https://www.kaggle.com/datasets
- Hugging Face Datasets: https://huggingface.co/datasets
- Open-Meteo: https://open-meteo.com/

## Suggested EDA questions
- How does search interest change over time?
- Which categories dominate the selected dataset?
- How do price, rating and review count relate?
- Which observations are outliers and do they represent errors or valid premium products?
- Do trends persist across multiple periods and independent sources?
