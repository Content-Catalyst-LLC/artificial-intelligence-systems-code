"""
AI Systems in Organizations and Institutions Mini-Workflow

This script demonstrates:
- organizational AI readiness scoring
- workflow risk scoring
- decision-allocation recommendations
- governance-gap diagnostics
- human-oversight classification

It is educational and uses synthetic data.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


OUTPUT_DIR = Path("../outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def build_use_cases() -> pd.DataFrame:
    """Create synthetic organizational AI use cases."""
    return pd.DataFrame(
        {
            "use_case": [
                "customer_support_routing",
                "employee_performance_review",
                "clinical_triage_support",
                "procurement_anomaly_detection",
                "public_benefits_eligibility",
                "infrastructure_emergency_response",
            ],
            "data_quality": [0.86, 0.62, 0.78, 0.82, 0.66, 0.74],
            "infrastructure": [0.82, 0.70, 0.76, 0.84, 0.68, 0.80],
            "staff_ai_literacy": [0.74, 0.58, 0.72, 0.76, 0.60, 0.70],
            "governance_maturity": [0.72, 0.50, 0.74, 0.78, 0.55, 0.82],
            "workflow_fit": [0.88, 0.44, 0.70, 0.86, 0.52, 0.68],
            "trust": [0.78, 0.42, 0.66, 0.80, 0.48, 0.70],
            "harm_potential": [0.20, 0.74, 0.86, 0.40, 0.88, 0.94],
            "rights_impact": [0.18, 0.82, 0.72, 0.24, 0.92, 0.70],
            "irreversibility": [0.14, 0.68, 0.78, 0.32, 0.75, 0.90],
            "opacity": [0.40, 0.66, 0.58, 0.50, 0.72, 0.52],
        }
    )


def recommend_decision_mode(row: pd.Series) -> str:
    """Recommend a human-AI decision structure based on risk and readiness."""
    if row["decision_risk"] >= 0.70:
        return "human_led_with_ai_support_and_strong_review"
    if row["decision_risk"] >= 0.40:
        return "human_in_the_loop"
    if row["ai_readiness"] >= 0.70:
        return "monitored_automation"
    return "ai_decision_support_only"


def score_use_cases(use_cases: pd.DataFrame) -> pd.DataFrame:
    """Compute readiness, risk, governance gap, and decision-mode recommendations."""
    scored = use_cases.copy()

    scored["ai_readiness"] = (
        0.20 * scored["data_quality"]
        + 0.16 * scored["infrastructure"]
        + 0.16 * scored["staff_ai_literacy"]
        + 0.22 * scored["governance_maturity"]
        + 0.16 * scored["workflow_fit"]
        + 0.10 * scored["trust"]
    )

    scored["decision_risk"] = (
        0.40 * scored["harm_potential"]
        + 0.30 * scored["rights_impact"]
        + 0.20 * scored["irreversibility"]
        + 0.10 * scored["opacity"]
    )

    scored["recommended_mode"] = scored.apply(recommend_decision_mode, axis=1)

    scored["governance_gap"] = (
        scored["decision_risk"] - scored["governance_maturity"]
    )

    scored["requires_governance_action"] = scored["governance_gap"] > 0.15

    return scored


def summarize_governance(scored: pd.DataFrame) -> pd.DataFrame:
    """Create governance summary diagnostics."""
    return pd.DataFrame(
        [
            {"metric": "mean_ai_readiness", "value": scored["ai_readiness"].mean()},
            {"metric": "mean_decision_risk", "value": scored["decision_risk"].mean()},
            {
                "metric": "share_requiring_governance_action",
                "value": scored["requires_governance_action"].mean(),
            },
            {
                "metric": "share_high_risk_decisions",
                "value": (scored["decision_risk"] >= 0.70).mean(),
            },
        ]
    )


def main() -> None:
    use_cases = build_use_cases()
    scored = score_use_cases(use_cases)
    summary = summarize_governance(scored)

    scored_sorted = scored.sort_values("decision_risk", ascending=False)

    scored.to_csv(OUTPUT_DIR / "organizational_ai_use_cases.csv", index=False)
    scored_sorted.to_csv(OUTPUT_DIR / "organizational_ai_use_cases_ranked.csv", index=False)
    summary.to_csv(OUTPUT_DIR / "organizational_ai_governance_summary.csv", index=False)

    print(scored_sorted[
        [
            "use_case",
            "ai_readiness",
            "decision_risk",
            "recommended_mode",
            "governance_gap",
            "requires_governance_action",
        ]
    ])
    print(summary)


if __name__ == "__main__":
    main()
