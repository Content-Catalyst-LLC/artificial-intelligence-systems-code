"""
Information-integrity risk scoring workflow.

This script creates synthetic media-content records and estimates:
- provenance gap
- amplification risk
- correction gap
- information-integrity risk
- governance priority bands
- review requirements

It is intended for educational and governance-design purposes, not production use.
"""

from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd


def create_content_inventory() -> pd.DataFrame:
    """Create a synthetic media-content inventory."""
    return pd.DataFrame(
        {
            "content_id": [
                "C-001",
                "C-002",
                "C-003",
                "C-004",
                "C-005",
                "C-006",
                "C-007",
                "C-008",
            ],
            "content_type": [
                "news_summary",
                "synthetic_video",
                "local_news_article",
                "health_claim_post",
                "election_clip",
                "science_explainer",
                "ai_generated_audio",
                "public_emergency_update",
            ],
            "source_type": [
                "news_aggregator",
                "unknown_source",
                "local_news",
                "platform_creator",
                "platform_creator",
                "science_publication",
                "unknown_source",
                "official_source",
            ],
            "source_credibility": [0.85, 0.30, 0.80, 0.35, 0.45, 0.90, 0.25, 0.92],
            "provenance_available": [1, 0, 1, 0, 0, 1, 0, 1],
            "ai_generated_or_assisted": [1, 1, 0, 0, 1, 0, 1, 0],
            "claim_uncertainty": [0.20, 0.75, 0.25, 0.80, 0.70, 0.15, 0.78, 0.18],
            "amplification_ratio": [1.4, 4.8, 1.1, 5.2, 3.9, 1.2, 4.4, 1.6],
            "public_impact": [0.70, 0.85, 0.55, 0.90, 0.95, 0.60, 0.88, 0.95],
            "verification_strength": [0.80, 0.25, 0.75, 0.30, 0.35, 0.85, 0.20, 0.90],
            "correction_available": [1, 0, 1, 0, 0, 1, 0, 1],
            "human_reviewed": [1, 0, 1, 0, 1, 1, 0, 1],
        }
    )


def score_information_integrity(content: pd.DataFrame) -> pd.DataFrame:
    """Score information-integrity risks for synthetic content records."""
    scored = content.copy()

    scored["provenance_gap"] = 1 - scored["provenance_available"]
    scored["correction_gap"] = 1 - scored["correction_available"]
    scored["human_review_gap"] = 1 - scored["human_reviewed"]

    scored["amplification_risk"] = (
        scored["amplification_ratio"] / scored["amplification_ratio"].max()
    )

    scored["information_integrity_risk"] = (
        0.22 * scored["claim_uncertainty"]
        + 0.18 * scored["amplification_risk"]
        + 0.18 * scored["public_impact"]
        + 0.18 * scored["provenance_gap"]
        + 0.14 * (1 - scored["verification_strength"])
        + 0.05 * scored["correction_gap"]
        + 0.05 * scored["human_review_gap"]
    )

    scored["risk_band"] = pd.cut(
        scored["information_integrity_risk"],
        bins=[0, 0.30, 0.50, 1.00],
        labels=["low", "moderate", "high"],
        include_lowest=True,
    )

    scored["governance_priority"] = np.select(
        [
            scored["information_integrity_risk"] >= 0.50,
            scored["information_integrity_risk"] >= 0.30,
        ],
        [
            "urgent_review_required",
            "scheduled_review_required",
        ],
        default="routine_monitoring",
    )

    scored["provenance_review_required"] = np.where(
        (scored["ai_generated_or_assisted"] == 1)
        & (scored["provenance_available"] == 0),
        1,
        0,
    )

    scored["correction_review_required"] = np.where(
        (scored["information_integrity_risk"] >= 0.50)
        & (scored["correction_available"] == 0),
        1,
        0,
    )

    return scored.sort_values("information_integrity_risk", ascending=False)


def summarize_by_risk_band(scored: pd.DataFrame) -> pd.DataFrame:
    """Summarize information-integrity scores by risk band."""
    return (
        scored.groupby("risk_band", observed=False)
        .agg(
            content_items=("content_id", "count"),
            mean_information_integrity_risk=("information_integrity_risk", "mean"),
            mean_provenance_gap=("provenance_gap", "mean"),
            mean_amplification_risk=("amplification_risk", "mean"),
            mean_correction_gap=("correction_gap", "mean"),
            provenance_review_required_share=("provenance_review_required", "mean"),
            correction_review_required_share=("correction_review_required", "mean"),
        )
        .reset_index()
    )


def summarize_by_source_type(scored: pd.DataFrame) -> pd.DataFrame:
    """Summarize information-integrity risk by source type."""
    return (
        scored.groupby("source_type")
        .agg(
            content_items=("content_id", "count"),
            mean_source_credibility=("source_credibility", "mean"),
            mean_information_integrity_risk=("information_integrity_risk", "mean"),
            mean_provenance_available=("provenance_available", "mean"),
            mean_verification_strength=("verification_strength", "mean"),
            mean_amplification_ratio=("amplification_ratio", "mean"),
        )
        .reset_index()
        .sort_values("mean_information_integrity_risk", ascending=False)
    )


def main() -> None:
    """Run the information-integrity workflow."""
    article_dir = Path(__file__).resolve().parents[1]
    output_dir = article_dir / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    content = create_content_inventory()
    scored = score_information_integrity(content)
    risk_summary = summarize_by_risk_band(scored)
    source_summary = summarize_by_source_type(scored)

    scored.to_csv(output_dir / "information_integrity_risk_scores.csv", index=False)
    risk_summary.to_csv(output_dir / "information_integrity_risk_summary.csv", index=False)
    source_summary.to_csv(output_dir / "information_integrity_source_summary.csv", index=False)

    print("\nInformation-integrity risk scores")
    print(scored.to_string(index=False))

    print("\nRisk-band summary")
    print(risk_summary.to_string(index=False))

    print("\nSource-type summary")
    print(source_summary.to_string(index=False))


if __name__ == "__main__":
    main()
