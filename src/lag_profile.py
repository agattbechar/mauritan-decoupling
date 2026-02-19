import pandas as pd

df = pd.read_csv("data/processed/merged_fx_cpi_2020_2025.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

def lag_profile(y_col, x_col, max_lag=12):
    y = df[y_col]
    x = df[x_col]
    out = []
    for lag in range(max_lag + 1):
        out.append((lag, y.corr(x.shift(lag))))
    return out

print("Lag profile: corr(infl_mom_pct(t), fx_mom_pct(t-lag))")
for lag, c in lag_profile("infl_mom_pct", "fx_mom_pct", 12):
    print(lag, round(c, 4))

print("\nLag profile: corr(infl_yoy_pct(t), fx_mom_pct(t-lag))")
for lag, c in lag_profile("infl_yoy_pct", "fx_mom_pct", 12):
    print(lag, round(c, 4))

