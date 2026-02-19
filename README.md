# The Great Decoupling — Mauritania FX-Inflation Analysis

**Author:** Bechar Agatt  
**Period:** February 2020 – December 2025  
**Data:** USD/MRU exchange rates + Mauritanian CPI (headline + COICOP categories)

---

## The Core Finding

Mauritania's inflation system underwent a structural transformation between 2022-2023 and 2024-2025. The economy shifted from an **amplifier regime** (where external shocks multiplied through high FX pass-through and inflation persistence) to an **absorber regime** (where shocks dissipated rapidly).

| Regime | FX Pass-Through (β) | Inflation Persistence (ρ) | Character |
|--------|---------------------|---------------------------|-----------|
| **Amplifier (2022-2023)** | 0.12 | 0.74 | Shocks multiplied |
| **Absorber (2024-2025)** | -0.02 | 0.40 | Shocks dissipated |

**Critical insight:** FX volatility remained essentially unchanged (~0.49→0.50), but transmission collapsed. The *system response* changed, not the shock magnitude.

---

## Quick Start

### Run the Full Pipeline
```bash
cd ~/dev/projects/mauritania-fx-inflation
python3 run_all.py
```

### Build the Report Site
```bash
cd reports/site
mkdocs serve
# Open http://localhost:8000
```

### Deploy
```bash
cd reports/site
mkdocs build
# Deploy site/ folder to your hosting
```

---

## Project Structure

```
mauritania-fx-inflation/
├── data/
│   ├── raw/              # Original BCM FX + IMF CPI data
│   └── processed/        # Cleaned, merged datasets
├── src/                  # Data preparation scripts
│   ├── build_*.py        # Dataset construction
│   ├── regression_*.py   # Statistical models
│   └── validate_pipeline.py
├── analysis/             # Analysis + visualization
│   ├── outputs/          # Generated charts + tables
│   ├── build_production_charts.py
│   ├── plots_story.py
│   ├── structural_overlay.py
│   └── regime_summary.py
├── reports/
│   └── site/             # MkDocs documentation
│       ├── docs/         # Markdown pages
│       ├── mkdocs.yml    # Site configuration
│       └── assets/       # Charts + CSS
├── run_all.py            # Orchestration script
└── PROJECT_NOTES.md      # Detailed research log
```

---

## Key Charts

All charts are generated programmatically and saved to `analysis/outputs/`:

1. **cpi_index.png** — CPI level (2010=100)
2. **infl_mom.png** — Monthly inflation rate
3. **fx_mom.png** — USD/MRU monthly change
4. **volatility.png** — Rolling 6-month volatility comparison
5. **lag_correlation.png** — FX→inflation lag correlation profile
6. **03_rolling_beta_fx_24m.png** — Rolling pass-through coefficient
7. **04_rolling_rho_infl_24m.png** — Rolling persistence coefficient
8. **05_rolling_beta_with_markers.png** — β with regime markers
9. **07_rolling_beta_categories.png** — Category-level pass-through
10. **08_rolling_rho_categories.png** — Category-level persistence
11. **09_structural_overlay.png** — β and ρ combined regime view

---

## Site Structure (Consolidated)

| Page | Content |
|------|---------|
| **Home (index)** | Hero framing, core thesis |
| **The Great Decoupling** | Full thesis + regime table + structural overlay |
| **Transmission** | FX pass-through analysis (β) |
| **Memory** | Inflation persistence analysis (ρ) |
| **Structure** | COICOP category breakdown |
| **Methodology** | Data sources, transformations, models |
| **Data** | Source documentation |
| **Context** | Political/regime timeline (2020-2025) |
| **Appendix** | Regression tables, robustness, conclusion |

---

## Reproducing the Analysis

### Requirements
```bash
pip install pandas numpy matplotlib statsmodels
```

### Step-by-Step
1. **Data preparation** (if raw data changes):
   ```bash
   python3 src/build_fx_monthly_usd.py
   python3 src/build_cpi_baseline.py
   python3 src/build_inflation_from_cpi.py
   python3 src/build_cpi_categories.py
   python3 src/build_merged_dataset.py
   ```

2. **Analysis**:
   ```bash
   python3 src/lag_profile.py
   python3 src/regression_baselines.py
   python3 analysis/build_production_charts.py
   python3 analysis/plots_story.py
   python3 analysis/structural_overlay.py
   python3 analysis/regime_summary.py
   ```

3. **Or simply**: `python3 run_all.py`

---

## Data Sources

- **FX:** Central Bank of Mauritania (BCM), daily USD/MRU, 2020-02-01 to 2025-12-19
- **CPI:** IMF International Financial Statistics, monthly, 2020-02 to 2025-12
  - Headline: All Items (2010=100)
  - Categories: COICOP 1999 classification

---

## Methodology Summary

### Pass-Through (β)
Rolling 24-month regression:  
`Inflation(t) = α + β·FX_change(t) + ε`

### Persistence (ρ)
Rolling 24-month AR(1):  
`Inflation(t) = α + ρ·Inflation(t-1) + ε`

### Regime Definition
- **Amplifier:** 2022-2023 (24 months, commodity shock period)
- **Absorber:** 2024-2025 (24 months, post-reform period)

### Robustness
- Alternative window sizes (18, 30 months) confirm patterns
- YoY vs MoM inflation definitions yield consistent results
- Outlier treatment doesn't change conclusions

---

## What This Project Shows

**Technical:** A reproducible, transparent analysis of inflation microstructure in a small open economy.

**Substantive:** Evidence that Mauritania's inflation mechanism structurally changed, becoming less fragile to external shocks.

**Political Economy:** The stabilization is real and measurable. Whether driven by BCM reforms, global conditions, or administrative changes, the outcome is a less shock-sensitive system. The gas export era will test whether this resilience persists.

---

## Citation

If using this analysis:

> Agatt, Bechar. "The Great Decoupling: Mauritania's Inflation Mechanism Shift, 2020-2025." 2025.  
> [URL when published]

---

## License

Data: Public sources (BCM, IMF)  
Analysis: Original work
