# Data Dictionary

All rows in `fashion_products_sample.csv` are synthetic examples.

| Column | Type | Description | Quality considerations |
|---|---|---|---|
| `sku` | string | Example product identifier | Check uniqueness against the correct business key; variants may need size/colour/market in the key. |
| `product_name` | string | Display name | Trim whitespace; avoid overwriting original source labels in production. |
| `category` | string | Apparel/accessory category | Normalize labels with an approved vocabulary. |
| `size` | string | Size label or dimension | Valid values depend on product category and sizing system. |
| `colour` | string | Colour name | Standardize spacing/case; confirm synonyms before mapping. |
| `material` | string | Fibre/material description | Verify composition claims against an authoritative source; percentages should be checked where parseable. |
| `price_inr` | numeric | Illustrative price in Indian rupees | Negative values require investigation; currency and tax basis must be documented. |
| `stock_qty` | numeric | Illustrative stock quantity | Negative values may indicate adjustments/backorders depending on system semantics. |
| `fabric_gsm` | numeric | Fabric mass in grams per square metre | Verify unit and plausibility by material/product; extreme values are investigation flags. |
| `supplier_id` | string | Example supplier key | Check referential integrity against a supplier master table. |
| `last_updated` | date string | Example record update date | Parse with explicit format and monitor freshness. |
