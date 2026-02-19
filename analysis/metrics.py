import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.graphics.tsaplots import plot_acf

from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent / "outputs"
OUT_DIR.mkdir(exist_ok=True)

# -------------------------------------------------------
# 1. LOAD DATA
# -------------------------------------------------------
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "merged_fx_cpi_2020_2025.csv")

print("Loading data from:", DATA_PATH)

df = pd.read_csv(DATA_PATH)
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date").reset_index(drop=True)

# -------------------------------------------------------
# 2. INFLATION PERSISTENCE (Half-Life)
# -------------------------------------------------------

# Estimate AR(1) for inflation
df["infl_lag1"] = df["infl_mom_pct"].shift(1)
df_ar = df.dropna()

Y = df_ar["infl_mom_pct"]
X = sm.add_constant(df_ar["infl_lag1"])

model_ar = sm.OLS(Y, X).fit()

rho = model_ar.params["infl_lag1"]

half_life = np.log(0.5) / np.log(abs(rho))

print("Inflation persistence (rho):", round(rho,4))
print("Half-life of inflation shock (months):", round(half_life,2))

# -------------------------------------------------------
# 3. ROLLING VOLATILITY
# -------------------------------------------------------

df["infl_vol_6m"] = df["infl_mom_pct"].rolling(6).std()
df["fx_vol_6m"] = df["fx_mom_pct"].rolling(6).std()

# -------------------------------------------------------
# 4. PLOT VOLATILITY SIDE BY SIDE
# -------------------------------------------------------

fig, ax = plt.subplots(2, 1, figsize=(8,8), sharex=True)

ax[0].plot(df["date"], df["infl_vol_6m"])
ax[0].set_title("6-Month Rolling Inflation Volatility")

ax[1].plot(df["date"], df["fx_vol_6m"])
ax[1].set_title("6-Month Rolling FX Volatility")

plt.xticks(rotation=45)
plt.tight_layout()
plt.tight_layout()
plt.savefig(OUT_DIR / "01_infl_vol_6m.png", dpi=200)
plt.close()
# -------------------------------------------------------
# 5. ACF CHECK
# -------------------------------------------------------

plot_acf(df["infl_mom_pct"].dropna(), lags=12)
plt.tight_layout()
plt.savefig(OUT_DIR / "01_infl_vol_6m.png", dpi=200)
plt.close()

fig, ax = plt.subplots(figsize=(10,5))
ax.plot(df["date"], df["infl_vol_6m"], label="Inflation volatility (6m std of MoM)")
ax.plot(df["date"], df["fx_vol_6m"], label="FX volatility (6m std of MoM)")
ax.set_title("Rolling Volatility: Inflation vs FX (6-month window)")
ax.set_xlabel("Date")
ax.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(OUT_DIR / "02_volatility_side_by_side.png", dpi=200)
plt.close()

print("Shock remaining after 3 months (rho^3):", round(rho**3, 3))
# -------------------------------------------------------
# 6. ROLLING PASS-THROUGH (24-month window)
# -------------------------------------------------------

window = 24
betas = []
rhos = []
dates = []

for end in range(window, len(df)):
    sub = df.iloc[end-window:end].copy()

    sub["infl_lag1"] = sub["infl_mom_pct"].shift(1)
    sub = sub.dropna(subset=["infl_mom_pct", "fx_mom_pct", "infl_lag1"])

    Y = sub["infl_mom_pct"]
    X = sm.add_constant(sub[["fx_mom_pct", "infl_lag1"]])

    m = sm.OLS(Y, X).fit()

    betas.append(m.params["fx_mom_pct"])
    rhos.append(m.params["infl_lag1"])
    dates.append(df["date"].iloc[end])

roll = pd.DataFrame({"date": dates, "beta_fx": betas, "rho_infl": rhos})

# Save the rolling estimates (important for later report + reproducibility)
roll_path = OUT_DIR / "rolling_pass_through_24m.csv"
roll.to_csv(roll_path, index=False)
print("Saved rolling estimates to:", roll_path)

