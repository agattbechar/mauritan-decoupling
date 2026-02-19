import pandas as pd
from pathlib import Path

IN_PATH = Path("data/processed/cpi_monthly_mauritania_2020_2025.csv")
OUT_PATH = Path("data/processed/cpi_inflation_mauritania_2020_2025.csv")

def main():
    df = pd.read_csv(IN_PATH)

    # Parse date and sort
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)

    # Compute inflation rates from index
    # MoM % = (CPI_t / CPI_{t-1} - 1) * 100
    df["infl_mom_pct"] = df["cpi_index"].pct_change() * 100

    # YoY % = (CPI_t / CPI_{t-12} - 1) * 100
    df["infl_yoy_pct"] = df["cpi_index"].pct_change(12) * 100

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_PATH, index=False)

    print("Saved:", OUT_PATH)
    print("\nFirst 15 rows:")
    print(df.head(15).to_string(index=False))
    print("\nLast 15 rows:")
    print(df.tail(15).to_string(index=False))

if __name__ == "__main__":
    main()
