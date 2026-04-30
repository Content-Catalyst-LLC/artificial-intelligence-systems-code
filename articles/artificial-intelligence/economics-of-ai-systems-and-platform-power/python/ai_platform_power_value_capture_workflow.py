"""
Economics of AI Systems and Platform Power Mini-Workflow

This script demonstrates:
- AI ecosystem actors
- concentration measurement
- platform-power scoring
- dependency diagnostics
- value-capture shares

It is educational and uses synthetic data.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


OUTPUT_DIR = Path("../outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def build_ai_ecosystem() -> pd.DataFrame:
    """Create a synthetic AI ecosystem value-chain table."""
    return pd.DataFrame(
        [
            {
                "actor": "cloud_compute_provider",
                "layer": "infrastructure",
                "market_share": 0.36,
                "data_control": 0.45,
                "distribution_control": 0.55,
                "switching_costs": 0.80,
                "gatekeeping_power": 0.85,
                "captured_surplus": 35.0,
            },
            {
                "actor": "foundation_model_provider",
                "layer": "model",
                "market_share": 0.28,
                "data_control": 0.70,
                "distribution_control": 0.60,
                "switching_costs": 0.65,
                "gatekeeping_power": 0.72,
                "captured_surplus": 25.0,
            },
            {
                "actor": "enterprise_application_firm",
                "layer": "application",
                "market_share": 0.18,
                "data_control": 0.55,
                "distribution_control": 0.45,
                "switching_costs": 0.40,
                "gatekeeping_power": 0.35,
                "captured_surplus": 20.0,
            },
            {
                "actor": "downstream_users",
                "layer": "user",
                "market_share": 0.18,
                "data_control": 0.20,
                "distribution_control": 0.10,
                "switching_costs": 0.25,
                "gatekeeping_power": 0.10,
                "captured_surplus": 20.0,
            },
        ]
    )


def score_platform_power(actors: pd.DataFrame) -> pd.DataFrame:
    """Score platform power, dependency risk, and value capture."""
    scored = actors.copy()

    scored["platform_power_score"] = (
        0.25 * scored["market_share"]
        + 0.20 * scored["data_control"]
        + 0.20 * scored["distribution_control"]
        + 0.20 * scored["switching_costs"]
        + 0.15 * scored["gatekeeping_power"]
    )

    total_surplus = scored["captured_surplus"].sum()
    scored["value_capture_share"] = scored["captured_surplus"] / total_surplus

    scored["dependency_risk"] = (
        0.40 * scored["switching_costs"]
        + 0.35 * scored["gatekeeping_power"]
        + 0.25 * scored["distribution_control"]
    )

    return scored.sort_values("platform_power_score", ascending=False)


def summarize_by_layer(scored: pd.DataFrame) -> pd.DataFrame:
    """Summarize platform-power diagnostics by value-chain layer."""
    return (
        scored
        .groupby("layer")
        .agg(
            actors=("actor", "count"),
            mean_market_share=("market_share", "mean"),
            mean_platform_power=("platform_power_score", "mean"),
            mean_value_capture=("value_capture_share", "mean"),
            mean_dependency_risk=("dependency_risk", "mean"),
        )
        .reset_index()
    )


def main() -> None:
    actors = build_ai_ecosystem()
    scored = score_platform_power(actors)
    summary = summarize_by_layer(scored)

    concentration_score = float((scored["market_share"] ** 2).sum())

    scored.to_csv(OUTPUT_DIR / "ai_platform_power_scores.csv", index=False)
    summary.to_csv(OUTPUT_DIR / "ai_platform_power_summary.csv", index=False)

    print("Concentration score:", round(concentration_score, 3))
    print(scored)
    print(summary)


if __name__ == "__main__":
    main()
