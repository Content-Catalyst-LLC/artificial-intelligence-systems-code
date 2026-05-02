"""
Risk-register and documentation-priority scoring workflow.

This script creates synthetic AI risk-register entries and estimates:
- residual risk
- documentation completeness
- documentation priority
- stale-documentation pressure
- governance priority bands

It is intended for educational and governance-design purposes, not production use.
"""

from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd


def create_risk_register() -> pd.DataFrame:
    """Create a synthetic AI risk register."""
    return pd.DataFrame(
        {
            "risk_id": ["R-001", "R-002", "R-003", "R-004", "R-005", "R-006", "R-007", "R-008"],
            "risk_name": [
                "unfair_outcome_disparity",
                "out_of_scope_use",
                "insufficient_human_review",
                "data_quality_gap",
                "security_or_misuse_event",
                "monitoring_not_reviewed",
                "stale_model_card",
                "missing_appeal_documentation",
            ],
            "risk_category": [
                "fairness",
                "governance",
                "human_oversight",
                "data_quality",
                "security",
                "monitoring",
                "documentation",
                "contestability",
            ],
            "likelihood": [0.35, 0.40, 0.30, 0.45, 0.25, 0.50, 0.42, 0.32],
            "impact": [0.90, 0.75, 0.85, 0.70, 0.80, 0.65, 0.72, 0.88],
            "mitigation_strength": [0.45, 0.55, 0.50, 0.40, 0.60, 0.35, 0.42, 0.48],
            "documentation_completeness": [0.60, 0.70, 0.55, 0.50, 0.65, 0.40, 0.35, 0.45],
            "days_since_review": [45, 60, 90, 120, 30, 150, 210, 135],
            "review_interval_days": [90, 90, 90, 90, 60, 60, 90, 90],
            "owner": [
                "Responsible AI",
                "Product Governance",
                "Operations",
                "Data Stewardship",
                "Security",
                "AI Operations",
                "Model Governance",
                "Legal and Compliance",
            ],
            "status": [
                "open",
                "mitigating",
                "open",
                "open",
                "mitigating",
                "open",
                "open",
                "escalated",
            ],
        }
    )


def score_risk_register(risk_register: pd.DataFrame) -> pd.DataFrame:
    """Score residual risk, documentation priority, and staleness."""
    scored = risk_register.copy()

    scored["residual_risk"] = (
        scored["likelihood"] * scored["impact"] * (1 - scored["mitigation_strength"])
    )

    scored["staleness_score"] = (
        scored["days_since_review"] / scored["review_interval_days"]
    ).clip(lower=0)

    scored["documentation_priority"] = (
        scored["residual_risk"]
        * (1 - scored["documentation_completeness"])
        * (1 + 0.25 * scored["staleness_score"])
    )

    scored["priority_band"] = pd.cut(
        scored["documentation_priority"],
        bins=[0, 0.05, 0.10, 1.00],
        labels=["low", "moderate", "high"],
        include_lowest=True,
    )

    scored["review_required"] = np.where(
        (scored["priority_band"] == "high")
        | (scored["staleness_score"] >= 1.0)
        | (scored["status"] == "escalated"),
        1,
        0,
    )

    return scored.sort_values("documentation_priority", ascending=False)


def summarize_by_priority(scored: pd.DataFrame) -> pd.DataFrame:
    """Summarize risks by documentation-priority band."""
    return (
        scored.groupby("priority_band", observed=False)
        .agg(
            risks=("risk_id", "count"),
            mean_residual_risk=("residual_risk", "mean"),
            mean_documentation_completeness=("documentation_completeness", "mean"),
            mean_staleness_score=("staleness_score", "mean"),
            mean_documentation_priority=("documentation_priority", "mean"),
            review_required_share=("review_required", "mean"),
        )
        .reset_index()
    )


def summarize_by_category(scored: pd.DataFrame) -> pd.DataFrame:
    """Summarize documentation risk by risk category."""
    return (
        scored.groupby("risk_category")
        .agg(
            risks=("risk_id", "count"),
            mean_residual_risk=("residual_risk", "mean"),
            max_documentation_priority=("documentation_priority", "max"),
            mean_documentation_completeness=("documentation_completeness", "mean"),
            review_required_share=("review_required", "mean"),
        )
        .reset_index()
        .sort_values("max_documentation_priority", ascending=False)
    )


def main() -> None:
    """Run the documentation-priority workflow."""
    article_dir = Path(__file__).resolve().parents[1]
    output_dir = article_dir / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    risk_register = create_risk_register()
    scored = score_risk_register(risk_register)
    priority_summary = summarize_by_priority(scored)
    category_summary = summarize_by_category(scored)

    scored.to_csv(output_dir / "risk_register_documentation_scores.csv", index=False)
    priority_summary.to_csv(output_dir / "risk_register_documentation_summary.csv", index=False)
    category_summary.to_csv(output_dir / "risk_register_category_summary.csv", index=False)

    print("\nRisk-register documentation scores")
    print(scored.to_string(index=False))

    print("\nPriority-band summary")
    print(priority_summary.to_string(index=False))

    print("\nCategory summary")
    print(category_summary.to_string(index=False))


if __name__ == "__main__":
    main()
