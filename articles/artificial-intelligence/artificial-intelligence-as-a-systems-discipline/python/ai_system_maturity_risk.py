"""
Artificial Intelligence as a Systems Discipline

Python workflow:
- synthetic AI system inventory
- technical maturity scoring
- governance maturity scoring
- systemic risk scoring
- lifecycle review routing
- governance memo generation
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ARTICLE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ARTICLE_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

RANDOM_SEED = 42
rng = np.random.default_rng(RANDOM_SEED)


def create_ai_system_inventory(n: int = 150) -> pd.DataFrame:
    """Create a synthetic inventory of deployed or proposed AI systems."""
    systems = pd.DataFrame(
        {
            "system_id": [f"AI-SYS-{i:03d}" for i in range(n)],
            "domain": rng.choice(
                [
                    "decision_support",
                    "generative_content",
                    "infrastructure",
                    "environmental_monitoring",
                    "scientific_research",
                    "customer_operations",
                    "internal_productivity",
                ],
                size=n,
            ),
            "risk_tier": rng.choice(
                ["low", "medium", "high"],
                size=n,
                p=[0.35, 0.45, 0.20],
            ),
            "data_quality": rng.uniform(0.40, 0.98, n),
            "model_reliability": rng.uniform(0.45, 0.97, n),
            "infrastructure_readiness": rng.uniform(0.35, 0.96, n),
            "human_oversight": rng.uniform(0.25, 0.95, n),
            "monitoring_coverage": rng.uniform(0.20, 0.95, n),
            "governance_readiness": rng.uniform(0.20, 0.95, n),
            "explainability": rng.uniform(0.20, 0.95, n),
            "security_readiness": rng.uniform(0.30, 0.96, n),
            "external_impact": rng.uniform(0.05, 0.90, n),
        }
    )

    systems["high_stakes"] = systems["risk_tier"].eq("high").astype(int)

    return systems


def score_ai_systems(systems: pd.DataFrame) -> pd.DataFrame:
    """Score AI systems for technical maturity, governance maturity, and risk."""
    scored = systems.copy()

    scored["technical_maturity"] = (
        0.30 * scored["data_quality"]
        + 0.30 * scored["model_reliability"]
        + 0.20 * scored["infrastructure_readiness"]
        + 0.20 * scored["security_readiness"]
    )

    scored["governance_maturity"] = (
        0.30 * scored["human_oversight"]
        + 0.30 * scored["monitoring_coverage"]
        + 0.25 * scored["governance_readiness"]
        + 0.15 * scored["explainability"]
    )

    scored["system_maturity"] = (
        0.50 * scored["technical_maturity"]
        + 0.50 * scored["governance_maturity"]
    )

    scored["systemic_risk"] = (
        0.30 * (1 - scored["system_maturity"])
        + 0.20 * (1 - scored["monitoring_coverage"])
        + 0.20 * (1 - scored["governance_readiness"])
        + 0.15 * scored["external_impact"]
        + 0.15 * scored["high_stakes"]
    )

    scored["review_required"] = (
        (scored["systemic_risk"] > 0.45)
        | (scored["governance_readiness"] < 0.45)
        | (scored["monitoring_coverage"] < 0.40)
        | ((scored["high_stakes"] == 1) & (scored["human_oversight"] < 0.65))
    )

    scored["deployment_status_recommendation"] = np.select(
        [
            scored["systemic_risk"] > 0.60,
            scored["review_required"],
            scored["system_maturity"] >= 0.75,
        ],
        [
            "pause_or_remediate_before_expansion",
            "approve_only_with_governance_review",
            "acceptable_with_monitoring",
        ],
        default="continue_development",
    )

    return scored.sort_values("systemic_risk", ascending=False)


def create_governance_summary(scored: pd.DataFrame) -> pd.DataFrame:
    """Create portfolio-level governance summary."""
    return pd.DataFrame(
        [
            {
                "systems_reviewed": len(scored),
                "review_required": int(scored["review_required"].sum()),
                "high_stakes_systems": int(scored["high_stakes"].sum()),
                "mean_system_maturity": scored["system_maturity"].mean(),
                "mean_systemic_risk": scored["systemic_risk"].mean(),
                "low_monitoring_systems": int((scored["monitoring_coverage"] < 0.40).sum()),
                "low_governance_systems": int((scored["governance_readiness"] < 0.45).sum()),
                "pause_or_remediate": int(
                    scored["deployment_status_recommendation"].eq(
                        "pause_or_remediate_before_expansion"
                    ).sum()
                ),
            }
        ]
    )


def main() -> None:
    """Run the AI systems discipline maturity workflow."""
    inventory = create_ai_system_inventory()
    scored = score_ai_systems(inventory)
    summary = create_governance_summary(scored)

    inventory.to_csv(OUTPUT_DIR / "python_ai_system_inventory.csv", index=False)
    scored.to_csv(OUTPUT_DIR / "python_ai_system_maturity_risk_scores.csv", index=False)
    summary.to_csv(OUTPUT_DIR / "python_ai_systems_governance_summary.csv", index=False)

    memo = f"""# AI Systems Discipline Governance Memo

Systems reviewed: {int(summary.loc[0, "systems_reviewed"])}
Review required: {int(summary.loc[0, "review_required"])}
High-stakes systems: {int(summary.loc[0, "high_stakes_systems"])}
Low-monitoring systems: {int(summary.loc[0, "low_monitoring_systems"])}
Low-governance systems: {int(summary.loc[0, "low_governance_systems"])}
Pause or remediate before expansion: {int(summary.loc[0, "pause_or_remediate"])}

Interpretation:
- AI systems should be evaluated across technical and governance maturity.
- High-stakes systems require stronger human oversight and monitoring.
- Deployment readiness depends on lifecycle evidence, not model performance alone.
- Systems with weak governance, weak monitoring, or high external impact require review.
"""

    (OUTPUT_DIR / "python_ai_systems_governance_memo.md").write_text(memo)

    print(scored.head(10))
    print(summary.T)
    print(memo)


if __name__ == "__main__":
    main()
