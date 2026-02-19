import re
from pathlib import Path
import pandas as pd

RAW_CPI_PATH = Path("data/raw/imf_cpi_full.csv")  # <-- change filename to your CPI csv
OUT_PATH = Path("data/processed/cpi_categories_monthly_2020_2025.csv")

COUNTRY = "Mauritania, Islamic Republic of"
START = "2020-02-01"
END = "2025-12-01"

# CPI category series codes we will use
SERIES = {
    "headline": "MRT.CPI._T.IX.M",
    "food": "MRT.CPI.CP01.IX.M",
    "transport": "MRT.CPI.CP07.IX.M",
    "housing_utilities": "MRT.CPI.CP04.IX.M",
    # services proxy components
    "education": "MRT.CPI.CP10.IX.M",
    "health": "MRT.CPI.CP06.IX.M",
    "restaurants_hotels": "MRT.CPI.CP11.IX.M",
    "communication": "MRT.CPI.CP08.IX.M",
    "recreation_culture": "MRT.CPI.CP09.IX.M",
    "misc_goods_services": "MRT.CPI.CP12.IX.M",
}

MONTH_COL_RE = re.compile(r"^\d{4}-M\d{2}$")  # e.g. 2020-M02

def month_col_to_date(col: str) -> pd.Timestamp:
    # "2020-M02" -> "2020-02-01"
    year = int(col[:4])
    month = int(col[-2:])
    return pd.Timestamp(year=year, month=month, day=1)

def extract_series(df: pd.DataFrame, series_code: str, name: str) -> pd.DataFrame:
    row = df[df["SERIES_CODE"] == series_code]
    if row.empty:
        raise ValueError(f"Series code not found: {series_code} ({name})")
    if len(row) > 1:
        # Should be unique; if not, keep first but warn.
        row = row.iloc[[0]]

    month_cols = [c for c in df.columns if MONTH_COL_RE.match(str(c))]
    s = row[month_cols].T
    s.columns = [name]
    s.index = [month_col_to_date(c) for c in month_cols]
    s = s.sort_index()
    s = s.loc[(s.index >= pd.to_datetime(START)) & (s.index <= pd.to_datetime(END))]
    s = s.reset_index().rename(columns={"index": "date"})
    s[name] = pd.to_numeric(s[name], errors="coerce")
    return s

def add_inflation(df: pd.DataFrame, col: str) -> pd.DataFrame:
    df = df.sort_values("date").copy()
    df[f"{col}_infl_mom_pct"] = df[col].pct_change() * 100
    df[f"{col}_infl_yoy_pct"] = df[col].pct_change(12) * 100
    return df

def main():
    df = pd.read_csv(RAW_CPI_PATH)
    df = df[df["COUNTRY"] == COUNTRY].copy()

    # Keep only monthly "Index" series rows to avoid accidental mixing
    df = df[(df["FREQUENCY"] == "Monthly") & (df["TYPE_OF_TRANSFORMATION"] == "Index")].copy()

    series_frames = []
    for name, code in SERIES.items():
        series_frames.append(extract_series(df, code, name))

    # Merge all extracted series by date
    out = series_frames[0]
    for f in series_frames[1:]:
        out = out.merge(f, on="date", how="inner")

    # Build services proxy index as the simple average of service-like categories
    service_cols = [
        "education", "health", "restaurants_hotels",
        "communication", "recreation_culture", "misc_goods_services"
    ]
    out["services_proxy"] = out[service_cols].mean(axis=1)

    # Add inflation measures for key series
    for col in ["headline", "food", "transport", "housing_utilities", "services_proxy"]:
        out = add_inflation(out, col)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT_PATH, index=False)
    print("Saved:", OUT_PATH)
    print("Rows:", len(out), "Min date:", out["date"].min(), "Max date:", out["date"].max())
    print("Columns:", list(out.columns))

if __name__ == "__main__":
    main()
