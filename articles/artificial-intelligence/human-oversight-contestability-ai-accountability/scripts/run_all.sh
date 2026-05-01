#!/usr/bin/env bash
set -euo pipefail

ARTICLE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "Running Python oversight triage workflow..."
python3 "$ARTICLE_DIR/python/oversight_triage.py"

echo "Running R contestability monitoring workflow..."
if command -v Rscript >/dev/null 2>&1; then
  Rscript "$ARTICLE_DIR/r/contestability_monitoring.R"
else
  echo "Rscript not found; skipping R workflow."
fi

echo "Running Julia threshold workflow..."
if command -v julia >/dev/null 2>&1; then
  julia "$ARTICLE_DIR/julia/oversight_thresholds.jl"
else
  echo "Julia not found; skipping Julia workflow."
fi

echo "Done."
