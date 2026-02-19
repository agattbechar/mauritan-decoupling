import pandas as pd

paths = [
    "data/processed/cpi_inflation_mauritania_2020_2025.csv",
    "data/processed/fx_usd_monthly_2020_2025.csv",
    "data/processed/merged_fx_cpi_2020_2025.csv",
]

for p in paths:
    df = pd.read_csv(p)
    df["date"] = pd.to_datetime(df["date"])
    print("\n", p)
    print("rows:", len(df))
    print("min:", df["date"].min(), "max:", df["date"].max())
    print("missing dates:", df["date"].isna().sum())

