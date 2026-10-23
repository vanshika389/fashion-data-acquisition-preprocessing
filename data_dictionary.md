# Data Dictionary

The sample dataset is synthetic and only intended to demonstrate data-quality handling.

| Column | Meaning | Expected type | Cleaning / validation |
|---|---|---|---|
| product_id | Product identifier | string | Trim whitespace; retain as identifier, not a numeric measure |
| product_name | Display name | string | Trim whitespace |
| category | Product category | categorical | Trim and lowercase; map common variants |
| colour | Product colour | categorical | Trim and title-case |
| list_price | Original/list price | numeric | Parse numeric; negative values invalid |
| sale_price | Current sale price | numeric | Parse numeric; negative values invalid |
| rating | Average product rating | numeric | Valid range is 0–5; outside range set missing |
| review_count | Number of reviews | integer | Negative values invalid |
| availability | Availability label | categorical | Standardise labels where possible |

## Engineered fields
- `discount_pct`: `(list_price - sale_price) / list_price * 100`; only calculated when list price is positive and both prices exist.
- `price_band`: `Budget` (< 500), `Mid-range` (500–1499.99), or `Premium` (>= 1500), based on sale price. Thresholds are illustrative and should be adapted to market and currency.
