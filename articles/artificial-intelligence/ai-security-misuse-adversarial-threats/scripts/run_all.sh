#!/usr/bin/env bash
set -euo pipefail

ARTICLE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "Running Python AI security risk scoring workflow..."
python3 "$ARTICLE_DIR/python/ai_security_risk_scoring.py"

echo "Running R misuse monitoring workflow..."
if command -v Rscript >/dev/null 2>&1; then
  Rscript "$ARTICLE_DIR/r/misuse_monitoring_summary.R"
else
  echo "Rscript not found; skipping R workflow."
fi

echo "Running Julia control sensitivity workflow..."
if command -v julia >/dev/null 2>&1; then
  julia "$ARTICLE_DIR/julia/control_sensitivity.jl"
else
  echo "Julia not found; skipping Julia workflow."
fi

echo "Done."
