"""
Defensive AI security risk scoring workflow.

This script creates a synthetic AI-system asset inventory and estimates
inherent risk, control strength, residual risk, and control-priority bands.

It does not implement attack techniques. It is intended for governance,
security planning, documentation, monitoring, and audit-readiness work.
"""

from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd


def create_asset_inventory() -> pd.DataFrame:
    """Create a synthetic AI security asset inventory."""
    return pd.DataFrame(
        {
            "asset": [
                "training_data",
                "fine_tuning_pipeline",
                "retrieval_index",
                "system_prompt",
                "model_endpoint",
                "tool_api_gateway",
                "audit_logs",
                "monitoring_pipeline",
                "agent_orchestration_layer",
                "model_artifact_store",
            ],
            "asset_type": [
                "data",
                "pipeline",
                "retrieval",
                "prompt",
                "model_service",
                "tooling",
                "logging",
                "monitoring",
                "agent_runtime",
                "model_supply_chain",
            ],
            "exposure": [0.50, 0.45, 0.75, 0.65, 0.80, 0.90, 0.40, 0.55, 0.85, 0.70],
            "impact": [0.85, 0.80, 0.75, 0.70, 0.90, 0.95, 0.65, 0.70, 0.92, 0.88],
            "threat_likelihood": [0.40, 0.35, 0.60, 0.55, 0.65, 0.70, 0.30, 0.45, 0.62, 0.50],
            "control_strength": [0.60, 0.55, 0.50, 0.45, 0.65, 0.55, 0.70, 0.60, 0.52, 0.58],
            "human_review_required": [0, 1, 0, 1, 0, 1, 0, 0, 1, 1],
        }
    )


def score_assets(assets: pd.DataFrame) -> pd.DataFrame:
    """Estimate inherent and residual risk for each asset."""
    scored = assets.copy()

    scored["inherent_risk"] = (
        scored["exposure"] * scored["impact"] * scored["threat_likelihood"]
    )

    scored["residual_risk"] = scored["inherent_risk"] * (
        1 - scored["control_strength"]
    )

    scored["risk_band"] = pd.cut(
        scored["residual_risk"],
        bins=[0, 0.10, 0.20, 1.00],
        labels=["low", "moderate", "high"],
        include_lowest=True,
    )

    scored["control_priority"] = np.select(
        [
            scored["residual_risk"] >= 0.20,
            scored["residual_risk"] >= 0.10,
        ],
        [
            "immediate_review",
            "scheduled_control_improvement",
        ],
        default="routine_monitoring",
    )

    return scored.sort_values("residual_risk", ascending=False)


def summarize_risk(scored_assets: pd.DataFrame) -> pd.DataFrame:
    """Summarize risk by risk band."""
    return (
        scored_assets.groupby("risk_band", observed=False)
        .agg(
            assets=("asset", "count"),
            mean_inherent_risk=("inherent_risk", "mean"),
            mean_residual_risk=("residual_risk", "mean"),
            mean_control_strength=("control_strength", "mean"),
            human_review_required_share=("human_review_required", "mean"),
        )
        .reset_index()
    )


def summarize_by_asset_type(scored_assets: pd.DataFrame) -> pd.DataFrame:
    """Summarize residual risk by asset type."""
    return (
        scored_assets.groupby("asset_type")
        .agg(
            assets=("asset", "count"),
            mean_residual_risk=("residual_risk", "mean"),
            max_residual_risk=("residual_risk", "max"),
            mean_control_strength=("control_strength", "mean"),
        )
        .reset_index()
        .sort_values("max_residual_risk", ascending=False)
    )


def main() -> None:
    """Run the defensive risk-scoring workflow."""
    article_dir = Path(__file__).resolve().parents[1]
    output_dir = article_dir / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    assets = create_asset_inventory()
    scored_assets = score_assets(assets)
    risk_summary = summarize_risk(scored_assets)
    asset_type_summary = summarize_by_asset_type(scored_assets)

    scored_assets.to_csv(output_dir / "ai_security_asset_risk_scores.csv", index=False)
    risk_summary.to_csv(output_dir / "ai_security_risk_summary.csv", index=False)
    asset_type_summary.to_csv(output_dir / "ai_security_asset_type_summary.csv", index=False)

    print("\nAI security asset risk scores")
    print(scored_assets.to_string(index=False))

    print("\nRisk-band summary")
    print(risk_summary.to_string(index=False))

    print("\nAsset-type summary")
    print(asset_type_summary.to_string(index=False))


if __name__ == "__main__":
    main()
