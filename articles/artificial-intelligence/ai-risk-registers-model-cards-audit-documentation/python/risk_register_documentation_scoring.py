"""
Risk-register and documentation-priority scoring workflow.

This script creates synthetic AI risk-register entries and estimates:
- residual risk
- documentation completeness
- documentation priority
- governance priority bands

It is intended for educational and governance-design purposes, not production use.
"""

from pathlib import Path
import pandas as pd


def create_risk_register() -> pd.DataFrame:
    """Create a synthetic AI risk register."""
    return pd.DataFrame(
        {
            "risk_id": ["R-001", "R-002", "R-003", "R-004", "R-005", "R-006"],
            "risk_name": [
                "unfair_outcome_disparity",
                "out_of_scope_use",
                "insufficient_human_review",
                "data_quality_gap",
                "security_or_misuse_event",
                "monitoring_not_reviewed",
            ],
            "likelihood": [0.35, 0.40, 0.30, 0.45, 0.25, 0.50],
            "impact": [0.90, 0.75, 0.85, 0.70, 0.80, 0.65],
            "mitigation_strength": [0.45, 0.55, 0.50, 0.40, 0.60, 0.35],
            "documentation_completeness": [0.60, 0.70, 0.55, 0.50, 0.65, 0.40],
            "owner": [
                "Responsible AI",
                "Product Governance",
                "Operations",
                "Data Stewardship",
                "Security",
                "AI Operations",
            ],
        }
    )


def score_risk_register(risk_register: pd.DataFrame) -> pd.DataFrame:
    """Score residual risk and documentation priority."""
    scored = risk_register.copy()

    scored["residual_risk"] = (
        scored["likelihood"] * scored["impact"] * (1 - scored["mitigation_strength"])
    )

    scored["documentation_priority"] = (
        scored["residual_risk"] * (1 - scored["documentation_completeness"])
    )

    scored["priority_band"] = pd.cut(
        scored["documentation_priority"],
        bins=[0, 0.05, 0.10, 1.00],
        labels=["low", "moderate", "high"],
        include_lowest=True,
    )

    return scored.sort_values("documentation_priority", ascending=False)


def main() -> None:
    """Run the documentation-priority workflow."""
    article_dir = Path(__file__).resolve().parents[1]
    output_dir = article_dir / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    risk_register = create_risk_register()
    scored = score_risk_register(risk_register)

    scored.to_csv(output_dir / "risk_register_documentation_scores.csv", index=False)

    summary = (
        scored.groupby("priority_band", observed=False)
        .agg(
            risks=("risk_id", "count"),
            mean_residual_risk=("residual_risk", "mean"),
            mean_documentation_completeness=("documentation_completeness", "mean"),
            mean_documentation_priority=("documentation_priority", "mean"),
        )
        .reset_index()
    )

    summary.to_csv(output_dir / "risk_register_documentation_summary.csv", index=False)

    print(scored)
    print(summary)


if __name__ == "__main__":
    main()
