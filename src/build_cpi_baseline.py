import pandas as pd
import re
from pathlib import Path

IN_PATH = Path("data/raw/imf_cpi_full.csv")
OUT_PATH = Path("data/processed/cpi_monthly_mauritania_2020_2025.csv")

COUNTRY_TARGET = "Mauritania, Islamic Republic of"
FREQ_TARGET = "Monthly"
COICOP_TARGET = "All Items"
TRANS_TARGET = "Standard reference period (2010=100), Index"

START = "2020-M02"
END = "2025-M12"

def is_month_col(c):
    return re.fullmatch(r"\d{4}-M(0[1-9]|1[0-2])", str(c)) is not None

def period_to_date(p):
    year = int(p[:4])
    month = int(p.split("-M")[1])
    return pd.Timestamp(year=year, month=month, day=1)

def main():
    print("START: build_cpi_baseline.py is running")

    df = pd.read_csv(IN_PATH, low_memory=False)

    # Normalize text
    df["COUNTRY"] = df["COUNTRY"].astype(str).str.strip()

    # Filter
    df = df[
        (df["COUNTRY"] == COUNTRY_TARGET) &
        (df["FREQUENCY"] == FREQ_TARGET) &
        (df["COICOP_1999"] == COICOP_TARGET) &
        (df["TYPE_OF_TRANSFORMATION"] == TRANS_TARGET)
    ].copy()

    if len(df) != 1:
        raise ValueError(f"Expected exactly 1 row, found {len(df)}. Check filters.")

    row = df.iloc[0]

    # Extract monthly columns
    month_cols = [c for c in df.columns if is_month_col(c)]
    month_cols = sorted([c for c in month_cols if START <= c <= END])

    data = []
    for col in month_cols:
        val = row[col]
        if pd.notna(val):
            data.append({
                "date": period_to_date(col),
                "cpi_index": float(val)
            })

    tidy = pd.DataFrame(data).sort_values("date")

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    tidy.to_csv(OUT_PATH, index=False)

    print("Saved:", OUT_PATH)
    print(tidy.head())
    print(tidy.tail())

if __name__ == "__main__":
    main()
