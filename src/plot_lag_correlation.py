import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Load data
df = pd.read_csv("data/processed/merged_fx_cpi_2020_2025.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

def lag_profile(y_col, x_col, max_lag=12):
    """Compute correlation between y(t) and x(t-lag) for lags 0 to max_lag"""
    y = df[y_col]
    x = df[x_col]
    out = []
    for lag in range(max_lag + 1):
        corr = y.corr(x.shift(lag))
        out.append((lag, corr))
    return out

# Generate lag correlations
print("Lag profile: corr(infl_mom_pct(t), fx_mom_pct(t-lag))")
lags_mom = lag_profile("infl_mom_pct", "fx_mom_pct", 12)
for lag, c in lags_mom:
    print(lag, round(c, 4))

print("\nLag profile: corr(infl_yoy_pct(t), fx_mom_pct(t-lag))")
lags_yoy = lag_profile("infl_yoy_pct", "fx_mom_pct", 12)
for lag, c in lags_yoy:
    print(lag, round(c, 4))

# Create the plot
fig, ax = plt.subplots(figsize=(10, 6))

lags = [x[0] for x in lags_mom]
corrs = [x[1] for x in lags_mom]

ax.bar(lags, corrs, color=['#e74c3c' if c < 0 else '#3498db' for c in corrs], alpha=0.7, edgecolor='black')
ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
ax.set_xlabel('Lag (months)', fontsize=12)
ax.set_ylabel('Correlation', fontsize=12)
ax.set_title('FX → Inflation Transmission: Lag Correlation Profile\n(corr(inflation(t), FX_change(t-lag)))', fontsize=14)
ax.set_xticks(lags)
ax.grid(axis='y', alpha=0.3)

# Add annotation for strongest correlation
max_corr = max(corrs, key=lambda x: abs(x))
max_lag = corrs.index(max_corr)
ax.annotate(f'Peak: {max_corr:.3f} at lag {max_lag}', 
            xy=(max_lag, max_corr), xytext=(max_lag + 2, max_corr + 0.05),
            arrowprops=dict(arrowstyle='->', color='gray'),
            fontsize=10, color='gray')

plt.tight_layout()

# Save to both locations
out_path = Path("analysis/outputs/lag_correlation.png")
chart_path = Path("reports/site/docs/assets/charts/lag_correlation.png")

plt.savefig(out_path, dpi=200, bbox_inches='tight')
plt.savefig(chart_path, dpi=200, bbox_inches='tight')
plt.close()

print(f"\nSaved: {out_path}")
print(f"Saved: {chart_path}")
