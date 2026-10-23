# Fashion Data Quality & Error Handling

## Objective
A practical, reproducible demonstration of data-quality assessment for apparel and textile product data. It checks completeness, duplicate identifiers, invalid values, inconsistent labels and potential outliers.

## Contents
- `data/fashion_products_sample.csv` — synthetic product records with deliberately introduced quality issues.
- `scripts/data_quality_checks.py` — Python script for profiling, issue detection, conservative standardization and report generation.
- `reports/Fashion_Data_Quality_Error_Handling_Guide.docx` — detailed methodology report.
- `reports/quality_issues.csv` — row-level issues detected by the script.
- `reports/quality_summary.csv` — field-level missingness and issue summary.
- `reports/fashion_products_standardized.csv` — standardized output with a review flag; questionable values are not silently removed.

## Run locally
Python 3.10+ is recommended.

```bash
pip install -r requirements.txt
python scripts/data_quality_checks.py
```

Run from the project root. The script writes report files to `reports/`.

## Checks demonstrated
- Missing required or optional values
- Repeated SKUs (flagged for review, not blindly deleted)
- Negative prices and stock quantities
- Non-positive fabric GSM
- Potential fabric GSM outliers using the IQR rule
- Whitespace and casing normalization for category and colour

## Important methodology notes
The data is **synthetic** and intended only for demonstration. It is not real sales, inventory, supplier or textile-laboratory data. Negative stock can sometimes represent backorders or adjustments, and repeated SKUs may be valid across sizes/markets; these are flagged for investigation rather than automatically corrected. Extreme values should be checked against source units and product context before changing them.

For a real dataset, document the source URL, licence, retrieval date, field definitions, units, geographic/category coverage and known limitations. Never infer business-critical composition or compliance claims without an authoritative source.
