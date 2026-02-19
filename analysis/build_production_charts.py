import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# ----------------------------
# Load Data
# ----------------------------

df = pd.read_csv("data/processed/merged_fx_cpi_2020_2025.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

# Ensure output folder exists
os.makedirs("analysis/outputs", exist_ok=True)

# ----------------------------
# 1) CPI Index
# ----------------------------

plt.figure(figsize=(10,5))
plt.plot(df["date"], df["cpi_index"], linewidth=2)
plt.title("CPI Index (2010=100)")
plt.xlabel("Date")
plt.ylabel("Index Level")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("analysis/outputs/cpi_index.png", dpi=300)
plt.close()

# ----------------------------
# 2) Inflation MoM
# ----------------------------

plt.figure(figsize=(10,5))
plt.plot(df["date"], df["infl_mom_pct"], linewidth=2)
plt.title("Monthly Inflation (MoM, %)")
plt.xlabel("Date")
plt.ylabel("Percent")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("analysis/outputs/infl_mom.png", dpi=300)
plt.close()

# ----------------------------
# 3) FX Monthly Change
# ----------------------------

plt.figure(figsize=(10,5))
plt.plot(df["date"], df["fx_mom_pct"], linewidth=2)
plt.title("USD/MRU Monthly Change (MoM, %)")
plt.xlabel("Date")
plt.ylabel("Percent")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("analysis/outputs/fx_mom.png", dpi=300)
plt.close()

# ----------------------------
# 4) Volatility (Rolling 6-month std)
# ----------------------------

df["infl_vol_6m"] = df["infl_mom_pct"].rolling(6).std()
df["fx_vol_6m"] = df["fx_mom_pct"].rolling(6).std()

plt.figure(figsize=(10,5))
plt.plot(df["date"], df["infl_vol_6m"], label="Inflation Volatility (6m)", linewidth=2)
plt.plot(df["date"], df["fx_vol_6m"], label="FX Volatility (6m)", linewidth=2)
plt.title("Rolling 6-Month Volatility")
plt.xlabel("Date")
plt.ylabel("Std Dev")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("analysis/outputs/volatility.png", dpi=300)
plt.close()

print("Production charts saved successfully.")
