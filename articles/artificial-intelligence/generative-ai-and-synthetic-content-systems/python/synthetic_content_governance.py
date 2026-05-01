"""
Generative AI and Synthetic Content Systems

Python workflow:
- generated content artifact records
- reliability scoring
- risk scoring
- provenance review
- human review routing
- governance summary generation
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


def create_synthetic_content_records(n: int = 180) -> pd.DataFrame:
    """Create synthetic records for generated content artifacts."""
    records = pd.DataFrame(
        {
            "artifact_id": [f"G{i:04d}" for i in range(n)],
            "modality": rng.choice(
                ["text", "image", "audio", "video", "code", "multimodal"],
                size=n,
                p=[0.36, 0.22, 0.10, 0.08, 0.14, 0.10],
            ),
            "use_case": rng.choice(
                ["drafting", "research", "marketing", "education", "design", "software"],
                size=n,
            ),
            "quality_score": rng.uniform(0.45, 0.98, n),
            "grounding_score": rng.uniform(0.20, 0.95, n),
            "prompt_adherence": rng.uniform(0.40, 0.98, n),
            "provenance_score": rng.uniform(0.10, 1.00, n),
            "sensitive_domain": rng.choice([0, 1], size=n, p=[0.76, 0.24]),
            "policy_risk": rng.beta(2.0, 6.0, n),
            "human_review_completed": rng.choice([0, 1], size=n, p=[0.32, 0.68]),
            "content_credentials_attached": rng.choice([0, 1], size=n, p=[0.55, 0.45]),
        }
    )

    records["synthetic_content_volume"] = rng.integers(1, 50, n)

    return records


def score_content_governance(records: pd.DataFrame) -> pd.DataFrame:
    """Score generated artifacts for governance and review priority."""
    scored = records.copy()

    scored["reliability_score"] = (
        0.28 * scored["quality_score"]
        + 0.28 * scored["grounding_score"]
        + 0.18 * scored["prompt_adherence"]
        + 0.18 * scored["provenance_score"]
        + 0.08 * scored["content_credentials_attached"]
    )

    scored["risk_score"] = (
        0.38 * scored["policy_risk"]
        + 0.24 * (1 - scored["grounding_score"])
        + 0.18 * (1 - scored["provenance_score"])
        + 0.12 * scored["sensitive_domain"]
        + 0.08 * (1 - scored["content_credentials_attached"])
    )

    scored["review_required"] = (
        (scored["risk_score"] > 0.45)
        | (scored["grounding_score"] < 0.50)
        | (scored["provenance_score"] < 0.45)
        | (scored["sensitive_domain"] == 1)
        | (scored["content_credentials_attached"] == 0)
    )

    scored["publication_ready"] = (
        (scored["reliability_score"] >= 0.70)
        & (scored["risk_score"] <= 0.40)
        & (scored["human_review_completed"] == 1)
        & (scored["content_credentials_attached"] == 1)
    )

    scored["priority_score"] = (
        0.42 * scored["risk_score"]
        + 0.20 * (1 - scored["reliability_score"])
        + 0.16 * scored["sensitive_domain"]
        + 0.12 * (1 - scored["human_review_completed"])
        + 0.10 * (1 - scored["content_credentials_attached"])
    )

    return scored.sort_values("priority_score", ascending=False)


def create_governance_summary(scored: pd.DataFrame) -> pd.DataFrame:
    """Create governance summary for generated content review."""
    return pd.DataFrame(
        [
            {
                "artifacts_reviewed": len(scored),
                "review_required": int(scored["review_required"].sum()),
                "publication_ready": int(scored["publication_ready"].sum()),
                "sensitive_domain_artifacts": int(scored["sensitive_domain"].sum()),
                "mean_reliability_score": scored["reliability_score"].mean(),
                "mean_risk_score": scored["risk_score"].mean(),
                "low_provenance_artifacts": int((scored["provenance_score"] < 0.45).sum()),
                "low_grounding_artifacts": int((scored["grounding_score"] < 0.50).sum()),
                "missing_content_credentials": int((scored["content_credentials_attached"] == 0).sum()),
            }
        ]
    )


def main() -> None:
    """Run the synthetic content governance workflow."""
    records = create_synthetic_content_records()
    scored = score_content_governance(records)
    summary = create_governance_summary(scored)

    records.to_csv(OUTPUT_DIR / "python_synthetic_content_records.csv", index=False)
    scored.to_csv(OUTPUT_DIR / "python_synthetic_content_governance_scores.csv", index=False)
    summary.to_csv(OUTPUT_DIR / "python_synthetic_content_governance_summary.csv", index=False)

    memo = f"""# Synthetic Content Governance Memo

Artifacts reviewed: {int(summary.loc[0, "artifacts_reviewed"])}
Review required: {int(summary.loc[0, "review_required"])}
Publication ready: {int(summary.loc[0, "publication_ready"])}
Sensitive-domain artifacts: {int(summary.loc[0, "sensitive_domain_artifacts"])}
Low-provenance artifacts: {int(summary.loc[0, "low_provenance_artifacts"])}
Low-grounding artifacts: {int(summary.loc[0, "low_grounding_artifacts"])}
Missing content credentials: {int(summary.loc[0, "missing_content_credentials"])}

Recommended actions:
1. Require human review for sensitive-domain generated content.
2. Block publication when provenance or grounding scores are below threshold.
3. Preserve prompts, model versions, edits, and approval records.
4. Attach content credentials or disclosure metadata where appropriate.
5. Monitor synthetic content volume to prevent low-quality flooding.
"""

    (OUTPUT_DIR / "python_synthetic_content_governance_memo.md").write_text(memo)

    print(scored.head(10))
    print(summary.T)
    print(memo)


if __name__ == "__main__":
    main()
