#!/usr/bin/env python3
"""
Run the full Mauritania FX-Inflation analysis pipeline.

Usage:
    python3 run_all.py

This script:
1. Validates the data pipeline
2. Runs all analysis scripts
3. Generates charts
4. Copies outputs to report assets
"""

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
SRC_DIR = PROJECT_ROOT / "src"
ANALYSIS_DIR = PROJECT_ROOT / "analysis"

SCRIPTS = [
    # Data validation
    ("Validating data pipeline", SRC_DIR / "validate_pipeline.py"),
    
    # Lag correlation (the missing chart)
    ("Generating lag correlation profile", SRC_DIR / "plot_lag_correlation.py"),
    
    # Core metrics
    ("Computing baseline regressions", SRC_DIR / "regression_baselines.py"),
    ("Analyzing lag correlations", SRC_DIR / "lag_correlation_analysis.py"),
    ("Computing lag profile", SRC_DIR / "lag_profile.py"),
    
    # Analysis outputs
    ("Building production charts", ANALYSIS_DIR / "build_production_charts.py"),
    ("Building story plots", ANALYSIS_DIR / "plots_story.py"),
    ("Generating structural overlay", ANALYSIS_DIR / "structural_overlay.py"),
    ("Computing regime summary", ANALYSIS_DIR / "regime_summary.py"),
]

def run_script(description, script_path):
    """Run a Python script and handle errors."""
    print(f"\n{'='*60}")
    print(f"{description}")
    print(f"Running: {script_path}")
    print('='*60)
    
    if not script_path.exists():
        print(f"WARNING: {script_path} not found, skipping...")
        return True
    
    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=PROJECT_ROOT,
        capture_output=False
    )
    
    if result.returncode != 0:
        print(f"ERROR: {script_path} failed with code {result.returncode}")
        return False
    return True

def copy_charts():
    """Copy generated charts to report assets."""
    print(f"\n{'='*60}")
    print("Copying charts to report assets")
    print('='*60)
    
    outputs_dir = PROJECT_ROOT / "analysis" / "outputs"
    assets_dir = PROJECT_ROOT / "reports" / "site" / "docs" / "assets" / "charts"
    
    assets_dir.mkdir(parents=True, exist_ok=True)
    
    charts = [
        "cpi_index.png",
        "infl_mom.png",
        "fx_mom.png",
        "volatility.png",
        "lag_correlation.png",
        "03_rolling_beta_fx_24m.png",
        "04_rolling_rho_infl_24m.png",
        "05_rolling_beta_with_markers.png",
        "07_rolling_beta_categories.png",
        "08_rolling_rho_categories.png",
        "09_structural_overlay.png",
    ]
    
    for chart in charts:
        src = outputs_dir / chart
        dst = assets_dir / chart
        if src.exists():
            import shutil
            shutil.copy2(src, dst)
            print(f"  Copied: {chart}")
        else:
            print(f"  Missing: {chart}")

def main():
    print("="*60)
    print("Mauritania FX-Inflation Analysis Pipeline")
    print("="*60)
    print(f"Project root: {PROJECT_ROOT}")
    
    success = True
    for desc, script in SCRIPTS:
        if not run_script(desc, script):
            success = False
    
    copy_charts()
    
    print(f"\n{'='*60}")
    if success:
        print("Pipeline completed successfully!")
        print("\nNext steps:")
        print("  1. cd reports/site")
        print("  2. mkdocs serve")
        print("  3. Open http://localhost:8000")
    else:
        print("Pipeline completed with errors.")
        sys.exit(1)
    print('='*60)

if __name__ == "__main__":
    main()
