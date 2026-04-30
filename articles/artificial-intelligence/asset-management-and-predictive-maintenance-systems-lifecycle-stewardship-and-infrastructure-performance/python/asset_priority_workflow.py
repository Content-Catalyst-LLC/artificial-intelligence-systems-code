"""
Asset Management and Predictive Maintenance Mini-Workflow

This script demonstrates:
- synthetic infrastructure asset register
- condition and age-based failure probability
- criticality-weighted risk scoring
- maintenance priority ranking
- intervention shortlist creation

It is educational and does not use operational infrastructure data.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


OUTPUT_DIR = Path("../outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

RANDOM_SEED = 42


def build_asset_register(n_assets: int = 250) -> pd.DataFrame:
    """Create a synthetic infrastructure asset register."""
    rng = np.random.default_rng(RANDOM_SEED)

    return pd.DataFrame(
        {
            "asset_id": [f"A-{i:04d}" for i in range(1, n_assets + 1)],
            "asset_class": rng.choice(
                [
                    "pump",
                    "valve",
                    "bridge_component",
                    "road_segment",
                    "substation_asset",
                ],
                size=n_assets,
                p=[0.20, 0.20, 0.20, 0.25, 0.15],
            ),
            "age_years": rng.integers(1, 60, size=n_assets),
            "condition_score": rng.uniform(0.15, 0.98, size=n_assets),
            "service_consequence": rng.integers(1, 6, size=n_assets),
            "environmental_exposure": rng.uniform(0.0, 1.0, size=n_assets),
        }
    )


def score_assets(assets: pd.DataFrame) -> pd.DataFrame:
    """Estimate failure probability, risk score, and priority score."""
    scored = assets.copy()

    linear_risk = (
        -3.0
        + 0.045 * scored["age_years"]
        + 2.5 * (1 - scored["condition_score"])
        + 0.9 * scored["environmental_exposure"]
    )

    scored["failure_probability"] = 1 / (1 + np.exp(-linear_risk))

    scored["risk_score"] = (
        scored["failure_probability"] * scored["service_consequence"]
    )

    scored["priority_score"] = (
        0.40 * (1 - scored["condition_score"])
        + 0.30 * scored["failure_probability"]
        + 0.20 * (scored["service_consequence"] / 5)
        + 0.10 * scored["environmental_exposure"]
    )

    scored["recommended_strategy"] = pd.cut(
        scored["priority_score"],
        bins=[-0.01, 0.35, 0.55, 0.75, 1.01],
        labels=[
            "monitor",
            "condition_based_maintenance",
            "planned_intervention",
            "urgent_review",
        ],
    )

    return scored


def summarize_portfolio(scored: pd.DataFrame) -> pd.DataFrame:
    """Summarize asset condition and risk by class and strategy."""
    return (
        scored
        .groupby(["asset_class", "recommended_strategy"], observed=True)
        .agg(
            asset_count=("asset_id", "count"),
            mean_condition=("condition_score", "mean"),
            mean_failure_probability=("failure_probability", "mean"),
            mean_risk_score=("risk_score", "mean"),
            mean_priority_score=("priority_score", "mean"),
        )
        .reset_index()
    )


def main() -> None:
    assets = build_asset_register()
    scored = score_assets(assets)
    summary = summarize_portfolio(scored)

    shortlist = (
        scored
        .sort_values("priority_score", ascending=False)
        .head(20)
        .reset_index(drop=True)
    )

    scored.to_csv(OUTPUT_DIR / "synthetic_asset_register_scored.csv", index=False)
    shortlist.to_csv(OUTPUT_DIR / "maintenance_priority_shortlist.csv", index=False)
    summary.to_csv(OUTPUT_DIR / "asset_portfolio_summary.csv", index=False)

    print("Top maintenance-priority assets:")
    print(shortlist)

    print("\nPortfolio summary:")
    print(summary)


if __name__ == "__main__":
    main()
