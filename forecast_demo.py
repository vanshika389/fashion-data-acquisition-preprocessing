from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "fashion_search_interest_demo.csv"
OUT = ROOT / "forecast_demo.png"

df = pd.read_csv(DATA, parse_dates=["month"]).sort_values("month")
target = "search_interest_index"
if df["month"].duplicated().any():
    raise ValueError("Expected one observation per month.")
if df[target].isna().any():
    raise ValueError("Target has missing values; document a gap-handling policy first.")
if len(df) < 18:
    raise ValueError("Use more history for a meaningful seasonal baseline.")

# Chronological split: last 12 months as test set.
train = df.iloc[:-12].copy()
test = df.iloc[-12:].copy()

# Seasonal-naive forecast: same month one year earlier.
seasonal_values = df[target].iloc[-24:-12].to_numpy()
pred = seasonal_values[:len(test)]
mae = mean_absolute_error(test[target], pred)
rmse = mean_squared_error(test[target], pred) ** 0.5

print("DATA NOTE: bundled values are synthetic, for demonstration only.")
print(f"Train periods: {len(train)} | Test periods: {len(test)}")
print(f"Seasonal-naive MAE: {mae:.2f}")
print(f"Seasonal-naive RMSE: {rmse:.2f}")

plt.figure(figsize=(10, 5))
plt.plot(train["month"], train[target], label="Training data")
plt.plot(test["month"], test[target], label="Actual test values")
plt.plot(test["month"], pred, marker="o", linestyle="--", label="Seasonal-naive forecast")
plt.title("Fashion Search-Interest Forecast Demo (Synthetic Data)")
plt.xlabel("Month")
plt.ylabel("Relative interest index (illustrative)")
plt.legend()
plt.tight_layout()
plt.savefig(OUT, dpi=150)
print(f"Chart saved to: {OUT}")
