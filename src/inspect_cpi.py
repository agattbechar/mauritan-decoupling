import pandas as pd

fx = pd.read_excel("data/raw/bcm_fx.xlsx")

print("Column names exactly as written:")
for col in fx.columns:
    print(f"'{col}'")

print("\nFirst 5 rows:")
print(fx.head(5).to_string(index=False))

