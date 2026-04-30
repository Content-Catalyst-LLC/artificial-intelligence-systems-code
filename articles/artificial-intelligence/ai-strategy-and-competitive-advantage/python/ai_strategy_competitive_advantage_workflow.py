"""
AI Strategy and Competitive Advantage Mini-Workflow

This script demonstrates:
- AI initiative scoring
- value, defensibility, and readiness diagnostics
- strategic dependence penalties
- value-capture estimation
- portfolio prioritization

It is educational and uses synthetic data.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


OUTPUT_DIR = Path("../outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def build_ai_strategy_portfolio() -> pd.DataFrame:
    """Create a synthetic AI initiative portfolio."""
    return pd.DataFrame(
        [
            {
                "initiative": "customer_support_copilot",
                "business_value": 0.75,
                "defensibility": 0.35,
                "data_readiness": 0.70,
                "workflow_fit": 0.80,
                "governance_maturity": 0.65,
                "platform_dependence": 0.70,
                "value_capture": 0.45,
            },
            {
                "initiative": "proprietary_workflow_intelligence",
                "business_value": 0.70,
                "defensibility": 0.85,
                "data_readiness": 0.75,
                "workflow_fit": 0.78,
                "governance_maturity": 0.72,
                "platform_dependence": 0.35,
                "value_capture": 0.80,
            },
            {
                "initiative": "generic_marketing_generation",
                "business_value": 0.55,
                "defensibility": 0.20,
                "data_readiness": 0.65,
                "workflow_fit": 0.68,
                "governance_maturity": 0.55,
                "platform_dependence": 0.60,
                "value_capture": 0.35,
            },
            {
                "initiative": "regulated_decision_support",
                "business_value": 0.82,
                "defensibility": 0.78,
                "data_readiness": 0.62,
                "workflow_fit": 0.70,
                "governance_maturity": 0.88,
                "platform_dependence": 0.45,
                "value_capture": 0.76,
            },
            {
                "initiative": "internal_knowledge_agent",
                "business_value": 0.68,
                "defensibility": 0.70,
                "data_readiness": 0.82,
                "workflow_fit": 0.76,
                "governance_maturity": 0.74,
                "platform_dependence": 0.50,
                "value_capture": 0.68,
            },
        ]
    )


def score_portfolio(portfolio: pd.DataFrame) -> pd.DataFrame:
    """Score AI initiatives for capability and strategic advantage."""
    scored = portfolio.copy()

    scored["capability_score"] = (
        0.25 * scored["business_value"]
        + 0.20 * scored["data_readiness"]
        + 0.20 * scored["workflow_fit"]
        + 0.20 * scored["governance_maturity"]
        + 0.15 * scored["defensibility"]
    )

    scored["strategic_advantage_score"] = (
        scored["capability_score"]
        * scored["defensibility"]
        * scored["value_capture"]
        * (1 - 0.40 * scored["platform_dependence"])
    )

    scored["priority_band"] = pd.cut(
        scored["strategic_advantage_score"],
        bins=[0, 0.10, 0.25, 1.00],
        labels=["low", "medium", "high"],
        include_lowest=True,
    )

    return scored.sort_values("strategic_advantage_score", ascending=False)


def summarize_portfolio(scored: pd.DataFrame) -> pd.DataFrame:
    """Summarize portfolio scores by priority band."""
    return (
        scored
        .groupby("priority_band", observed=False)
        .agg(
            initiatives=("initiative", "count"),
            mean_business_value=("business_value", "mean"),
            mean_defensibility=("defensibility", "mean"),
            mean_governance_maturity=("governance_maturity", "mean"),
            mean_platform_dependence=("platform_dependence", "mean"),
            mean_value_capture=("value_capture", "mean"),
            mean_strategic_advantage_score=("strategic_advantage_score", "mean"),
        )
        .reset_index()
    )


def main() -> None:
    portfolio = build_ai_strategy_portfolio()
    scored = score_portfolio(portfolio)
    summary = summarize_portfolio(scored)

    scored.to_csv(OUTPUT_DIR / "ai_strategy_portfolio_scores.csv", index=False)
    summary.to_csv(OUTPUT_DIR / "ai_strategy_priority_summary.csv", index=False)

    print(scored)
    print(summary)


if __name__ == "__main__":
    main()
