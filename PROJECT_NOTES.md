Mauritania FX → Inflation (CPI) Microstructure Project

Time window: 2020-02 to 2025-12
Frame: Quant microstructure lens (clear, disciplined, not abstract)
Goal: A publishable, reproducible report that changes how we think about inflation in Mauritania.

1) Core Hypothesis

Hypothesis:
In Mauritania (2020–2025), exchange-rate depreciation does influence inflation —
but inflation inertia (persistence) plays a structurally larger role than FX alone.

We test this through a microstructure mindset:

Who transmits shocks?

How fast do shocks propagate?

Does transmission weaken across regimes?

Is inflation reactive — or self-reinforcing?

We do not assume FX drives inflation.

We test it.

2) Why 2020-02 to 2025-12?
2.1 Hard Data Alignment

FX (USD/MRU) daily data begins 2020-02-01.

CPI monthly series begins 2020-M02.

Starting earlier introduces stitching errors.

2.2 Clean Regime Window

This window captures:

Post-inauguration stabilization

COVID shock

2022 global commodity shock

2024 re-election & executive reshuffle

FX market modernization era

2.3 Macro Shock Awareness

13 March 2020: first COVID case in Mauritania.

2022: global food and energy shock.

2024–2025: new executive configuration and gas transition period.

This is not arbitrary.
It is a structurally rich window.

3) Data Pipeline (Reproducible)
3.1 FX (USD/MRU)

Source: Central Bank of Mauritania (BCM)

Processing:

Daily → monthly average

Monthly % change computed

Output:

date

fx_usd_avg

fx_mom_pct

3.2 CPI (Headline)

Selection rule:

Monthly frequency

COICOP: Total / All items

Index level (we compute inflation ourselves)

Output:

date

cpi_index

infl_mom_pct

infl_yoy_pct

3.3 Merge

Monthly merge of CPI and FX.

Result:
69 observations (2020-02 → 2025-12)

4) Baseline Microstructure Tests

We run the minimum necessary tests:

Time-series visualization

Lag correlation profile

OLS with persistence

Rolling pass-through

Rolling inflation persistence

Volatility comparison

Everything interpretable.
Nothing decorative.

5) Static Relationship: FX → Inflation

Model:

inflation(t) = α + β·FX_change(t) + ρ·inflation(t-1) + ε

Results (HAC robust):

β ≈ 0.094

ρ ≈ 0.480

R² ≈ 0.33

Interpretation

A 1% depreciation in USD/MRU is associated with roughly 0.09% monthly inflation.

But last month’s inflation explains almost half of this month’s inflation.

Translation:

FX matters.

Inflation memory matters more.

6) Inflation Persistence (The Memory Layer)

AR(1) estimate:

ρ = 0.5727

What does this mean?

If ρ = 0 → inflation has no memory.

If ρ = 1 → inflation never forgets.

Mauritania ≈ 0.57.

Half-life of an inflation shock ≈ 1.24 months.

After 3 months:
ρ³ ≈ 0.188
→ ~19% of the shock still remains.

Inflation fades — but slowly enough to matter.

This is structural inertia.

7) Lag Profile (Does FX Lead?)

We computed:

Corr(inflation(t), FX_change(t-k)), k = 0..12

Findings:

Strongest at lag 0

Rapid decay afterward

No delayed 6–12 month build-up

Interpretation:

Pass-through, when it occurs, is immediate.

There is no slow-burn FX transmission mechanism in this period.

8) Rolling Pass-Through (β over Time)

24-month rolling regression.

2022–early 2023:

β ≈ 0.30–0.42

2024–2025:

β ≈ 0.08

Late 2025:

Near zero / slightly negative

Key insight:

Transmission weakened significantly after 2023.

Important:

FX volatility did NOT collapse.

Transmission weakened.

This suggests structural dampening, not calm markets.

9) Rolling Inflation Persistence (ρ over Time)

Peak persistence:
2023–early 2024 (ρ > 0.55)

Sharp drop:
Mid-2024

2025:
Stabilized near 0.40

Interpretation:

During global shock period:
Inflation became stickier.

Post-shock:
Memory declines.

Inflation regime shifted.

10) Volatility Analysis

FX volatility:

Pre-2023: 0.4903

2024+: 0.5036

Inflation volatility:

Pre-2023: 0.3088

2024+: 0.3222

Volatility barely changed.

But pass-through changed dramatically.

This is the key microstructure observation.

The shock transmission channel weakened without volatility collapse.

11) Regime Markers (Annotated in Charts)

We annotate:

2020-03: COVID shock

2020-08: PM Bilal appointment

2022: global commodity spike

2024-06: presidential election

2024-08: PM Djay appointment

2024+: post-election executive configuration

We do not assume causality.

We observe structural shifts around these windows.

12) What This Project Actually Shows

Mauritania’s inflation (2020–2025) is:

Not purely FX-driven.

Not purely domestic either.

It is:

Shock-amplified by inertia.

FX shocks hit quickly.

Inflation memory carries them forward.

After 2023, the transmission mechanism weakens significantly.

This suggests:

Institutional or structural adaptation in pricing behavior.

13) Microstructure Interpretation (Non-Technical)

In microstructure terms:

FX volatility remained present.

But the CPI book stopped reacting aggressively.

That implies:

Pricing behavior changed

Expectations stabilized

Or import absorption improved

Or administered pricing muted pass-through

The market structure evolved.

Not just the variables.

14) What Makes This Insight Different

Most discussions ask:

"Does FX cause inflation?"

We ask:

"How does shock transmission evolve across regimes?"

The key finding:

Transmission is time-varying.
Persistence dominates.
Volatility alone explains little.

That reframes inflation analysis.

15) Phase 2 (Before Report Freeze)

We will add:

CPI category-level pass-through

Food vs non-food comparison

Contribution decomposition

Subsample regressions (2020–2023 vs 2024–2025)

Regime comparison tests

Only after that do we finalize the publication layer.

16) Project Structure

mauritania-fx-inflation/
data/
raw/
processed/
analysis/
src/
reports/
PROJECT_NOTES.md

All outputs reproducible.
All transformations scripted.
No manual Excel manipulation.

Current Working Conclusion (Subject to Final Layer)

Mauritania’s inflation is structurally persistent.

FX shocks matter — but only during high global stress regimes.

After 2023, the transmission mechanism weakens significantly.

The story is not "FX causes inflation."

The story is:

Shock + Inertia = Inflation.

And inertia matters more than people think.