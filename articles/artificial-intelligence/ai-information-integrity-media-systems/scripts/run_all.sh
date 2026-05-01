#!/usr/bin/env bash
set -euo pipefail

ARTICLE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "Running Python information-integrity risk scoring workflow..."
python3 "$ARTICLE_DIR/python/information_integrity_risk_scoring.py"

echo "Running R source diversity and media monitoring workflow..."
if command -v Rscript >/dev/null 2>&1; then
  Rscript "$ARTICLE_DIR/r/source_diversity_media_monitoring.R"
else
  echo "Rscript not found; skipping R workflow."
fi

echo "Running Julia source diversity sensitivity workflow..."
if command -v julia >/dev/null 2>&1; then
  julia "$ARTICLE_DIR/julia/source_diversity_sensitivity.jl"
else
  echo "Julia not found; skipping Julia workflow."
fi

echo "Done."
