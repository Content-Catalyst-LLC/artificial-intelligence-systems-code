"""
Self-Supervised Learning and Foundation Models

Python workflow:
- self-supervised pretraining simulation
- representation utility scoring
- data risk scoring
- foundation-model risk scoring
- governance review routing
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


def simulate_pretraining_runs(n: int = 150) -> pd.DataFrame:
    """Create synthetic self-supervised pretraining records."""
    objectives = [
        "next_token_prediction",
        "masked_language_modeling",
        "masked_autoencoding",
        "contrastive_learning",
        "multimodal_alignment",
    ]

    modalities = [
        "text",
        "vision",
        "audio",
        "code",
        "scientific_data",
        "multimodal",
    ]

    rows = []

    for i in range(n):
        representation_quality = rng.uniform(0.55, 0.95)
        transfer_performance = representation_quality + rng.normal(0.02, 0.05)

        rows.append(
            {
                "run_id": f"SSL-{i:03d}",
                "objective": rng.choice(objectives),
                "modality": rng.choice(modalities),
                "representation_quality": float(np.clip(representation_quality, 0, 1)),
                "transfer_performance": float(np.clip(transfer_performance, 0, 1)),
                "robustness_score": float(rng.uniform(0.45, 0.92)),
                "grounding_score": float(rng.uniform(0.35, 0.90)),
                "data_provenance_score": float(rng.uniform(0.25, 0.95)),
                "data_quality_score": float(rng.uniform(0.40, 0.98)),
                "privacy_risk": float(rng.beta(2.0, 6.0)),
                "bias_risk": float(rng.beta(2.5, 5.5)),
                "compute_cost_index": float(rng.uniform(0.10, 0.95)),
                "governance_readiness": float(rng.uniform(0.25, 0.95)),
                "broad_downstream_reuse": int(rng.choice([0, 1], p=[0.45, 0.55])),
            }
        )

    return pd.DataFrame(rows)


def score_pretraining_runs(records: pd.DataFrame) -> pd.DataFrame:
    """Score self-supervised runs for utility and governance risk."""
    scored = records.copy()

    scored["model_utility_score"] = (
        0.30 * scored["representation_quality"]
        + 0.30 * scored["transfer_performance"]
        + 0.20 * scored["robustness_score"]
        + 0.20 * scored["grounding_score"]
    )

    scored["data_risk_score"] = (
        0.30 * (1 - scored["data_provenance_score"])
        + 0.25 * (1 - scored["data_quality_score"])
        + 0.25 * scored["privacy_risk"]
        + 0.20 * scored["bias_risk"]
    )

    scored["foundation_model_risk"] = (
        0.30 * scored["data_risk_score"]
        + 0.20 * (1 - scored["governance_readiness"])
        + 0.15 * scored["compute_cost_index"]
        + 0.15 * (1 - scored["grounding_score"])
        + 0.10 * scored["bias_risk"]
        + 0.10 * scored["broad_downstream_reuse"]
    )

    scored["review_required"] = (
        (scored["foundation_model_risk"] > 0.45)
        | (scored["data_provenance_score"] < 0.50)
        | (scored["privacy_risk"] > 0.45)
        | (scored["bias_risk"] > 0.45)
        | ((scored["broad_downstream_reuse"] == 1) & (scored["governance_readiness"] < 0.65))
    )

    scored["deployment_recommendation"] = np.select(
        [
            scored["foundation_model_risk"] > 0.60,
            scored["review_required"],
            scored["model_utility_score"] > 0.75,
        ],
        [
            "pause_for_foundation_model_risk_review",
            "approve_only_after_governance_review",
            "candidate_for_controlled_adaptation",
        ],
        default="continue_pretraining_or_evaluation",
    )

    return scored.sort_values("foundation_model_risk", ascending=False)


def summarize_by_objective(scored: pd.DataFrame) -> pd.DataFrame:
    """Summarize pretraining quality and risk by objective."""
    return (
        scored.groupby("objective")
        .agg(
            runs=("run_id", "count"),
            mean_model_utility=("model_utility_score", "mean"),
            mean_transfer_performance=("transfer_performance", "mean"),
            mean_data_risk=("data_risk_score", "mean"),
            mean_foundation_model_risk=("foundation_model_risk", "mean"),
            review_rate=("review_required", "mean"),
            mean_governance_readiness=("governance_readiness", "mean"),
        )
        .reset_index()
        .sort_values("mean_model_utility", ascending=False)
    )


def main() -> None:
    """Run the self-supervised pretraining review workflow."""
    records = simulate_pretraining_runs()
    scored = score_pretraining_runs(records)
    objective_summary = summarize_by_objective(scored)

    governance_summary = pd.DataFrame(
        [
            {
                "runs_reviewed": len(scored),
                "objectives_compared": scored["objective"].nunique(),
                "review_required": int(scored["review_required"].sum()),
                "broad_reuse_runs": int(scored["broad_downstream_reuse"].sum()),
                "high_risk_runs": int((scored["foundation_model_risk"] > 0.60).sum()),
                "mean_model_utility": scored["model_utility_score"].mean(),
                "mean_foundation_model_risk": scored["foundation_model_risk"].mean(),
            }
        ]
    )

    records.to_csv(OUTPUT_DIR / "python_self_supervised_pretraining_records.csv", index=False)
    scored.to_csv(OUTPUT_DIR / "python_foundation_model_risk_scores.csv", index=False)
    objective_summary.to_csv(OUTPUT_DIR / "python_pretraining_objective_summary.csv", index=False)
    governance_summary.to_csv(OUTPUT_DIR / "python_foundation_model_governance_summary.csv", index=False)

    memo = f"""# Self-Supervised Learning and Foundation Model Governance Memo

Runs reviewed: {int(governance_summary.loc[0, "runs_reviewed"])}
Objectives compared: {int(governance_summary.loc[0, "objectives_compared"])}
Review required: {int(governance_summary.loc[0, "review_required"])}
Broad downstream reuse runs: {int(governance_summary.loc[0, "broad_reuse_runs"])}
High-risk runs: {int(governance_summary.loc[0, "high_risk_runs"])}
Mean model utility: {governance_summary.loc[0, "mean_model_utility"]:.4f}
Mean foundation model risk: {governance_summary.loc[0, "mean_foundation_model_risk"]:.4f}

Interpretation:
- Self-supervised models should be evaluated for representation quality and downstream transfer.
- Broad downstream reuse increases governance obligations.
- Data provenance, privacy risk, bias risk, and grounding quality should be reviewed before adaptation.
- Foundation models require lifecycle monitoring because defects can propagate across many systems.
"""

    (OUTPUT_DIR / "python_foundation_model_governance_memo.md").write_text(memo)

    print(objective_summary)
    print(governance_summary.T)
    print(memo)


if __name__ == "__main__":
    main()
