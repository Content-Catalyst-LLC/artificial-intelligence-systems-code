#!/usr/bin/env bash
set -euo pipefail

ARTICLE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "Running Python rights-impact scoring workflow..."
python3 "$ARTICLE_DIR/python/rights_impact_scoring.py"

echo
echo "Running R disparity and remedy monitoring workflow..."
if command -v Rscript >/dev/null 2>&1; then
  Rscript "$ARTICLE_DIR/r/disparity_remedy_monitoring.R"
else
  echo "Rscript not found; skipping R workflow."
fi

echo
echo "Running Julia governance-control sensitivity workflow..."
if command -v julia >/dev/null 2>&1; then
  julia "$ARTICLE_DIR/julia/governance_control_sensitivity.jl"
else
  echo "Julia not found; skipping Julia workflow."
fi

echo
echo "Checking Rust residual rights-risk checker..."
if command -v cargo >/dev/null 2>&1; then
  (cd "$ARTICLE_DIR/rust" && cargo run)
else
  echo "Cargo not found; skipping Rust workflow."
fi

echo
echo "Checking Go public-accountability service build..."
if command -v go >/dev/null 2>&1; then
  (cd "$ARTICLE_DIR/go" && go test ./...)
else
  echo "Go not found; skipping Go workflow."
fi

echo
echo "Checking C++ rights-risk scorer..."
if command -v g++ >/dev/null 2>&1; then
  g++ -std=c++17 "$ARTICLE_DIR/cpp/rights_risk_scorer.cpp" -o "$ARTICLE_DIR/outputs/rights_risk_scorer"
  "$ARTICLE_DIR/outputs/rights_risk_scorer"
else
  echo "g++ not found; skipping C++ workflow."
fi

echo
echo "Checking TypeScript validator..."
if command -v npm >/dev/null 2>&1 && [ -d "$ARTICLE_DIR/typescript/node_modules" ]; then
  (cd "$ARTICLE_DIR/typescript" && npm start)
else
  echo "npm or node_modules not found; skipping TypeScript workflow. Run npm install in the typescript folder first."
fi

echo
echo "Done."
