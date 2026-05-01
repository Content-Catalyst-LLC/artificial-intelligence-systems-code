"""
Transfer Learning, Fine-Tuning, and Model Adaptation

Python workflow:
- adaptation experiment simulation
- transfer gain scoring
- forgetting risk scoring
- overfit risk scoring
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


def simulate_adaptation_experiments(n: int = 120) -> pd.DataFrame:
    """Create synthetic transfer-learning experiment records."""
    methods = [
        "base_model_zero_shot",
        "linear_head_only",
        "full_fine_tuning",
        "regularized_fine_tuning",
        "adapter_tuning",
        "lora",
        "qlora",
    ]

    rows = []

    for experiment_id in range(n):
        method = rng.choice(methods)

        base_target = rng.normal(0.62, 0.04)
        base_source_retention = rng.normal(0.91, 0.03)

        if method == "base_model_zero_shot":
            target_performance = base_target
            source_retention = base_source_retention
            trainable_parameter_share = 0.00
            compute_cost = 0.05
        elif method == "linear_head_only":
            target_performance = base_target + rng.normal(0.05, 0.03)
            source_retention = base_source_retention - rng.normal(0.01, 0.01)
            trainable_parameter_share = 0.01
            compute_cost = 0.12
        elif method == "full_fine_tuning":
            target_performance = base_target + rng.normal(0.12, 0.04)
            source_retention = base_source_retention - rng.normal(0.10, 0.04)
            trainable_parameter_share = 1.00
            compute_cost = 0.90
        elif method == "regularized_fine_tuning":
            target_performance = base_target + rng.normal(0.10, 0.035)
            source_retention = base_source_retention - rng.normal(0.05, 0.02)
            trainable_parameter_share = 1.00
            compute_cost = 0.88
        elif method == "adapter_tuning":
            target_performance = base_target + rng.normal(0.09, 0.03)
            source_retention = base_source_retention - rng.normal(0.02, 0.015)
            trainable_parameter_share = 0.04
            compute_cost = 0.28
        elif method == "lora":
            target_performance = base_target + rng.normal(0.10, 0.03)
            source_retention = base_source_retention - rng.normal(0.02, 0.015)
            trainable_parameter_share = 0.02
            compute_cost = 0.24
        else:
            target_performance = base_target + rng.normal(0.09, 0.035)
            source_retention = base_source_retention - rng.normal(0.025, 0.015)
            trainable_parameter_share = 0.02
            compute_cost = 0.16

        rows.append(
            {
                "experiment_id": f"ADAPT-{experiment_id:03d}",
                "method": method,
                "target_performance": float(np.clip(target_performance, 0, 1)),
                "source_retention": float(np.clip(source_retention, 0, 1)),
                "trainable_parameter_share": trainable_parameter_share,
                "compute_cost_index": compute_cost,
                "target_dataset_size": int(rng.integers(100, 5000)),
                "target_data_quality": float(rng.uniform(0.45, 0.98)),
                "domain_shift_score": float(rng.uniform(0.05, 0.70)),
                "sensitive_domain": int(rng.choice([0, 1], p=[0.75, 0.25])),
            }
        )

    return pd.DataFrame(rows)


def score_adaptation(records: pd.DataFrame) -> pd.DataFrame:
    """Score adaptation experiments for transfer gain and governance risk."""
    scored = records.copy()

    baseline = scored.loc[
        scored["method"].eq("base_model_zero_shot"),
        "target_performance",
    ].mean()

    if np.isnan(baseline):
        baseline = 0.62

    scored["transfer_gain"] = scored["target_performance"] - baseline
    scored["forgetting_risk"] = np.clip(1 - scored["source_retention"], 0, 1)

    scored["overfit_risk"] = (
        0.35 * (1 - scored["target_data_quality"])
        + 0.35 * (1 / np.sqrt(scored["target_dataset_size"] / 100))
        + 0.30 * scored["domain_shift_score"]
    )

    scored["adaptation_risk"] = (
        0.30 * scored["forgetting_risk"]
        + 0.25 * scored["overfit_risk"]
        + 0.20 * scored["domain_shift_score"]
        + 0.15 * scored["sensitive_domain"]
        + 0.10 * scored["compute_cost_index"]
    )

    scored["review_required"] = (
        (scored["adaptation_risk"] > 0.45)
        | (scored["transfer_gain"] < 0)
        | (scored["source_retention"] < 0.80)
        | (scored["sensitive_domain"] == 1)
    )

    scored["deployment_recommendation"] = np.select(
        [
            scored["transfer_gain"] < 0,
            scored["adaptation_risk"] > 0.55,
            scored["review_required"],
            scored["transfer_gain"] > 0.05,
        ],
        [
            "reject_negative_transfer",
            "pause_for_risk_review",
            "approve_only_after_review",
            "candidate_for_controlled_deployment",
        ],
        default="continue_experimentation",
    )

    return scored.sort_values("adaptation_risk", ascending=False)


def summarize_by_method(scored: pd.DataFrame) -> pd.DataFrame:
    """Create method-level experiment summary."""
    return (
        scored.groupby("method")
        .agg(
            experiments=("experiment_id", "count"),
            mean_target_performance=("target_performance", "mean"),
            mean_transfer_gain=("transfer_gain", "mean"),
            mean_source_retention=("source_retention", "mean"),
            mean_adaptation_risk=("adaptation_risk", "mean"),
            review_rate=("review_required", "mean"),
            mean_trainable_parameter_share=("trainable_parameter_share", "mean"),
            mean_compute_cost=("compute_cost_index", "mean"),
        )
        .reset_index()
        .sort_values("mean_transfer_gain", ascending=False)
    )


def main() -> None:
    """Run the adaptation review workflow."""
    records = simulate_adaptation_experiments()
    scored = score_adaptation(records)
    method_summary = summarize_by_method(scored)

    governance_summary = pd.DataFrame(
        [
            {
                "experiments_reviewed": len(scored),
                "methods_compared": scored["method"].nunique(),
                "review_required": int(scored["review_required"].sum()),
                "negative_transfer_cases": int((scored["transfer_gain"] < 0).sum()),
                "high_forgetting_risk_cases": int((scored["source_retention"] < 0.80).sum()),
                "mean_transfer_gain": scored["transfer_gain"].mean(),
                "mean_adaptation_risk": scored["adaptation_risk"].mean(),
            }
        ]
    )

    records.to_csv(OUTPUT_DIR / "python_adaptation_experiment_records.csv", index=False)
    scored.to_csv(OUTPUT_DIR / "python_adaptation_risk_scores.csv", index=False)
    method_summary.to_csv(OUTPUT_DIR / "python_adaptation_method_summary.csv", index=False)
    governance_summary.to_csv(OUTPUT_DIR / "python_adaptation_governance_summary.csv", index=False)

    memo = f"""# Transfer Learning and Fine-Tuning Governance Memo

Experiments reviewed: {int(governance_summary.loc[0, "experiments_reviewed"])}
Methods compared: {int(governance_summary.loc[0, "methods_compared"])}
Review required: {int(governance_summary.loc[0, "review_required"])}
Negative transfer cases: {int(governance_summary.loc[0, "negative_transfer_cases"])}
High forgetting-risk cases: {int(governance_summary.loc[0, "high_forgetting_risk_cases"])}
Mean transfer gain: {governance_summary.loc[0, "mean_transfer_gain"]:.4f}
Mean adaptation risk: {governance_summary.loc[0, "mean_adaptation_risk"]:.4f}

Interpretation:
- Adapted models should be compared against base and baseline systems.
- Fine-tuning should be evaluated for target gain and source capability retention.
- Parameter-efficient methods can reduce cost and forgetting risk but still require review.
- Sensitive-domain adaptation should require documented governance approval.
"""

    (OUTPUT_DIR / "python_adaptation_governance_memo.md").write_text(memo)

    print(method_summary)
    print(governance_summary.T)
    print(memo)


if __name__ == "__main__":
    main()
