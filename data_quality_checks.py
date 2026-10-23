"""Fashion product data quality checks and conservative cleaning demo.

The bundled CSV is synthetic and deliberately includes example defects.
The script flags questionable records and writes cleaned/issue-report outputs.
It does not invent missing business-critical values or silently delete outliers.
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "fashion_products_sample.csv"
OUT_DIR = ROOT / "reports"
OUT_DIR.mkdir(exist_ok=True)

df = pd.read_csv(INPUT)
original = df.copy()
issues = []

def add_issue(mask, field, issue_type, recommendation):
    for idx in df.index[mask.fillna(False)]:
        issues.append({
            "row_number": int(idx) + 2,  # CSV header is row 1
            "sku": df.at[idx, "sku"] if "sku" in df.columns else None,
            "field": field,
            "issue_type": issue_type,
            "observed_value": str(df.at[idx, field]) if field in df.columns else "",
            "recommended_action": recommendation,
        })

# Missingness
for col in df.columns:
    mask = df[col].isna() | df[col].astype("string").str.strip().eq("")
    add_issue(mask, col, "missing_value", "Verify against the authoritative product or supplier source; do not guess.")

# Duplicated SKU: treat as a review flag, because variants may require a composite key.
sku_dup = df["sku"].duplicated(keep=False)
add_issue(sku_dup, "sku", "duplicate_sku_review", "Verify the business key; variants or markets may legitimately reuse identifiers.")

# Basic domain checks
add_issue(df["price_inr"].lt(0), "price_inr", "negative_price", "Check refunds/adjustments and source mapping; correct only with evidence.")
add_issue(df["stock_qty"].lt(0), "stock_qty", "negative_stock", "Check whether this represents backorders or an inventory adjustment.")
add_issue(df["fabric_gsm"].le(0), "fabric_gsm", "nonpositive_fabric_gsm", "Verify measurement and unit with supplier or lab.")
# Robust extreme-value flag, not automatic deletion
q1 = df["fabric_gsm"].quantile(0.25)
q3 = df["fabric_gsm"].quantile(0.75)
iqr = q3 - q1
if iqr > 0:
    outlier_mask = (df["fabric_gsm"] < q1 - 1.5 * iqr) | (df["fabric_gsm"] > q3 + 1.5 * iqr)
    add_issue(outlier_mask, "fabric_gsm", "potential_outlier_iqr", "Investigate units/decimal placement; an extreme value is not automatically an error.")

# Standardization is safe to demonstrate while retaining originals in a separate file
clean = df.copy()
for col in ["category", "colour", "size", "product_name"]:
    clean[col] = clean[col].astype("string").str.strip()
clean["category"] = clean["category"].str.title()
clean["colour"] = clean["colour"].str.replace(r"\s+", " ", regex=True).str.title()

# Do not remove rows or impute missing critical values automatically.
clean["quality_review_required"] = False
clean["quality_review_required"] |= clean["size"].isna()
clean["quality_review_required"] |= clean["price_inr"].lt(0)
clean["quality_review_required"] |= clean["stock_qty"].lt(0)
clean["quality_review_required"] |= clean["fabric_gsm"].gt(q3 + 1.5 * iqr) if iqr > 0 else False

issues_df = pd.DataFrame(issues).drop_duplicates()
issues_path = OUT_DIR / "quality_issues.csv"
clean_path = OUT_DIR / "fashion_products_standardized.csv"
summary_path = OUT_DIR / "quality_summary.csv"

issues_df.to_csv(issues_path, index=False)
clean.to_csv(clean_path, index=False)

summary_rows = []
for col in original.columns:
    missing_count = int(original[col].isna().sum())
    summary_rows.append({
        "metric": "missing_values",
        "field": col,
        "value": missing_count,
        "notes": f"{missing_count / len(original):.1%} of {len(original)} records",
    })
summary_rows.extend([
    {"metric": "exact_duplicate_rows", "field": "all_columns", "value": int(original.duplicated().sum()), "notes": "Exact row duplicates in raw sample"},
    {"metric": "duplicate_sku_rows", "field": "sku", "value": int(sku_dup.sum()), "notes": "Review business key before removal"},
    {"metric": "flagged_issue_rows", "field": "all_fields", "value": int(issues_df["row_number"].nunique()) if not issues_df.empty else 0, "notes": "Rows with one or more detected issues"},
    {"metric": "total_issue_flags", "field": "all_fields", "value": int(len(issues_df)), "notes": "A row may have multiple issue flags"},
])
pd.DataFrame(summary_rows).to_csv(summary_path, index=False)
print(f"Input rows: {len(original)}")
print(f"Issue flags: {len(issues_df)}")
print(f"Wrote: {issues_path.relative_to(ROOT)}")
print(f"Wrote: {clean_path.relative_to(ROOT)}")
print(f"Wrote: {summary_path.relative_to(ROOT)}")
print("Note: standardized output preserves questionable records; review flags before analytical use.")
