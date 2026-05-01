#!/usr/bin/env bash
set -euo pipefail

ARTICLE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "Running Python task exposure and job redesign workflow..."
python3 "$ARTICLE_DIR/python/task_exposure_job_redesign.py"

echo "Running R job quality monitoring workflow..."
if command -v Rscript >/dev/null 2>&1; then
  Rscript "$ARTICLE_DIR/r/job_quality_monitoring.R"
else
  echo "Rscript not found; skipping R workflow."
fi

echo "Running Julia labor transition sensitivity workflow..."
if command -v julia >/dev/null 2>&1; then
  julia "$ARTICLE_DIR/julia/labor_transition_sensitivity.jl"
else
  echo "Julia not found; skipping Julia workflow."
fi

echo "Done."
