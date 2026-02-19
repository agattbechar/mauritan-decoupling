import pandas as pd
from pathlib import Path

IN_PATH = Path("data/raw/bcm_fx.xlsx")
OUT_PATH = Path("data/processed/fx_usd_monthly_2020_2025.csv")

YEARS = ["2020", "2021", "2022", "2023", "2024", "2025"]

def detect_header_row(path: Path, sheet: str, max_rows: int = 10) -> int:
    """
    Try header rows 0..max_rows-1 and pick the first one where columns
    include Date + Devise + something containing 'Cours'.
    """
    for h in range(max_rows):
        df_try = pd.read_excel(path, sheet_name=sheet, header=h)
        cols = [str(c).strip().lower() for c in df_try.columns]

        has_date = any("date" == c or "date" in c for c in cols)
        has_devise = any("devise" == c or "devise" in c for c in cols)
        has_cours = any("cours" in c for c in cols)

        if has_date and has_devise and has_cours:
            return h

    raise ValueError(f"Could not detect header row for sheet {sheet}. Columns looked like: {df_try.columns}")

def pick_col(columns, keyword: str) -> str:
    keyword = keyword.lower()
    for c in columns:
        if keyword in str(c).strip().lower():
            return c
    raise ValueError(f"Could not find column containing '{keyword}' in columns: {list(columns)}")

def main():
    frames = []

    for year in YEARS:
        header_row = detect_header_row(IN_PATH, sheet=year)
        print(f"Reading sheet {year} with header row {header_row}")

        df_year = pd.read_excel(IN_PATH, sheet_name=year, header=header_row)
        df_year.columns = [str(c).strip() for c in df_year.columns]

        # Identify columns even if names differ (Cours 2 vs Cours de Référence 2, etc.)
        date_col = pick_col(df_year.columns, "date")
        curr_col = pick_col(df_year.columns, "devise")
        rate_col = pick_col(df_year.columns, "cours")

        df_year = df_year[[date_col, curr_col, rate_col]].copy()
        df_year.columns = ["date", "currency", "rate"]

        frames.append(df_year)

    df = pd.concat(frames, ignore_index=True)

    # Clean types
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["currency"] = df["currency"].astype(str).str.strip()
    df["rate"] = pd.to_numeric(df["rate"], errors="coerce")
    df = df.dropna(subset=["date", "currency", "rate"])

    # Filter USD
    usd = df[df["currency"] == "USD"].copy().sort_values("date")

    print("\nRaw USD date range:")
    print(usd["date"].min(), "to", usd["date"].max())
    print("Raw USD rows:", len(usd))

    # Monthly average (Month Start)
    monthly = (
        usd.set_index("date")["rate"]
        .resample("MS")
        .mean()
        .reset_index()
        .rename(columns={"rate": "fx_usd_avg"})
    )

    monthly["fx_mom_pct"] = monthly["fx_usd_avg"].pct_change() * 100

    # Match CPI window
    monthly = monthly[(monthly["date"] >= "2020-02-01") & (monthly["date"] <= "2025-12-01")].copy()

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    monthly.to_csv(OUT_PATH, index=False)

    print("\nFinal FX monthly rows:", len(monthly))
    print("\nFirst 5 rows:")
    print(monthly.head(5).to_string(index=False))
    print("\nLast 5 rows:")
    print(monthly.tail(5).to_string(index=False))

if __name__ == "__main__":
    main()
