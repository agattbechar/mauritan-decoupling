# Fixes Applied — Post-ChatGPT Cleanup

## Summary

ChatGPT lost track of the project structure, creating phantom references, duplicate files, and circular navigation. This document records what was fixed.

---

## Critical Issues Fixed

### 1. Missing Chart: `lag_correlation.png`
**Problem:** `results.md` referenced `lag_correlation.png` but it didn't exist. Only `lag_profile.py` (console output) existed.

**Fix:** 
- Created `src/plot_lag_correlation.py` that generates and saves the chart
- Outputs to both `analysis/outputs/` and `reports/site/docs/assets/charts/`

**Status:** Script created. Run with `python3 src/plot_lag_correlation.py` in your environment (requires pandas).

---

### 2. Duplicate Documentation
**Problem:** Both `methodology.md` and `methods.md` existed with nearly identical content.

**Fix:** 
- Deleted `methods.md`
- Kept `methodology.md` (more comprehensive)

---

### 3. Empty/Stub Files
**Problem:** 
- `appendix.md` was just a header ("# Appendix")
- `fr/` folder contained empty stubs
- French was enabled in nav but content didn't exist

**Fix:**
- **Rewrote `appendix.md`** — Full content:
  - Complete regression tables (baseline, full model, regime comparison)
  - Lag correlation profile with table
  - Volatility analysis
  - Category-level breakdown (Food, Transport, Services)
  - Robustness checks
  - Data quality & limitations
  - **Conclusion with political economy positioning** (technocrat/opposition balance)
- **Removed French from nav** — Deleted i18n plugin from `mkdocs.yml`

---

### 4. Phantom Page References
**Problem:** Multiple pages referenced `results.md` which was a content bucket, not a coherent page.

**Fix:**
- Deleted `results.md`
- Updated `decoupling.md` — Removed "Proceed to Results", replaced with links to Transmission/Memory/Structure/Appendix
- Updated `structure.md` — Changed "next page" reference to point to Appendix
- Updated `transmission.md` — Removed "The next question: Did inflation also lose its memory?" (circular reference)

---

### 5. Navigation Cleanup
**Problem:** Nav had 10 items with confusing names and ordering.

**Fix:** Updated `mkdocs.yml`:
```yaml
nav:
  - Home: index.md
  - The Great Decoupling: decoupling.md
  - Transmission: transmission.md
  - Memory: memory.md
  - Structure: structure.md
  - Methodology: methodology.md
  - Data: data.md
  - Context: setting.md
  - Appendix: appendix.md
```

Changes:
- Removed French (i18n plugin)
- Removed `results.md` from nav
- Renamed "Setting" → "Context" (clearer)
- Cleaned up page titles (removed parentheticals)

---

### 6. Added Orchestration
**Problem:** No way to run the full pipeline. Someone cloning wouldn't know execution order.

**Fix:** Created `run_all.py` — orchestrates:
1. Data validation
2. Lag correlation generation
3. Regression baselines
4. All analysis scripts
5. Chart copying to assets

---

### 7. Added Documentation
**Problem:** No README for newcomers.

**Fix:** Created comprehensive `README.md` with:
- Core finding summary
- Quick start (run pipeline, build site, deploy)
- Project structure explanation
- Chart inventory
- Site structure
- Reproduction instructions
- Data sources
- Methodology summary
- Citation format

---

## New Files Created

1. `src/plot_lag_correlation.py` — Generates missing lag correlation chart
2. `run_all.py` — Pipeline orchestration
3. `README.md` — Project documentation
4. `reports/site/docs/appendix.md` — Complete appendix (was empty)

## Files Deleted

1. `reports/site/docs/methods.md` — Duplicate of methodology.md
2. `reports/site/docs/results.md` — Content bucket, not needed in consolidated structure

## Files Modified

1. `reports/site/mkdocs.yml` — Removed French, simplified nav, removed results.md
2. `reports/site/docs/decoupling.md` — Updated cross-references
3. `reports/site/docs/transmission.md` — Removed circular "next question"
4. `reports/site/docs/structure.md` — Updated to point to appendix

---

## Remaining Work (User Side)

1. **Generate lag_correlation.png:**
   ```bash
   cd ~/dev/projects/mauritania-fx-inflation
   python3 src/plot_lag_correlation.py
   ```

2. **Test site build:**
   ```bash
   cd reports/site
   mkdocs serve
   ```

3. **Optional — Remove unused charts:**
   - `01_infl_vol_6m.png`
   - `02_volatility_side_by_side.png`
   - `06_story_rolling_beta_rho_with_markers.png`
   Or integrate them into pages if desired.

---

## The Appendix Conclusion (Political Positioning)

The new appendix includes a conclusion that navigates your positioning:

- **Acknowledges the achievement:** "The stabilization of Mauritania's inflation mechanism is a genuine achievement... The outcome is real."
- **Frames it as public good:** "Reduced pass-through means households are less vulnerable... These are public goods."
- **Establishes technocrat credibility:** "The goal of this analysis is not to cheerlead or condemn, but to measure."
- **Maintains opposition stance:** "Real opposition is not reflexive negation. It is the capacity to say: 'This worked. Now let's ensure the next phase works too — and more equitably.'"
- **Forward-looking:** Poses questions about gas export era, Dutch disease, distribution

This positions you as the expert who can praise what works while maintaining independence to critique what comes next.

---

## Structural Philosophy

**Before (ChatGPT drift):** 9+ pages with overlap, phantom references, circular navigation

**After (Consolidated):** 8 tight pages:
1. Home — Hook
2. Decoupling — Full thesis
3. Transmission — β mechanics
4. Memory — ρ mechanics
5. Structure — Category breakdown
6. Methodology — How we know
7. Data — What we measured
8. Context — When/why it happened
9. Appendix — Deep dive + conclusion

Every page has a single job. No duplication. No phantom references.
