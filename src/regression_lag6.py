import pandas as pd
import statsmodels.api as sm

df = pd.read_csv("data/processed/merged_fx_cpi_2020_2025.csv")
df["date"] = pd.to_datetime(df["date"])

# Use MoM inflation
df["fx_lag6"] = df["fx_mom_pct"].shift(6)

df = df.dropna(subset=["infl_mom_pct", "fx_lag6"]).copy()

Y = df["infl_mom_pct"]
X = df["fx_lag6"]

X = sm.add_constant(X)

model = sm.OLS(Y, X).fit()

print(model.summary())
