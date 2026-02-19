import pandas as pd
import statsmodels.api as sm

LAG = 0  # change this after seeing lag correlations

df = pd.read_csv("data/processed/merged_fx_cpi_2020_2025.csv")
df["date"] = pd.to_datetime(df["date"])

df["fx_lag"] = df["fx_mom_pct"].shift(LAG)

# Use MoM inflation baseline
df = df.dropna(subset=["infl_mom_pct", "fx_lag"]).copy()

Y = df["infl_mom_pct"]
X = sm.add_constant(df["fx_lag"])

model = sm.OLS(Y, X).fit()

print("Observations:", len(df))
print(model.summary())
