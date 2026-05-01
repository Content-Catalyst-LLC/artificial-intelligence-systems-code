"""
Multimodal AI: Language, Vision, Audio, and Action

Python workflow:
- multimodal AI evaluation simulation
- modality coverage scoring
- cross-modal alignment and grounding review
- action safety, privacy, accessibility, and human review scoring
- governance risk routing
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


def simulate_multimodal_evaluations(n: int = 240) -> pd.DataFrame:
    """Create synthetic multimodal evaluation records."""
    use_cases = [
        "visual_question_answering",
        "audio_event_understanding",
        "video_event_summary",
        "document_image_analysis",
        "sensor_fusion_monitoring",
        "robotic_action_planning",
        "multimodal_retrieval",
    ]

    rows = []

    for i in range(n):
        use_case = rng.choice(use_cases)

        has_text = int(rng.choice([0, 1], p=[0.10, 0.90]))
        has_vision = int(rng.choice([0, 1], p=[0.25, 0.75]))
        has_audio = int(rng.choice([0, 1], p=[0.55, 0.45]))
        has_video = int(rng.choice([0, 1], p=[0.65, 0.35]))
        has_sensor = int(rng.choice([0, 1], p=[0.60, 0.40]))
        has_action = int(use_case == "robotic_action_planning")

        modality_count = has_text + has_vision + has_audio + has_video + has_sensor + has_action

        rows.append(
            {
                "eval_id": f"MM-EVAL-{i:03d}",
                "use_case": use_case,
                "has_text": has_text,
                "has_vision": has_vision,
                "has_audio": has_audio,
                "has_video": has_video,
                "has_sensor": has_sensor,
                "has_action": has_action,
                "modality_count": modality_count,
                "cross_modal_alignment": float(rng.uniform(0.35, 0.98)),
                "grounding_score": float(rng.uniform(0.35, 0.98)),
                "robustness_score": float(rng.uniform(0.40, 0.98)),
                "conflict_detection_score": float(rng.uniform(0.30, 0.95)),
                "privacy_control_score": float(rng.uniform(0.50, 1.00)),
                "accessibility_score": float(rng.uniform(0.45, 1.00)),
                "action_safety_score": float(rng.uniform(0.50, 1.00) if has_action else rng.uniform(0.70, 1.00)),
                "human_review_score": float(rng.uniform(0.45, 1.00)),
                "modality_missing_risk": float(max(0.0, 0.50 - (modality_count / 6))),
                "modality_conflict_risk": float(rng.beta(2.0, 5.5)),
                "latency_seconds": float(rng.gamma(shape=2.4, scale=1.2)),
                "compute_cost_index": float(rng.uniform(0.10, 0.95)),
            }
        )

    return pd.DataFrame(rows)


def score_multimodal_system(records: pd.DataFrame) -> pd.DataFrame:
    """Score multimodal records for capability and governance risk."""
    scored = records.copy()

    scored["modality_coverage_score"] = np.minimum(scored["modality_count"] / 4, 1)

    scored["multimodal_capability_score"] = (
        0.20 * scored["modality_coverage_score"]
        + 0.20 * scored["cross_modal_alignment"]
        + 0.20 * scored["grounding_score"]
        + 0.15 * scored["robustness_score"]
        + 0.15 * scored["conflict_detection_score"]
        + 0.10 * scored["accessibility_score"]
    )

    scored["safety_and_governance_score"] = (
        0.25 * scored["privacy_control_score"]
        + 0.25 * scored["action_safety_score"]
        + 0.20 * scored["human_review_score"]
        + 0.15 * scored["conflict_detection_score"]
        + 0.15 * scored["robustness_score"]
    )

    scored["multimodal_system_risk"] = (
        0.22 * (1 - scored["multimodal_capability_score"])
        + 0.22 * (1 - scored["safety_and_governance_score"])
        + 0.16 * scored["modality_missing_risk"]
        + 0.16 * scored["modality_conflict_risk"]
        + 0.12 * scored["compute_cost_index"]
        + 0.12 * np.minimum(scored["latency_seconds"] / 10, 1)
    )

    scored["review_required"] = (
        (scored["multimodal_system_risk"] > 0.42)
        | (scored["cross_modal_alignment"] < 0.60)
        | (scored["grounding_score"] < 0.60)
        | (scored["conflict_detection_score"] < 0.55)
        | (scored["privacy_control_score"] < 0.70)
        | (scored["accessibility_score"] < 0.65)
        | ((scored["has_action"] == 1) & (scored["action_safety_score"] < 0.80))
    )

    scored["deployment_recommendation"] = np.select(
        [
            scored["multimodal_system_risk"] > 0.58,
            scored["review_required"],
            scored["multimodal_capability_score"] > 0.82,
        ],
        [
            "pause_for_multimodal_system_review",
            "approve_only_after_modality_and_safety_review",
            "candidate_for_controlled_deployment",
        ],
        default="continue_evaluation",
    )

    return scored.sort_values("multimodal_system_risk", ascending=False)


def summarize_by_use_case(scored: pd.DataFrame) -> pd.DataFrame:
    """Summarize multimodal quality and risk by use case."""
    return (
        scored.groupby("use_case")
        .agg(
            evaluations=("eval_id", "count"),
            mean_modality_count=("modality_count", "mean"),
            mean_alignment=("cross_modal_alignment", "mean"),
            mean_grounding=("grounding_score", "mean"),
            mean_robustness=("robustness_score", "mean"),
            mean_capability=("multimodal_capability_score", "mean"),
            mean_safety_governance=("safety_and_governance_score", "mean"),
            mean_system_risk=("multimodal_system_risk", "mean"),
            review_rate=("review_required", "mean"),
        )
        .reset_index()
        .sort_values("mean_system_risk", ascending=False)
    )


def main() -> None:
    """Run multimodal AI evaluation and governance review."""
    records = simulate_multimodal_evaluations()
    scored = score_multimodal_system(records)
    use_case_summary = summarize_by_use_case(scored)

    governance_summary = pd.DataFrame(
        [
            {
                "evaluations_reviewed": len(scored),
                "review_required": int(scored["review_required"].sum()),
                "action_cases": int(scored["has_action"].sum()),
                "low_grounding_cases": int((scored["grounding_score"] < 0.60).sum()),
                "low_alignment_cases": int((scored["cross_modal_alignment"] < 0.60).sum()),
                "mean_capability_score": scored["multimodal_capability_score"].mean(),
                "mean_safety_governance_score": scored["safety_and_governance_score"].mean(),
                "mean_multimodal_system_risk": scored["multimodal_system_risk"].mean(),
            }
        ]
    )

    records.to_csv(OUTPUT_DIR / "python_multimodal_evaluation_records.csv", index=False)
    scored.to_csv(OUTPUT_DIR / "python_multimodal_system_risk_scores.csv", index=False)
    use_case_summary.to_csv(OUTPUT_DIR / "python_multimodal_use_case_summary.csv", index=False)
    governance_summary.to_csv(OUTPUT_DIR / "python_multimodal_governance_summary.csv", index=False)

    memo = f"""# Multimodal AI Governance Memo

Evaluations reviewed: {int(governance_summary.loc[0, "evaluations_reviewed"])}
Review required: {int(governance_summary.loc[0, "review_required"])}
Action-oriented cases: {int(governance_summary.loc[0, "action_cases"])}
Low-grounding cases: {int(governance_summary.loc[0, "low_grounding_cases"])}
Low-alignment cases: {int(governance_summary.loc[0, "low_alignment_cases"])}
Mean capability score: {governance_summary.loc[0, "mean_capability_score"]:.4f}
Mean safety/governance score: {governance_summary.loc[0, "mean_safety_governance_score"]:.4f}
Mean multimodal system risk: {governance_summary.loc[0, "mean_multimodal_system_risk"]:.4f}

Interpretation:
- Multimodal AI systems should be evaluated by modality, fusion quality, grounding, and action risk.
- Missing or conflicting modalities should trigger uncertainty review.
- Action-oriented systems require stricter safety thresholds and rollback controls.
- Privacy, accessibility, and human review are core multimodal governance requirements.
"""

    (OUTPUT_DIR / "python_multimodal_governance_memo.md").write_text(memo)

    print(governance_summary.T)
    print(use_case_summary)
    print(scored.head(10))
    print(memo)


if __name__ == "__main__":
    main()
