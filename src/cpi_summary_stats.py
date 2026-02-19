import pandas as pd

df = pd.read_csv("data/processed/cpi_inflation_mauritania_2020_2025.csv")
df["date"] = pd.to_datetime(df["date"])

print("Date range:", df["date"].min(), "to", df["date"].max())
print("\nMoM inflation summary:")
print(df["infl_mom_pct"].describe())

print("\nYoY inflation summary:")
print(df["infl_yoy_pct"].describe())

print("\nMax MoM month:")
print(df.loc[df["infl_mom_pct"].idxmax()])

print("\nMin MoM month:")
print(df.loc[df["infl_mom_pct"].idxmin()])