# Plot rolling beta (FX pass-through)
plt.figure(figsize=(10,5))
plt.plot(roll["date"], roll["beta_fx"])
plt.axhline(0, linewidth=1)
plt.title("Rolling FX Pass-Through (β), 24-month window")
plt.xlabel("Date")
plt.ylabel("β (effect of FX MoM on inflation MoM)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(OUT_DIR / "03_rolling_beta_fx_24m.png", dpi=200)
plt.close()

# Plot rolling rho (inflation persistence)
plt.figure(figsize=(10,5))
plt.plot(roll["date"], roll["rho_infl"])
plt.axhline(0, linewidth=1)
plt.title("Rolling Inflation Persistence (ρ), 24-month window")
plt.xlabel("Date")
plt.ylabel("ρ (inflation memory)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(OUT_DIR / "04_rolling_rho_infl_24m.png", dpi=200)
plt.close()

pre = df[df["date"] < "2023-01-01"]["fx_vol_6m"].mean()
post = df[df["date"] >= "2024-01-01"]["fx_vol_6m"].mean()

print("Average FX volatility pre-2023:", round(pre,4))
print("Average FX volatility 2024+: ", round(post,4))

pre_infl = df[df["date"] < "2023-01-01"]["infl_vol_6m"].mean()
post_infl = df[df["date"] >= "2024-01-01"]["infl_vol_6m"].mean()

print("Average inflation volatility pre-2023:", round(pre_infl,4))
print("Average inflation volatility 2024+: ", round(post_infl,4))

plt.figure(figsize=(10,5))
plt.plot(roll["date"], roll["beta_fx"])
plt.axvline(pd.to_datetime("2022-04-01"), linestyle="--")
plt.axvline(pd.to_datetime("2023-10-01"), linestyle="--")
plt.title("Rolling FX Pass-Through with Regime Markers")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(OUT_DIR / "05_rolling_beta_with_markers.png", dpi=200)
plt.close()


# --- Event markers (edit labels if you want shorter text)
EVENTS = [
    ("2022-03-01", "Global commodity shock\n(Ukraine war → food/energy prices)"),
    ("2022-04-01", "BCM leadership change\n(new governor appointed)"),
    ("2023-12-14", "FX market modernization\n(interbank FX market launch / platform)"),
    ("2024-08-02", "Government reset\n(new PM appointed)"),
]

events_df = pd.DataFrame(EVENTS, columns=["date", "label"])
events_df["date"] = pd.to_datetime(events_df["date"])

# Safety: make sure roll date is datetime
roll["date"] = pd.to_datetime(roll["date"])

fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

# -------------------------
# Top panel: Rolling beta
# -------------------------
axes[0].plot(roll["date"], roll["beta_fx"])
axes[0].axhline(0, linewidth=1)
axes[0].set_title("Rolling FX Pass-Through (β), 24-month window")
axes[0].set_ylabel("β (effect of FX MoM on inflation MoM)")

# -------------------------
# Bottom panel: Rolling rho
# -------------------------
axes[1].plot(roll["date"], roll["rho_infl"])
axes[1].axhline(0, linewidth=1)
axes[1].set_title("Rolling Inflation Persistence (ρ), 24-month window")
axes[1].set_ylabel("ρ (inflation memory)")
axes[1].set_xlabel("Date")

# -------------------------
# Event markers + annotations
# -------------------------
y_beta_min, y_beta_max = axes[0].get_ylim()
y_rho_min, y_rho_max = axes[1].get_ylim()

for i, row in events_df.iterrows():
    d = row["date"]
    label = row["label"]

    # Vertical line on both panels
    for ax in axes:
        ax.axvline(d, linestyle="--", linewidth=1)

    # Put text on the top panel (beta) so we don’t clutter both
    # Alternate vertical placement a bit so labels don’t overlap too much
    y_text = y_beta_max - (i % 2) * (0.12 * (y_beta_max - y_beta_min)) - 0.05 * (y_beta_max - y_beta_min)

    axes[0].annotate(
        label,
        xy=(d, y_beta_max),
        xytext=(d, y_text),
        textcoords="data",
        ha="left",
        va="top",
        fontsize=9,
        arrowprops=dict(arrowstyle="-", linewidth=0.8),
    )

plt.xticks(rotation=45)
plt.tight_layout()
out_path = OUT_DIR / "06_story_rolling_beta_rho_with_markers.png"
plt.savefig(out_path, dpi=200)
plt.close()

print("Saved combined story figure to:", out_path)

# Optional: also save the event markers for later report text
events_out = OUT_DIR / "event_markers_used.csv"
events_df.to_csv(events_out, index=False)
print("Saved event markers to:", events_out)