from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

DATA_FX = Path("data/processed/merged_fx_cpi_2020_2025.csv")
DATA_CATS = Path("data/processed/cpi_categories_monthly_2020_2025.csv")
OUT = Path("analysis/outputs/09_structural_overlay.png")
OUT.parent.mkdir(parents=True, exist_ok=True)

ROLL = 24

EVENTS = [
    ("2020-03-01", "COVID"),
    ("2022-03-01", "Commodity shock"),
    ("2023-12-01", "FX reform window"),
    ("2024-08-01", "PM change"),
]

def rolling_beta(df, y_col):
    betas = []
    dates = []
    df = df.dropna(subset=[y_col, "fx_mom_pct"]).sort_values("date")
    for i in range(ROLL, len(df)+1):
        w = df.iloc[i-ROLL:i]
        Y = w[y_col]
        X = sm.add_constant(w["fx_mom_pct"])
        model = sm.OLS(Y, X).fit()
        betas.append(model.params["fx_mom_pct"])
        dates.append(w["date"].iloc[-1])
    return pd.DataFrame({"date": dates, "beta": betas})

def rolling_rho(df, y_col):
    df = df.sort_values("date").copy()
    df["lag1"] = df[y_col].shift(1)
    df = df.dropna(subset=[y_col, "lag1"])
    rhos = []
    dates = []
    for i in range(ROLL, len(df)+1):
        w = df.iloc[i-ROLL:i]
        Y = w[y_col]
        X = sm.add_constant(w["lag1"])
        model = sm.OLS(Y, X).fit()
        rhos.append(model.params["lag1"])
        dates.append(w["date"].iloc[-1])
    return pd.DataFrame({"date": dates, "rho": rhos})

def main():
    fx = pd.read_csv(DATA_FX)
    fx["date"] = pd.to_datetime(fx["date"])

    cats = pd.read_csv(DATA_CATS)
    cats["date"] = pd.to_datetime(cats["date"])

    df = cats.merge(fx[["date", "fx_mom_pct"]], on="date", how="inner")

    # Headline + Food MoM inflation
    targets = {
        "headline": "headline_infl_mom_pct",
        "food": "food_infl_mom_pct",
    }

    beta_frames = {}
    rho_frames = {}

    for name, col in targets.items():
        beta_frames[name] = rolling_beta(df, col)
        rho_frames[name] = rolling_rho(df, col)

    fig, axes = plt.subplots(2, 1, figsize=(12,8), sharex=True)

    # --- Panel 1: Rolling Beta
    for name, bdf in beta_frames.items():
        axes[0].plot(bdf["date"], bdf["beta"], label=name)

    axes[0].axhline(0, linewidth=1)
    axes[0].set_title("Rolling FX Pass-Through (β)")
    axes[0].set_ylabel("β")
    axes[0].legend()

    # --- Panel 2: Rolling Rho
    for name, rdf in rho_frames.items():
        axes[1].plot(rdf["date"], rdf["rho"], label=name)

    axes[1].axhline(0, linewidth=1)
    axes[1].set_title("Rolling Inflation Persistence (ρ)")
    axes[1].set_ylabel("ρ")
    axes[1].legend()

    for d, label in EVENTS:
        d = pd.to_datetime(d)
        axes[0].axvline(d, linestyle="--", linewidth=1)
        axes[1].axvline(d, linestyle="--", linewidth=1)

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(OUT, dpi=200)
    print("Saved:", OUT)

if __name__ == "__main__":
    main()
