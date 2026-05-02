"""
Rights-impact and public-accountability scoring workflow.

This script creates a synthetic inventory of AI use cases and estimates
inherent rights risk, governance-control strength, residual rights risk,
disparate burden, and accountability priority.

It is intended for educational and governance-design purposes, not production use.
"""

from __future__ import annotations

from pathlib import Path
import numpy as np
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
                "tenant_screening",
                "worker_productivity_monitoring",
            ],
            "domain": [
                "public_services",
                "education",
                "healthcare",
                "employment",
                "platform_governance",
                "infrastructure",
                "housing",
                "labor",
            ],
            "harm_probability": [0.35, 0.30, 0.25, 0.40, 0.45, 0.20, 0.42, 0.38],
            "harm_impact": [0.90, 0.75, 0.85, 0.80, 0.55, 0.60, 0.82, 0.72],
            "vulnerability_exposure": [0.90, 0.70, 0.65, 0.75, 0.50, 0.45, 0.80, 0.68],
            "institutional_power": [0.95, 0.75, 0.85, 0.70, 0.60, 0.80, 0.78, 0.76],
            "governance_control_strength": [0.45, 0.50, 0.65, 0.40, 0.55, 0.60, 0.42, 0.48],
            "appeal_available": [1, 1, 1, 0, 0, 1, 0, 1],
            "remedy_available": [1, 1, 1, 0, 0, 1, 0, 0],
            "public_reporting": [1, 0, 0, 0, 0, 1, 0, 0],
        }
    )


def score_rights_risk(use_cases: pd.DataFrame) -> pd.DataFrame:
    """Estimate inherent and residual rights risk."""
    scored = use_cases.copy()

    scored["inherent_rights_risk"] = (
        0.30 * scored["harm_probability"]
        + 0.30 * scored["harm_impact"]
        + 0.20 * scored["vulnerability_exposure"]
        + 0.20 * scored["institutional_power"]
    )

    scored["accountability_gap"] = (
        (1 - scored["appeal_available"]) * 0.35
        + (1 - scored["remedy_available"]) * 0.40
        + (1 - scored["public_reporting"]) * 0.25
    )

    scored["adjusted_governance_strength"] = np.clip(
        scored["governance_control_strength"] - 0.20 * scored["accountability_gap"],
        0,
        1,
    )

    scored["residual_rights_risk"] = (
        scored["inherent_rights_risk"] * (1 - scored["adjusted_governance_strength"])
    )

    scored["risk_band"] = pd.cut(
        scored["residual_rights_risk"],
        bins=[0, 0.20, 0.35, 1.00],
        labels=["low", "moderate", "high"],
        include_lowest=True,
    )

    scored["accountability_priority"] = np.select(
        [
            scored["residual_rights_risk"] >= 0.35,
            scored["residual_rights_risk"] >= 0.20,
        ],
        [
            "rights_review_required",
            "control_improvement_required",
        ],
        default="routine_monitoring",
    )

    return scored.sort_values("residual_rights_risk", ascending=False)


def summarize_by_risk_band(scored: pd.DataFrame) -> pd.DataFrame:
    """Summarize risk scores by risk band."""
    return (
        scored.groupby("risk_band", observed=False)
        .agg(
            use_cases=("use_case", "count"),
            mean_inherent_rights_risk=("inherent_rights_risk", "mean"),
            mean_residual_rights_risk=("residual_rights_risk", "mean"),
            mean_governance_control_strength=("governance_control_strength", "mean"),
            mean_accountability_gap=("accountability_gap", "mean"),
        )
        .reset_index()
    )


def summarize_by_domain(scored: pd.DataFrame) -> pd.DataFrame:
    """Summarize rights risk by domain."""
    return (
        scored.groupby("domain")
        .agg(
            use_cases=("use_case", "count"),
            mean_residual_rights_risk=("residual_rights_risk", "mean"),
            max_residual_rights_risk=("residual_rights_risk", "max"),
            appeal_available_share=("appeal_available", "mean"),
            remedy_available_share=("remedy_available", "mean"),
            public_reporting_share=("public_reporting", "mean"),
        )
        .reset_index()
        .sort_values("max_residual_rights_risk", ascending=False)
    )


def main() -> None:
    """Run the rights-impact scoring workflow."""
    article_dir = Path(__file__).resolve().parents[1]
    output_dir = article_dir / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    use_cases = create_use_case_inventory()
    scored = score_rights_risk(use_cases)
    band_summary = summarize_by_risk_band(scored)
    domain_summary = summarize_by_domain(scored)

    scored.to_csv(output_dir / "rights_impact_scores.csv", index=False)
    band_summary.to_csv(output_dir / "rights_impact_summary.csv", index=False)
    domain_summary.to_csv(output_dir / "rights_domain_summary.csv", index=False)

    print("\nRights-impact scores")
    print(scored.to_string(index=False))

    print("\nRisk-band summary")
    print(band_summary.to_string(index=False))

    print("\nDomain summary")
    print(domain_summary.to_string(index=False))


if __name__ == "__main__":
    main()
