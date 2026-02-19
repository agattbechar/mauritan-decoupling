import pandas as pd

def main():

    # --- 1. Load CPI file ---
    path = "data/raw/imf_cpi_full.csv"   # <-- adjust if needed
    df = pd.read_csv(path)

    # --- 2. Filter Mauritania only ---
    df = df[df["COUNTRY"] == "Mauritania, Islamic Republic of"]

    print("\nNumber of Mauritania rows:", len(df))

    print("\nUnique FREQUENCY values:")
    print(df["FREQUENCY"].unique())

    print("\nUnique TYPE_OF_TRANSFORMATION values:")
    print(df["TYPE_OF_TRANSFORMATION"].unique())

    print("\nUnique COICOP_1999 values:")
    print(df["COICOP_1999"].unique())

    # --- 3. Now extract monthly index series only ---
    monthly_index = df[
        (df["FREQUENCY"] == "Monthly") &
        (df["TYPE_OF_TRANSFORMATION"].str.contains("Index", case=False))
    ]

    print("\nMonthly index series:")
    print(monthly_index[["SERIES_CODE", "COICOP_1999"]].drop_duplicates())

if __name__ == "__main__":
    main()
