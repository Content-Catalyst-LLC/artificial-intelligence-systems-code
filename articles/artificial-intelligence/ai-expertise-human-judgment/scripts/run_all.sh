#!/usr/bin/env bash
set -euo pipefail

ARTICLE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "Running Python human-AI decision support workflow..."
python3 "$ARTICLE_DIR/python/human_ai_decision_support.py"

echo
echo "Running R expert disagreement monitoring workflow..."
if command -v Rscript >/dev/null 2>&1; then
  Rscript "$ARTICLE_DIR/r/expert_disagreement_monitoring.R"
else
  echo "Rscript not found; skipping R workflow."
fi

echo
echo "Running Julia reliance sensitivity workflow..."
if command -v julia >/dev/null 2>&1; then
  julia "$ARTICLE_DIR/julia/reliance_sensitivity.jl"
else
  echo "Julia not found; skipping Julia workflow."
fi

echo
echo "Checking Rust reliance checker..."
if command -v cargo >/dev/null 2>&1; then
  (cd "$ARTICLE_DIR/rust" && cargo run)
else
  echo "Cargo not found; skipping Rust workflow."
fi

echo
echo "Checking Go monitoring service build..."
if command -v go >/dev/null 2>&1; then
  (cd "$ARTICLE_DIR/go" && go test ./...)
else
  echo "Go not found; skipping Go workflow."
fi

echo
echo "Checking C++ reliance scorer..."
if command -v g++ >/dev/null 2>&1; then
  g++ -std=c++17 "$ARTICLE_DIR/cpp/reliance_scorer.cpp" -o "$ARTICLE_DIR/outputs/reliance_scorer"
  "$ARTICLE_DIR/outputs/reliance_scorer"
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
