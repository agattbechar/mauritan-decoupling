from pathlib import Path
import pandas as pd

ROLL_BETA_RHO = Path("analysis/outputs/09_structural_overlay.png")  # already made
DATA_FX = Path("data/processed/merged_fx_cpi_2020_2025.csv")
DATA_CATS = Path("data/processed/cpi_categories_monthly_2020_2025.csv")

OUT_TABLE = Path("analysis/outputs/10_regime_table.csv")
OUT_TABLE.parent.mkdir(parents=True, exist_ok=True)

# Define regimes (data-driven but clean)
REGIMES = {
    "Amplifier (2022–2023)": ("2022-01-01", "2023-12-31"),
    "Absorber (2024–2025)": ("2024-01-01", "2025-12-31"),
}

def main():
    fx = pd.read_csv(DATA_FX)
    fx["date"] = pd.to_datetime(fx["date"])

    cats = pd.read_csv(DATA_CATS)
    cats["date"] = pd.to_datetime(cats["date"])

    df = cats.merge(fx[["date", "fx_mom_pct"]], on="date", how="inner").sort_values("date")

    # Use the already-computed rolling series? If not saved, compute quick proxies:
    # We'll use simple regressions + AR(1) within each regime (clean & understandable).

    rows = []

    for reg_name, (start, end) in REGIMES.items():
        sub = df[(df["date"] >= start) & (df["date"] <= end)].copy()

        # Pass-through β: infl_mom ~ fx_mom (headline + food)
        import statsmodels.api as sm

        def beta(ycol):
            s = sub.dropna(subset=[ycol, "fx_mom_pct"])
            Y = s[ycol]
            X = sm.add_constant(s["fx_mom_pct"])
            m = sm.OLS(Y, X).fit()
            return float(m.params["fx_mom_pct"])

        # Persistence ρ: infl_mom ~ infl_mom(-1)
        def rho(ycol):
            s = sub[["date", ycol]].dropna().sort_values("date")
            s["lag1"] = s[ycol].shift(1)
            s = s.dropna()
            Y = s[ycol]
            X = sm.add_constant(s["lag1"])
            m = sm.OLS(Y, X).fit()
            return float(m.params["lag1"])

        rows.append({
            "regime": reg_name,
            "beta_headline": beta("headline_infl_mom_pct"),
            "beta_food": beta("food_infl_mom_pct"),
            "rho_headline": rho("headline_infl_mom_pct"),
            "rho_food": rho("food_infl_mom_pct"),
            "n_months": len(sub),
        })

    out = pd.DataFrame(rows)
    out.to_csv(OUT_TABLE, index=False)
    print("Saved:", OUT_TABLE)
    print(out)

if __name__ == "__main__":
    main()
