import pandas as pd
import numpy as np

df = pd.read_csv("data/processed/merged_fx_cpi_2020_2025.csv")
df["date"] = pd.to_datetime(df["date"])

# We use MoM inflation for responsiveness
infl = df["infl_mom_pct"]
fx = df["fx_mom_pct"]

print("\nLag correlation profile (FX leads inflation):")

for lag in range(0, 7):  # 0 to 6 months
    corr = infl.corr(fx.shift(lag))
    print(f"Lag {lag} months: correlation = {corr:.4f}")
print("\nFX autocorrelation:")

for lag in range(0, 7):
    corr = fx.corr(fx.shift(lag))
    print(f"Lag {lag} months: autocorr = {corr:.4f}")
