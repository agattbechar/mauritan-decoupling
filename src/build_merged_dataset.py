import pandas as pd
from pathlib import Path

CPI_PATH = Path("data/processed/cpi_inflation_mauritania_2020_2025.csv")
FX_PATH = Path("data/processed/fx_usd_monthly_2020_2025.csv")
OUT_PATH = Path("data/processed/merged_fx_cpi_2020_2025.csv")

def main():
    cpi = pd.read_csv(CPI_PATH)
    fx = pd.read_csv(FX_PATH)

    cpi["date"] = pd.to_datetime(cpi["date"])
    fx["date"] = pd.to_datetime(fx["date"])

    merged = pd.merge(cpi, fx, on="date", how="inner")
    merged = merged.sort_values("date").reset_index(drop=True)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(OUT_PATH, index=False)

    print("Saved:", OUT_PATH)
    print("\nFirst 10 rows:")
    print(merged.head(10).to_string(index=False))
    print("\nLast 10 rows:")
    print(merged.tail(10).to_string(index=False))

if __name__ == "__main__":
    main()
