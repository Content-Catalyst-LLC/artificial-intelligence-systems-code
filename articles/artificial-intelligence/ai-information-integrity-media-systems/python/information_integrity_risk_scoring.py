"""
Information-integrity risk scoring workflow.

This script creates synthetic media-content records and estimates:
- provenance gap
- amplification risk
- information-integrity risk
- governance priority bands

It is intended for educational and governance-design purposes, not production use.
"""

from pathlib import Path
import pandas as pd


def create_content_inventory() -> pd.DataFrame:
    """Create a synthetic media-content inventory."""
    return pd.DataFrame(
        {
            "content_id": ["C-001", "C-002", "C-003", "C-004", "C-005", "C-006"],
            "content_type": [
                "news_summary",
                "synthetic_video",
                "local_news_article",
                "health_claim_post",
                "election_clip",
                "science_explainer",
            ],
            "source_credibility": [0.85, 0.30, 0.80, 0.35, 0.45, 0.90],
            "provenance_available": [1, 0, 1, 0, 0, 1],
            "claim_uncertainty": [0.20, 0.75, 0.25, 0.80, 0.70, 0.15],
            "amplification_ratio": [1.4, 4.8, 1.1, 5.2, 3.9, 1.2],
            "public_impact": [0.70, 0.85, 0.55, 0.90, 0.95, 0.60],
            "verification_strength": [0.80, 0.25, 0.75, 0.30, 0.35, 0.85],
        }
    )


def score_information_integrity(content: pd.DataFrame) -> pd.DataFrame:
    """Score information-integrity risks for synthetic content records."""
    scored = content.copy()

    scored["provenance_gap"] = 1 - scored["provenance_available"]

    scored["amplification_risk"] = (
        scored["amplification_ratio"] / scored["amplification_ratio"].max()
    )

    scored["information_integrity_risk"] = (
        0.25 * scored["claim_uncertainty"]
        + 0.20 * scored["amplification_risk"]
        + 0.20 * scored["public_impact"]
        + 0.20 * scored["provenance_gap"]
        + 0.15 * (1 - scored["verification_strength"])
    )

    scored["risk_band"] = pd.cut(
        scored["information_integrity_risk"],
        bins=[0, 0.30, 0.50, 1.00],
        labels=["low", "moderate", "high"],
        include_lowest=True,
    )

    return scored.sort_values("information_integrity_risk", ascending=False)


def main() -> None:
    """Run the information-integrity workflow."""
    article_dir = Path(__file__).resolve().parents[1]
    output_dir = article_dir / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    content = create_content_inventory()
    scored = score_information_integrity(content)

    scored.to_csv(output_dir / "information_integrity_risk_scores.csv", index=False)

    summary = (
        scored.groupby("risk_band", observed=False)
        .agg(
            content_items=("content_id", "count"),
            mean_information_integrity_risk=("information_integrity_risk", "mean"),
            mean_provenance_gap=("provenance_gap", "mean"),
            mean_amplification_risk=("amplification_risk", "mean"),
        )
        .reset_index()
    )

    summary.to_csv(output_dir / "information_integrity_risk_summary.csv", index=False)

    print(scored)
    print(summary)


if __name__ == "__main__":
    main()
