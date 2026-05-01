#!/usr/bin/env bash
set -euo pipefail

ARTICLE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "Running Python risk-register documentation scoring workflow..."
python3 "$ARTICLE_DIR/python/risk_register_documentation_scoring.py"

echo "Running R audit evidence gap workflow..."
if command -v Rscript >/dev/null 2>&1; then
  Rscript "$ARTICLE_DIR/r/audit_evidence_gap_analysis.R"
else
  echo "Rscript not found; skipping R workflow."
fi

echo "Running Julia documentation sensitivity workflow..."
if command -v julia >/dev/null 2>&1; then
  julia "$ARTICLE_DIR/julia/documentation_sensitivity.jl"
else
  echo "Julia not found; skipping Julia workflow."
fi

echo "Done."
