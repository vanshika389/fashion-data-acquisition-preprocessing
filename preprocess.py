from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_FILE = ROOT / "data" / "raw" / "fashion_products_sample.csv"
OUT_DIR = ROOT / "data" / "processed"
OUT_DIR.mkdir(parents=True, exist_ok=True)

def main():
    df = pd.read_csv(RAW_FILE)
    initial_rows = len(df)
    initial_missing = int(df.isna().sum().sum())
    exact_duplicates = int(df.duplicated().sum())

    # Standardise column names and whitespace in text columns.
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_", regex=False)
    text_cols = df.select_dtypes(include=["object", "string"]).columns
    for col in text_cols:
        df[col] = df[col].astype("string").str.strip()

    # Standardise known category aliases while preserving a consistent taxonomy.
    if "category" in df.columns:
        df["category"] = df["category"].str.lower()
        category_map = {
            "t-shirt": "tops",
            "t shirts": "tops",
            "t-shirt ": "tops",
            "knitwear": "tops",
        }
        df["category"] = df["category"].replace(category_map)
        df["category"] = df["category"].str.title()

    if "colour" in df.columns:
        df["colour"] = df["colour"].str.title()
    if "availability" in df.columns:
        df["availability"] = df["availability"].str.lower().str.replace(r"\s+", " ", regex=True)
        df["availability"] = df["availability"].replace({
            "in stock": "In Stock", "out of stock": "Out of Stock", "preorder": "Preorder"
        })

    # Parse numeric columns; invalid values become missing for explicit treatment.
    numeric_cols = ["list_price", "sale_price", "rating", "review_count"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    for col in ["list_price", "sale_price", "review_count"]:
        if col in df.columns:
            df.loc[df[col] < 0, col] = pd.NA
    if "rating" in df.columns:
        df.loc[~df["rating"].between(0, 5), "rating"] = pd.NA

    # Remove exact duplicates only. Duplicate product IDs are not automatically removed:
    # whether they are valid depends on the source's intended row grain.
    df = df.drop_duplicates().copy()

    # Impute numeric fields using medians; categorical fields with explicit Unknown.
    # In a predictive modelling workflow, learn imputation values on training data only.
    for col in numeric_cols:
        if col in df.columns and df[col].isna().any():
            median = df[col].median()
            df[col] = df[col].fillna(median) if pd.notna(median) else df[col]
    for col in df.select_dtypes(include=["object", "string"]).columns:
        df[col] = df[col].fillna("Unknown")

    # Feature engineering; protect against division by zero.
    if {"list_price", "sale_price"}.issubset(df.columns):
        valid = df["list_price"].gt(0) & df["sale_price"].notna() & df["list_price"].notna()
        df["discount_pct"] = pd.NA
        df.loc[valid, "discount_pct"] = (
            (df.loc[valid, "list_price"] - df.loc[valid, "sale_price"])
            / df.loc[valid, "list_price"] * 100
        ).round(2)
        df["price_band"] = pd.cut(
            df["sale_price"], bins=[-float("inf"), 500, 1500, float("inf")],
            labels=["Budget", "Mid-range", "Premium"], right=False
        ).astype("string")

    output_file = OUT_DIR / "fashion_products_cleaned.csv"
    df.to_csv(output_file, index=False)

    report = [
        "FASHION DATA PREPROCESSING - QUALITY REPORT",
        f"Input file: {RAW_FILE.relative_to(ROOT)}",
        f"Input rows: {initial_rows}",
        f"Rows after exact duplicate removal: {len(df)}",
        f"Exact duplicate rows detected: {exact_duplicates}",
        f"Missing cells before cleaning: {initial_missing}",
        f"Missing cells after cleaning: {int(df.isna().sum().sum())}",
        f"Output columns: {', '.join(df.columns)}",
        "",
        "Note: This project uses synthetic demonstration data. Imputation and category mappings are examples, not universal rules."
    ]
    (OUT_DIR / "quality_report.txt").write_text("\n".join(report), encoding="utf-8")
    print("\n".join(report))
    print(f"\nCleaned dataset saved to: {output_file}")

if __name__ == "__main__":
    main()
