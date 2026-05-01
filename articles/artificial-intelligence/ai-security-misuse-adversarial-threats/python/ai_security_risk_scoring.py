"""
Defensive AI security risk scoring workflow.

This script creates a synthetic AI-system asset inventory and estimates
inherent risk, control strength, and residual risk.

It does not implement attack techniques. It is intended for governance,
security planning, documentation, and monitoring.
"""

from pathlib import Path
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
            ],
            "exposure": [0.50, 0.45, 0.75, 0.65, 0.80, 0.90, 0.40, 0.55],
            "impact": [0.85, 0.80, 0.75, 0.70, 0.90, 0.95, 0.65, 0.70],
            "threat_likelihood": [0.40, 0.35, 0.60, 0.55, 0.65, 0.70, 0.30, 0.45],
            "control_strength": [0.60, 0.55, 0.50, 0.45, 0.65, 0.55, 0.70, 0.60],
        }
    )


def score_assets(assets: pd.DataFrame) -> pd.DataFrame:
    """Estimate inherent and residual risk for each asset."""
    assets = assets.copy()

    assets["inherent_risk"] = (
        assets["exposure"] * assets["impact"] * assets["threat_likelihood"]
    )

    assets["residual_risk"] = assets["inherent_risk"] * (1 - assets["control_strength"])

    assets["risk_band"] = pd.cut(
        assets["residual_risk"],
        bins=[0, 0.10, 0.20, 1.00],
        labels=["low", "moderate", "high"],
        include_lowest=True,
    )

    return assets.sort_values("residual_risk", ascending=False)


def main() -> None:
    """Run the defensive risk-scoring workflow."""
    article_dir = Path(__file__).resolve().parents[1]
    output_dir = article_dir / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    assets = create_asset_inventory()
    scored_assets = score_assets(assets)

    scored_assets.to_csv(output_dir / "ai_security_asset_risk_scores.csv", index=False)

    summary = (
        scored_assets.groupby("risk_band", observed=False)
        .agg(
            assets=("asset", "count"),
            mean_inherent_risk=("inherent_risk", "mean"),
            mean_residual_risk=("residual_risk", "mean"),
            mean_control_strength=("control_strength", "mean"),
        )
        .reset_index()
    )

    summary.to_csv(output_dir / "ai_security_risk_summary.csv", index=False)

    print(scored_assets)
    print(summary)


if __name__ == "__main__":
    main()
