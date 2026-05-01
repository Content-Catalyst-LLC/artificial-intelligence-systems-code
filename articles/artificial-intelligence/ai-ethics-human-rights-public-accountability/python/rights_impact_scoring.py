"""
Rights-impact and public-accountability scoring workflow.

This script creates a synthetic inventory of AI use cases and estimates
inherent rights risk, governance-control strength, and residual rights risk.

It is intended for educational and governance-design purposes, not production use.
"""

from pathlib import Path
import pandas as pd


def create_use_case_inventory() -> pd.DataFrame:
    """Create a synthetic AI rights-impact use-case inventory."""
    return pd.DataFrame(
        {
            "use_case": [
                "public_benefits_review",
                "student_risk_prediction",
                "clinical_triage_support",
                "hiring_screening",
                "content_recommendation",
                "infrastructure_maintenance_prioritization",
            ],
            "harm_probability": [0.35, 0.30, 0.25, 0.40, 0.45, 0.20],
            "harm_impact": [0.90, 0.75, 0.85, 0.80, 0.55, 0.60],
            "vulnerability_exposure": [0.90, 0.70, 0.65, 0.75, 0.50, 0.45],
            "institutional_power": [0.95, 0.75, 0.85, 0.70, 0.60, 0.80],
            "governance_control_strength": [0.45, 0.50, 0.65, 0.40, 0.55, 0.60],
        }
    )


def score_rights_risk(use_cases: pd.DataFrame) -> pd.DataFrame:
    """Estimate inherent and residual rights risk."""
    use_cases = use_cases.copy()

    use_cases["inherent_rights_risk"] = (
        0.30 * use_cases["harm_probability"]
        + 0.30 * use_cases["harm_impact"]
        + 0.20 * use_cases["vulnerability_exposure"]
        + 0.20 * use_cases["institutional_power"]
    )

    use_cases["residual_rights_risk"] = (
        use_cases["inherent_rights_risk"]
        * (1 - use_cases["governance_control_strength"])
    )

    use_cases["risk_band"] = pd.cut(
        use_cases["residual_rights_risk"],
        bins=[0, 0.20, 0.35, 1.00],
        labels=["low", "moderate", "high"],
        include_lowest=True,
    )

    return use_cases.sort_values("residual_rights_risk", ascending=False)


def main() -> None:
    """Run the rights-impact scoring workflow."""
    article_dir = Path(__file__).resolve().parents[1]
    output_dir = article_dir / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    use_cases = create_use_case_inventory()
    scored = score_rights_risk(use_cases)

    scored.to_csv(output_dir / "rights_impact_scores.csv", index=False)

    summary = (
        scored.groupby("risk_band", observed=False)
        .agg(
            use_cases=("use_case", "count"),
            mean_inherent_rights_risk=("inherent_rights_risk", "mean"),
            mean_residual_rights_risk=("residual_rights_risk", "mean"),
            mean_governance_control_strength=("governance_control_strength", "mean"),
        )
        .reset_index()
    )

    summary.to_csv(output_dir / "rights_impact_summary.csv", index=False)

    print(scored)
    print(summary)


if __name__ == "__main__":
    main()
