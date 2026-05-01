"""
Robustness and Adversarial Resilience in Machine Learning

Python workflow:
- Simulate robustness and adversarial resilience evaluation records.
- Score clean performance, corruption robustness, adversarial robustness,
  out-of-distribution behavior, privacy exposure, detection quality,
  containment readiness, and governance risk.
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


def simulate_robustness_evaluations(n: int = 280) -> pd.DataFrame:
    """Create synthetic robustness and adversarial evaluation records."""
    system_types = [
        "image_classifier",
        "tabular_risk_model",
        "text_classifier",
        "rag_assistant",
        "llm_application",
        "ai_agent",
        "multimodal_system",
    ]

    attack_types = [
        "corruption",
        "evasion",
        "data_poisoning",
        "prompt_injection",
        "retrieval_poisoning",
        "model_extraction",
        "feedback_manipulation",
        "out_of_distribution",
    ]

    rows = []

    for i in range(n):
        system_type = rng.choice(system_types)
        attack_type = rng.choice(attack_types)

        clean_performance = rng.uniform(0.78, 0.98)
        corruption_performance = clean_performance - rng.uniform(0.02, 0.22)
        adversarial_performance = clean_performance - rng.uniform(0.05, 0.38)
        ood_performance = clean_performance - rng.uniform(0.04, 0.30)

        detection_score = rng.uniform(0.35, 0.98)
        containment_score = rng.uniform(0.40, 1.00)
        recovery_score = rng.uniform(0.35, 1.00)
        auditability_score = rng.uniform(0.55, 1.00)
        privacy_control_score = rng.uniform(0.45, 1.00)
        human_review_score = rng.uniform(0.45, 1.00)

        attack_success_rate = rng.uniform(0.02, 0.55)
        incident_severity = rng.choice([1, 2, 3, 4, 5], p=[0.32, 0.28, 0.20, 0.13, 0.07])
        exposure_level = rng.uniform(0.05, 1.00)

        if attack_type in ["prompt_injection", "retrieval_poisoning"] and system_type in ["rag_assistant", "llm_application", "ai_agent"]:
            attack_success_rate = max(attack_success_rate, rng.uniform(0.20, 0.60))
            exposure_level = max(exposure_level, rng.uniform(0.35, 1.00))

        if attack_type == "model_extraction":
            privacy_control_score = min(privacy_control_score, rng.uniform(0.35, 0.80))

        rows.append(
            {
                "eval_id": f"ROBUST-EVAL-{i:03d}",
                "system_type": system_type,
                "attack_type": attack_type,
                "clean_performance": float(clean_performance),
                "corruption_performance": float(max(corruption_performance, 0.0)),
                "adversarial_performance": float(max(adversarial_performance, 0.0)),
                "ood_performance": float(max(ood_performance, 0.0)),
                "detection_score": float(detection_score),
                "containment_score": float(containment_score),
                "recovery_score": float(recovery_score),
                "auditability_score": float(auditability_score),
                "privacy_control_score": float(privacy_control_score),
                "human_review_score": float(human_review_score),
                "attack_success_rate": float(attack_success_rate),
                "incident_severity": int(incident_severity),
                "exposure_level": float(exposure_level),
            }
        )

    return pd.DataFrame(rows)


def score_robustness(records: pd.DataFrame) -> pd.DataFrame:
    """Score robustness, resilience, and governance risk."""
    scored = records.copy()

    scored["corruption_drop"] = scored["clean_performance"] - scored["corruption_performance"]
    scored["adversarial_drop"] = scored["clean_performance"] - scored["adversarial_performance"]
    scored["ood_drop"] = scored["clean_performance"] - scored["ood_performance"]

    scored["robustness_score"] = np.clip(
        1
        - (
            0.30 * scored["corruption_drop"]
            + 0.45 * scored["adversarial_drop"]
            + 0.25 * scored["ood_drop"]
        ),
        0,
        1,
    )

    scored["resilience_score"] = (
        0.25 * scored["detection_score"]
        + 0.25 * scored["containment_score"]
        + 0.20 * scored["recovery_score"]
        + 0.15 * scored["auditability_score"]
        + 0.15 * scored["human_review_score"]
    )

    scored["security_control_score"] = (
        0.35 * scored["detection_score"]
        + 0.25 * scored["privacy_control_score"]
        + 0.20 * scored["containment_score"]
        + 0.20 * scored["auditability_score"]
    )

    scored["impact_index"] = np.clip(
        0.45 * scored["attack_success_rate"]
        + 0.30 * (scored["incident_severity"] / 5)
        + 0.25 * scored["exposure_level"],
        0,
        1,
    )

    scored["adversarial_system_risk"] = (
        0.25 * (1 - scored["robustness_score"])
        + 0.25 * (1 - scored["resilience_score"])
        + 0.20 * (1 - scored["security_control_score"])
        + 0.30 * scored["impact_index"]
    )

    scored["review_required"] = (
        (scored["adversarial_system_risk"] > 0.42)
        | (scored["adversarial_drop"] > 0.22)
        | (scored["attack_success_rate"] > 0.30)
        | (scored["incident_severity"] >= 4)
        | (scored["privacy_control_score"] < 0.65)
        | (scored["containment_score"] < 0.65)
        | (scored["recovery_score"] < 0.60)
    )

    scored["recommended_action"] = np.select(
        [
            scored["adversarial_system_risk"] > 0.60,
            scored["attack_success_rate"] > 0.40,
            scored["adversarial_drop"] > 0.25,
            scored["privacy_control_score"] < 0.65,
            scored["containment_score"] < 0.65,
        ],
        [
            "pause_deployment_and_open_security_review",
            "run_adaptive_red_team_and_patch_controls",
            "review_adversarial_training_or_detection_controls",
            "open_privacy_and_extraction_risk_review",
            "improve_containment_and_rollback_controls",
        ],
        default="continue_monitoring_and_periodic_testing",
    )

    return scored.sort_values("adversarial_system_risk", ascending=False)


def summarize_by_attack(scored: pd.DataFrame) -> pd.DataFrame:
    """Summarize robustness and risk by attack type."""
    return (
        scored.groupby("attack_type")
        .agg(
            evaluations=("eval_id", "count"),
            mean_clean_performance=("clean_performance", "mean"),
            mean_adversarial_drop=("adversarial_drop", "mean"),
            mean_robustness_score=("robustness_score", "mean"),
            mean_resilience_score=("resilience_score", "mean"),
            mean_attack_success_rate=("attack_success_rate", "mean"),
            mean_system_risk=("adversarial_system_risk", "mean"),
            review_rate=("review_required", "mean"),
        )
        .reset_index()
        .sort_values("mean_system_risk", ascending=False)
    )


def main() -> None:
    """Run robustness and adversarial resilience review."""
    records = simulate_robustness_evaluations()
    scored = score_robustness(records)
    attack_summary = summarize_by_attack(scored)

    governance_summary = pd.DataFrame(
        [
            {
                "evaluations_reviewed": len(scored),
                "review_required": int(scored["review_required"].sum()),
                "high_severity_cases": int((scored["incident_severity"] >= 4).sum()),
                "high_attack_success_cases": int((scored["attack_success_rate"] > 0.30).sum()),
                "mean_robustness_score": scored["robustness_score"].mean(),
                "mean_resilience_score": scored["resilience_score"].mean(),
                "mean_security_control_score": scored["security_control_score"].mean(),
                "mean_adversarial_system_risk": scored["adversarial_system_risk"].mean(),
            }
        ]
    )

    records.to_csv(OUTPUT_DIR / "python_robustness_evaluation_records.csv", index=False)
    scored.to_csv(OUTPUT_DIR / "python_adversarial_risk_scores.csv", index=False)
    attack_summary.to_csv(OUTPUT_DIR / "python_attack_type_summary.csv", index=False)
    governance_summary.to_csv(OUTPUT_DIR / "python_robustness_governance_summary.csv", index=False)

    memo = f"""# Robustness and Adversarial Resilience Governance Memo

Evaluations reviewed: {int(governance_summary.loc[0, "evaluations_reviewed"])}
Review required: {int(governance_summary.loc[0, "review_required"])}
High-severity cases: {int(governance_summary.loc[0, "high_severity_cases"])}
High attack-success cases: {int(governance_summary.loc[0, "high_attack_success_cases"])}
Mean robustness score: {governance_summary.loc[0, "mean_robustness_score"]:.4f}
Mean resilience score: {governance_summary.loc[0, "mean_resilience_score"]:.4f}
Mean security-control score: {governance_summary.loc[0, "mean_security_control_score"]:.4f}
Mean adversarial system risk: {governance_summary.loc[0, "mean_adversarial_system_risk"]:.4f}

Interpretation:
- Clean performance is not sufficient evidence of robustness.
- Adversarial drops, attack success, severity, and exposure should be reviewed together.
- Resilience depends on detection, containment, recovery, auditability, and human review.
- High-risk findings should trigger red-team review, mitigation, rollback readiness, and governance documentation.
"""

    (OUTPUT_DIR / "python_robustness_governance_memo.md").write_text(memo)

    print(governance_summary.T)
    print(attack_summary)
    print(scored.head(10))
    print(memo)


if __name__ == "__main__":
    main()
