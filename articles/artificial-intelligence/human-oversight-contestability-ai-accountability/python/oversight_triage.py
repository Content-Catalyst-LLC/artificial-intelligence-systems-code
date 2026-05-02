"""
Oversight triage simulation for AI-assisted decisions.

This script creates synthetic cases and applies transparent escalation rules
based on risk, uncertainty, rights sensitivity, vulnerability, and reviewer
capacity. It is intended for educational and governance-design purposes,
not production use.
"""

from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd


def create_cases(n_cases: int = 1000, seed: int = 42) -> pd.DataFrame:
    """Create a synthetic AI-assisted decision dataset."""
    rng = np.random.default_rng(seed)

    cases = pd.DataFrame(
        {
            "case_id": np.arange(1, n_cases + 1),
            "uncertainty": rng.beta(2, 5, n_cases),
            "harm_probability": rng.beta(2, 8, n_cases),
            "harm_impact": rng.uniform(0.1, 1.0, n_cases),
            "rights_sensitive": rng.binomial(1, 0.20, n_cases),
            "vulnerable_context": rng.binomial(1, 0.15, n_cases),
            "affected_group": rng.choice(
                ["Group A", "Group B", "Group C"],
                n_cases,
                p=[0.50, 0.30, 0.20],
            ),
        }
    )

    cases["expected_risk"] = cases["harm_probability"] * cases["harm_impact"]

    return cases


def apply_escalation_rule(
    cases: pd.DataFrame,
    risk_threshold: float = 0.18,
    uncertainty_threshold: float = 0.55,
) -> pd.DataFrame:
    """Apply a transparent governance escalation rule."""
    cases = cases.copy()

    cases["human_review_required"] = (
        (cases["expected_risk"] >= risk_threshold)
        | (cases["uncertainty"] >= uncertainty_threshold)
        | (cases["rights_sensitive"] == 1)
        | (cases["vulnerable_context"] == 1)
    )

    cases["route"] = np.where(
        cases["human_review_required"],
        "human_review",
        "standard_processing",
    )

    cases["review_reason"] = np.select(
        [
            cases["rights_sensitive"] == 1,
            cases["vulnerable_context"] == 1,
            cases["expected_risk"] >= risk_threshold,
            cases["uncertainty"] >= uncertainty_threshold,
        ],
        [
            "rights_sensitive",
            "vulnerable_context",
            "risk_threshold",
            "uncertainty_threshold",
        ],
        default="standard_processing",
    )

    return cases


def summarize_routes(cases: pd.DataFrame) -> pd.DataFrame:
    """Summarize oversight routing behavior."""
    return (
        cases.groupby("route")
        .agg(
            cases=("case_id", "count"),
            mean_uncertainty=("uncertainty", "mean"),
            mean_expected_risk=("expected_risk", "mean"),
            rights_sensitive_share=("rights_sensitive", "mean"),
            vulnerable_context_share=("vulnerable_context", "mean"),
        )
        .reset_index()
    )


def summarize_by_group(cases: pd.DataFrame) -> pd.DataFrame:
    """Summarize review routing by affected group."""
    return (
        cases.groupby("affected_group")
        .agg(
            cases=("case_id", "count"),
            review_rate=("human_review_required", "mean"),
            mean_uncertainty=("uncertainty", "mean"),
            mean_expected_risk=("expected_risk", "mean"),
            rights_sensitive_share=("rights_sensitive", "mean"),
            vulnerable_context_share=("vulnerable_context", "mean"),
        )
        .reset_index()
    )


def estimate_reviewer_capacity(
    cases: pd.DataFrame,
    available_reviewer_hours: float = 80.0,
    minutes_per_review: float = 12.0,
) -> pd.DataFrame:
    """Estimate whether review volume exceeds available human-review capacity."""
    required_reviews = int(cases["human_review_required"].sum())
    review_capacity = int((available_reviewer_hours * 60) / minutes_per_review)
    capacity_gap = required_reviews - review_capacity

    return pd.DataFrame(
        {
            "required_reviews": [required_reviews],
            "available_reviewer_hours": [available_reviewer_hours],
            "minutes_per_review": [minutes_per_review],
            "estimated_review_capacity": [review_capacity],
            "capacity_gap": [capacity_gap],
            "capacity_status": [
                "insufficient_capacity" if capacity_gap > 0 else "capacity_available"
            ],
        }
    )


def main() -> None:
    """Run the oversight triage workflow."""
    article_dir = Path(__file__).resolve().parents[1]
    output_dir = article_dir / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    cases = create_cases()
    cases = apply_escalation_rule(cases)

    route_summary = summarize_routes(cases)
    group_summary = summarize_by_group(cases)
    capacity_summary = estimate_reviewer_capacity(cases)

    cases.to_csv(output_dir / "oversight_triage_cases.csv", index=False)
    route_summary.to_csv(output_dir / "oversight_triage_summary.csv", index=False)
    group_summary.to_csv(output_dir / "oversight_group_summary.csv", index=False)
    capacity_summary.to_csv(output_dir / "reviewer_capacity_summary.csv", index=False)

    print("\nOversight route summary")
    print(route_summary.to_string(index=False))

    print("\nAffected-group routing summary")
    print(group_summary.to_string(index=False))

    print("\nReviewer capacity summary")
    print(capacity_summary.to_string(index=False))

    print(f"\nOverall review rate: {cases['human_review_required'].mean():.2%}")


if __name__ == "__main__":
    main()
