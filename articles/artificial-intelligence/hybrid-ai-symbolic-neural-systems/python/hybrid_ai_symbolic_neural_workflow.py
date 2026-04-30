"""
Hybrid AI Mini-Workflow: Neural Scores + Symbolic Rules

This script demonstrates:
- synthetic neural model scores
- symbolic facts
- rule-based constraint checks
- hybrid final decisions
- audit traces

It is educational and does not use private data.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


OUTPUT_DIR = Path("../outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

RANDOM_SEED = 42


def build_records(n: int = 500) -> pd.DataFrame:
    """Create synthetic records with neural scores and symbolic attributes."""
    rng = np.random.default_rng(RANDOM_SEED)

    return pd.DataFrame(
        {
            "entity_id": [f"E-{i:04d}" for i in range(1, n + 1)],
            "neural_risk_score": rng.beta(2.2, 4.0, size=n),
            "condition_score": rng.uniform(0.10, 0.98, size=n),
            "criticality": rng.choice(
                ["low", "medium", "high"],
                size=n,
                p=[0.45, 0.35, 0.20],
            ),
            "sensitive_workflow": rng.choice([0, 1], size=n, p=[0.80, 0.20]),
        }
    )


def symbolic_review_required(row: pd.Series) -> tuple[int, list[str]]:
    """Apply symbolic governance and domain rules."""
    triggered_rules: list[str] = []

    if row["criticality"] == "high" and row["condition_score"] <= 0.35:
        triggered_rules.append("critical_asset_low_condition_requires_review")

    if row["sensitive_workflow"] == 1 and row["neural_risk_score"] >= 0.45:
        triggered_rules.append("sensitive_workflow_requires_human_review")

    if row["criticality"] == "medium" and row["condition_score"] <= 0.25:
        triggered_rules.append("medium_criticality_severe_condition_requires_review")

    return int(len(triggered_rules) > 0), triggered_rules


def apply_hybrid_decision(records: pd.DataFrame) -> pd.DataFrame:
    """Combine neural recommendation with symbolic rule checks."""
    frame = records.copy()

    frame["neural_recommendation"] = (
        frame["neural_risk_score"] >= 0.55
    ).astype(int)

    symbolic_results = frame.apply(symbolic_review_required, axis=1)

    frame["symbolic_review_required"] = [
        result[0] for result in symbolic_results
    ]

    frame["triggered_rules"] = [
        "; ".join(result[1]) if result[1] else "none"
        for result in symbolic_results
    ]

    frame["hybrid_decision"] = (
        (frame["neural_recommendation"] == 1)
        | (frame["symbolic_review_required"] == 1)
    ).astype(int)

    frame["decision_source"] = np.select(
        [
            (frame["neural_recommendation"] == 1)
            & (frame["symbolic_review_required"] == 1),
            (frame["neural_recommendation"] == 1)
            & (frame["symbolic_review_required"] == 0),
            (frame["neural_recommendation"] == 0)
            & (frame["symbolic_review_required"] == 1),
        ],
        [
            "neural_and_symbolic",
            "neural_only",
            "symbolic_only",
        ],
        default="no_review",
    )

    return frame


def summarize_hybrid_behavior(frame: pd.DataFrame) -> pd.DataFrame:
    """Summarize hybrid decision behavior by source."""
    return (
        frame
        .groupby("decision_source")
        .agg(
            n=("entity_id", "count"),
            mean_neural_score=("neural_risk_score", "mean"),
            mean_condition=("condition_score", "mean"),
            hybrid_review_rate=("hybrid_decision", "mean"),
        )
        .reset_index()
    )


def main() -> None:
    records = build_records()
    hybrid = apply_hybrid_decision(records)
    summary = summarize_hybrid_behavior(hybrid)

    hybrid.to_csv(OUTPUT_DIR / "hybrid_ai_audit_trace.csv", index=False)
    summary.to_csv(OUTPUT_DIR / "hybrid_ai_decision_summary.csv", index=False)

    print(summary)
    print(hybrid.head())


if __name__ == "__main__":
    main()
