from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

DATA_FX = Path("data/processed/merged_fx_cpi_2020_2025.csv")
DATA_CATS = Path("data/processed/cpi_categories_monthly_2020_2025.csv")
OUT_DIR = Path("analysis/outputs")
OUT_DIR.mkdir(parents=True, exist_ok=True)

EVENTS = [
    ("2020-03-01", "COVID shock"),
    ("2022-03-01", "Global commodity shock"),
    ("2023-12-01", "FX market modernization"),
    ("2024-06-01", "Election window"),
    ("2024-08-01", "New PM / cabinet reset"),
]
events = [(pd.to_datetime(d), label) for d, label in EVENTS]

ROLL_WINDOW = 24  # months

def rolling_beta(df, y_col, x_col="fx_mom_pct"):
    # rolling regression: y(t) ~ const + x(t)
    betas = []
    dates = []
    df = df.dropna(subset=[y_col, x_col]).sort_values("date")
    for i in range(ROLL_WINDOW, len(df) + 1):
        w = df.iloc[i - ROLL_WINDOW:i]
        y = w[y_col]
        X = sm.add_constant(w[x_col])
        model = sm.OLS(y, X).fit()
        betas.append(model.params[x_col])
        dates.append(w["date"].iloc[-1])
    return pd.DataFrame({"date": dates, "beta": betas})

def rolling_rho(df, y_col):
    # rolling AR(1): y(t) ~ const + y(t-1)
    rhos = []
    dates = []
    df = df.dropna(subset=[y_col]).sort_values("date").copy()
    df["y_lag1"] = df[y_col].shift(1)
    df = df.dropna(subset=["y_lag1"])
    for i in range(ROLL_WINDOW, len(df) + 1):
        w = df.iloc[i - ROLL_WINDOW:i]
        y = w[y_col]
        X = sm.add_constant(w["y_lag1"])
        model = sm.OLS(y, X).fit()
        rhos.append(model.params["y_lag1"])
        dates.append(w["date"].iloc[-1])
    return pd.DataFrame({"date": dates, "rho": rhos})

def add_event_lines(ax):
    for d, label in events:
        ax.axvline(d, linestyle="--", linewidth=1)
    # Put legend-like text only once to avoid clutter
    # (In report we’ll explain these markers clearly.)

def main():
    fx = pd.read_csv(DATA_FX)
    fx["date"] = pd.to_datetime(fx["date"])
    fx = fx.sort_values("date")

    cats = pd.read_csv(DATA_CATS)
    cats["date"] = pd.to_datetime(cats["date"])
    cats = cats.sort_values("date")

    # Merge FX with category inflation (MoM)
    df = cats.merge(fx[["date", "fx_mom_pct"]], on="date", how="inner")

    # --- Rolling betas: category MoM inflation vs FX MoM change
    targets = {
        "headline": "headline_infl_mom_pct",
        "food": "food_infl_mom_pct",
        "transport": "transport_infl_mom_pct",
        "services_proxy": "services_proxy_infl_mom_pct",
    }

    beta_frames = {}
    for name, col in targets.items():
        beta_frames[name] = rolling_beta(df, y_col=col)

    # --- Rolling rho: persistence of category MoM inflation
    rho_frames = {}
    for name, col in targets.items():
        rho_frames[name] = rolling_rho(df, y_col=col)

    # 1) Rolling betas plot
    plt.figure(figsize=(12,6))
    for name, bdf in beta_frames.items():
        plt.plot(bdf["date"], bdf["beta"], label=name)
    plt.axhline(0, linewidth=1)
    add_event_lines(plt.gca())
    plt.title("Rolling FX Pass-Through (β): category inflation vs FX change (24m window)")
    plt.xlabel("Date")
    plt.ylabel("β")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(OUT_DIR / "07_rolling_beta_categories.png", dpi=200)
    plt.close()

    # 2) Rolling rhos plot
    plt.figure(figsize=(12,6))
    for name, rdf in rho_frames.items():
        plt.plot(rdf["date"], rdf["rho"], label=name)
    plt.axhline(0, linewidth=1)
    add_event_lines(plt.gca())
    plt.title("Rolling Inflation Persistence (ρ): category MoM inflation AR(1) (24m window)")
    plt.xlabel("Date")
    plt.ylabel("ρ")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(OUT_DIR / "08_rolling_rho_categories.png", dpi=200)
    plt.close()

    print("Saved plots to:", OUT_DIR)

if __name__ == "__main__":
    main()
