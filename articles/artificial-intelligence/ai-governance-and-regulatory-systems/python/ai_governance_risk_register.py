"""
AI Governance and Regulatory Systems Mini-Workflow

This script demonstrates:
- AI use-case inventory
- inherent risk scoring
- mitigation maturity
- residual risk scoring
- control mapping

It is educational and uses synthetic data.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


OUTPUT_DIR = Path("../outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def build_use_case_inventory() -> pd.DataFrame:
    """Create a synthetic AI governance use-case inventory."""
    return pd.DataFrame(
        [
            {
                "system_id": "ai-001",
                "system_name": "Customer Support Summarizer",
                "domain": "customer_service",
                "risk_tier": "limited",
                "likelihood": 2,
                "severity": 2,
                "mitigation_maturity": 0.70,
                "owner": "CX Operations",
                "required_controls": "user_notice; logging; quality_review",
            },
            {
                "system_id": "ai-002",
                "system_name": "Hiring Screening Classifier",
                "domain": "employment",
                "risk_tier": "high",
                "likelihood": 3,
                "severity": 5,
                "mitigation_maturity": 0.45,
                "owner": "People Operations",
                "required_controls": "bias_audit; human_review; appeal_process; documentation",
            },
            {
                "system_id": "ai-003",
                "system_name": "Medical Triage Assistant",
                "domain": "healthcare",
                "risk_tier": "high",
                "likelihood": 3,
                "severity": 5,
                "mitigation_maturity": 0.60,
                "owner": "Clinical Operations",
                "required_controls": "clinical_validation; human_oversight; incident_reporting; monitoring",
            },
            {
                "system_id": "ai-004",
                "system_name": "Infrastructure Drift Monitor",
                "domain": "critical_infrastructure",
                "risk_tier": "high",
                "likelihood": 2,
                "severity": 5,
                "mitigation_maturity": 0.55,
                "owner": "Infrastructure Reliability",
                "required_controls": "robustness_testing; monitoring; escalation; audit_logs",
            },
        ]
    )


def score_risk(use_cases: pd.DataFrame) -> pd.DataFrame:
    """Compute inherent risk, residual risk, and review priority."""
    scored = use_cases.copy()

    scored["inherent_risk"] = scored["likelihood"] * scored["severity"]

    scored["residual_risk"] = (
        scored["inherent_risk"] * (1 - scored["mitigation_maturity"])
    )

    scored["review_priority"] = pd.cut(
        scored["residual_risk"],
        bins=[-0.01, 2.0, 5.0, 10.0, float("inf")],
        labels=["low", "moderate", "high", "critical"],
    )

    return scored


def build_control_map(scored_cases: pd.DataFrame) -> pd.DataFrame:
    """Explode required controls into a system-control map."""
    rows = []

    for _, row in scored_cases.iterrows():
        for control in row["required_controls"].split("; "):
            rows.append(
                {
                    "system_id": row["system_id"],
                    "system_name": row["system_name"],
                    "risk_tier": row["risk_tier"],
                    "owner": row["owner"],
                    "control": control,
                }
            )

    return pd.DataFrame(rows)


def main() -> None:
    use_cases = build_use_case_inventory()
    scored = score_risk(use_cases)
    control_map = build_control_map(scored)

    scored.to_csv(OUTPUT_DIR / "ai_governance_risk_register.csv", index=False)
    control_map.to_csv(OUTPUT_DIR / "ai_governance_control_map.csv", index=False)

    print("Risk register:")
    print(scored.sort_values("residual_risk", ascending=False))

    print("\nControl map:")
    print(control_map)


if __name__ == "__main__":
    main()
