# The Great Decoupling: Mauritania's Inflation Mechanism Shift (2020-2025)

[![Website](https://img.shields.io/badge/Website-Live-blue)](https://becharagatt.github.io/mauritania-decoupling)
[![Language](https://img.shields.io/badge/Language-EN%2FFR-green)](https://becharagatt.github.io/mauritania-decoupling)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

> **A quantitative microstructure analysis of Mauritania's inflation regime transformation**

## Overview

This project presents the first rigorous empirical analysis of Mauritania's inflation dynamics during the critical 2020-2025 period. Using Central Bank of Mauritania (BCM) and IMF data, we demonstrate that Mauritania's inflation system underwent a structural transformation: shifting from an **amplifier regime** (2022-2023) where external shocks multiplied, to an **absorber regime** (2024-2025) where shocks dissipated.

## Key Findings

| Metric | Amplifier Regime (2022-2023) | Absorber Regime (2024-2025) |
|--------|------------------------------|----------------------------|
| **FX Pass-Through (β)** | 0.12 | -0.02 |
| **Inflation Persistence (ρ)** | 0.74 | 0.40 |

**Critical Insight:** FX volatility remained essentially unchanged (0.49→0.50), yet transmission collapsed. The *system response* changed, not the shock magnitude—indicating structural, not circumstantial, improvement.

## What's Inside

### 📊 Analysis
- **Rolling regression framework** (24-month windows) for time-varying β and ρ
- **COICOP category breakdown** (Food, Transport, Services)
- **Regime comparison** with statistical robustness checks
- **Volatility analysis** showing system adaptation

### 🌍 Bilingual Presentation
- **English:** Professional research format for international audiences
- **Français:** Full translation for Mauritanian policymakers and civil society

### 🔬 Methodology
- Data: BCM daily FX rates + IMF CPI series (71 months, Feb 2020–Dec 2025)
- Models: OLS with HAC standard errors, AR(1) persistence
- Code: Fully reproducible Python pipeline

### 📈 Outputs
- Interactive website with all visualizations
- Full regression tables and technical appendix
- Downloadable datasets and replication code
- Policy implications for Mauritania's gas export era

## Repository Structure

```
mauritania-fx-inflation/
├── data/
│   ├── raw/              # Original BCM & IMF data
│   └── processed/        # Cleaned, merged datasets
├── src/                  # Data preparation & analysis scripts
├── analysis/             # Charts, tables, outputs
├── reports/site/         # Quarto website source (EN/FR)
└── README.md
```

## Why This Matters

Most inflation analysis asks: "Was inflation high or low?"

We ask: **"Did the inflation mechanism itself change?"**

This distinction is crucial for policy design in Mauritania's transition to gas-exporting status. If inflation has become less sensitive to external shocks, the economy is structurally more resilient—but the gas windfall will test whether this resilience persists.

## Citation

If using this analysis:

```bibtex
@report{agatt2025decoupling,
  title={The Great Decoupling: Mauritania's Inflation Mechanism Shift, 2020-2025},
  author={Agatt, Bechar},
  year={2025},
  institution={Independent Research},
  url={https://becharagatt.github.io/mauritania-decoupling}
}
```

## Data Sources

- **FX Data:** Central Bank of Mauritania (BCM), daily USD/MRU, 2020-2025
- **CPI Data:** IMF International Financial Statistics, monthly, 2020-2025
- **Coverage:** 71 months (Feb 2020 – Dec 2025)

## License

Data: Public sources (BCM, IMF)  
Analysis & Code: [MIT License](LICENSE)

## Contact

For questions, collaboration, or media inquiries: [Your contact info]

---

*"We do not speculate. We measure."*
