import pandas as pd
import statsmodels.api as sm

LAG = 0  # set after lag_profile.py

df = pd.read_csv("data/processed/merged_fx_cpi_2020_2025.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

df["fx_lag"] = df["fx_mom_pct"].shift(LAG)
df["infl_lag1"] = df["infl_mom_pct"].shift(1)

d = df.dropna(subset=["infl_mom_pct", "fx_lag", "infl_lag1"]).copy()

Y = d["infl_mom_pct"]
X = sm.add_constant(d[["fx_lag", "infl_lag1"]])

m = sm.OLS(Y, X).fit(cov_type="HAC", cov_kwds={"maxlags": 6})

print("Observations:", len(d))
print(m.summary())
