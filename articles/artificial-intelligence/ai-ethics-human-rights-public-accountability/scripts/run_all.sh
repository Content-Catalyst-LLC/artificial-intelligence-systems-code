#!/usr/bin/env bash
set -euo pipefail

ARTICLE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "Running Python rights-impact scoring workflow..."
python3 "$ARTICLE_DIR/python/rights_impact_scoring.py"

echo "Running R disparity and remedy monitoring workflow..."
if command -v Rscript >/dev/null 2>&1; then
  Rscript "$ARTICLE_DIR/r/disparity_remedy_monitoring.R"
else
  echo "Rscript not found; skipping R workflow."
fi

echo "Running Julia governance-control sensitivity workflow..."
if command -v julia >/dev/null 2>&1; then
  julia "$ARTICLE_DIR/julia/governance_control_sensitivity.jl"
else
  echo "Julia not found; skipping Julia workflow."
fi

echo "Done."
