"""
Synthetic Data, Simulation, and AI Evaluation Environments

Python workflow:
- Simulate real and synthetic datasets.
- Compare distribution fidelity, task utility, privacy proximity, and rare-case coverage.
- Score evaluation risk for synthetic data and simulation environments.
- Produce governance-ready summaries.
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


def sigmoid(values: np.ndarray) -> np.ndarray:
    """Compute logistic sigmoid."""
    return 1 / (1 + np.exp(-values))


def simulate_real_data(n: int = 3000) -> pd.DataFrame:
    """Create synthetic 'real' reference data for evaluation."""
    age_like = rng.normal(45, 12, n)
    exposure = rng.gamma(shape=2.0, scale=1.2, size=n)
    sensor_score = rng.normal(0, 1, n)
    subgroup = rng.choice(["A", "B", "C"], size=n, p=[0.62, 0.28, 0.10])

    subgroup_shift = np.select(
        [subgroup == "A", subgroup == "B", subgroup == "C"],
        [0.0, 0.35, 0.75],
        default=0.0,
    )

    logit = (
        0.035 * (age_like - 45)
        + 0.45 * exposure
        + 0.70 * sensor_score
        + subgroup_shift
        - 1.7
    )

    probability = sigmoid(logit)
    outcome = rng.binomial(1, probability)

    return pd.DataFrame(
        {
            "age_like": age_like,
            "exposure": exposure,
            "sensor_score": sensor_score,
            "subgroup": subgroup,
            "outcome": outcome,
            "true_probability": probability,
        }
    )


def generate_synthetic_data(real: pd.DataFrame, n: int = 3000, mode: str = "moderate_fidelity") -> pd.DataFrame:
    """Generate a synthetic dataset with controlled imperfections."""
    if mode == "high_fidelity":
        noise_scale = 0.25
        subgroup_probs = real["subgroup"].value_counts(normalize=True).sort_index().to_numpy()
        exposure_shape = 2.0
        exposure_scale = 1.2
    elif mode == "low_privacy_high_fidelity":
        sampled = real.sample(n=n, replace=True, random_state=RANDOM_SEED).reset_index(drop=True)
        numeric_cols = ["age_like", "exposure", "sensor_score"]
        sampled[numeric_cols] = sampled[numeric_cols] + rng.normal(0, 0.03, size=(n, len(numeric_cols)))
        sampled["synthetic_mode"] = mode
        return sampled
    else:
        noise_scale = 0.65
        subgroup_probs = np.array([0.68, 0.24, 0.08])
        exposure_shape = 1.8
        exposure_scale = 1.35

    subgroup = rng.choice(["A", "B", "C"], size=n, p=subgroup_probs)
    subgroup_shift = np.select(
        [subgroup == "A", subgroup == "B", subgroup == "C"],
        [0.0, 0.25, 0.55],
        default=0.0,
    )

    age_like = rng.normal(real["age_like"].mean(), real["age_like"].std() + noise_scale, n)
    exposure = rng.gamma(shape=exposure_shape, scale=exposure_scale, size=n)
    sensor_score = rng.normal(real["sensor_score"].mean(), real["sensor_score"].std() + noise_scale, n)

    logit = (
        0.030 * (age_like - 45)
        + 0.40 * exposure
        + 0.60 * sensor_score
        + subgroup_shift
        - 1.6
    )

    probability = sigmoid(logit)
    outcome = rng.binomial(1, probability)

    return pd.DataFrame(
        {
            "age_like": age_like,
            "exposure": exposure,
            "sensor_score": sensor_score,
            "subgroup": subgroup,
            "outcome": outcome,
            "true_probability": probability,
            "synthetic_mode": mode,
        }
    )


def standardized_mean_gap(real: pd.DataFrame, synthetic: pd.DataFrame, column: str) -> float:
    """Compute standardized mean gap for one numeric column."""
    denominator = max(real[column].std(), 1e-9)
    return float(abs(real[column].mean() - synthetic[column].mean()) / denominator)


def category_distribution_gap(real: pd.DataFrame, synthetic: pd.DataFrame, column: str) -> float:
    """Compute total variation distance between categorical distributions."""
    real_dist = real[column].value_counts(normalize=True)
    syn_dist = synthetic[column].value_counts(normalize=True)
    categories = sorted(set(real_dist.index).union(set(syn_dist.index)))

    gap = 0.0
    for category in categories:
        gap += abs(real_dist.get(category, 0.0) - syn_dist.get(category, 0.0))

    return float(0.5 * gap)


def simple_auc_score(scores: np.ndarray, labels: np.ndarray) -> float:
    """Compute a simple AUC using pairwise ranking."""
    positives = scores[labels == 1]
    negatives = scores[labels == 0]

    if len(positives) == 0 or len(negatives) == 0:
        return float("nan")

    comparisons = 0.0
    total = 0

    for positive_score in positives:
        comparisons += np.sum(positive_score > negatives)
        comparisons += 0.5 * np.sum(positive_score == negatives)
        total += len(negatives)

    return float(comparisons / total)


def nearest_neighbor_privacy_risk(real: pd.DataFrame, synthetic: pd.DataFrame) -> float:
    """Estimate privacy proximity risk using a nearest-neighbor distance heuristic."""
    numeric_cols = ["age_like", "exposure", "sensor_score"]

    real_values = real[numeric_cols].to_numpy()
    syn_values = synthetic[numeric_cols].to_numpy()

    real_standardized = (real_values - real_values.mean(axis=0)) / real_values.std(axis=0)
    syn_standardized = (syn_values - real_values.mean(axis=0)) / real_values.std(axis=0)

    sample_size = min(500, len(syn_standardized))
    sampled_syn = syn_standardized[:sample_size]

    min_distances = []

    for row in sampled_syn:
        distances = np.sqrt(np.sum((real_standardized - row) ** 2, axis=1))
        min_distances.append(np.min(distances))

    min_distances = np.array(min_distances)
    return float(np.mean(min_distances < 0.10))


def evaluate_synthetic_dataset(real: pd.DataFrame, synthetic: pd.DataFrame, mode: str) -> dict[str, float | str]:
    """Evaluate synthetic data fidelity, utility, privacy, and coverage."""
    numeric_cols = ["age_like", "exposure", "sensor_score"]

    fidelity_gaps = [standardized_mean_gap(real, synthetic, column) for column in numeric_cols]
    subgroup_gap = category_distribution_gap(real, synthetic, "subgroup")
    outcome_gap = abs(real["outcome"].mean() - synthetic["outcome"].mean())

    fidelity_risk = float(np.mean(fidelity_gaps) + subgroup_gap + outcome_gap)

    real_auc = simple_auc_score(real["true_probability"].to_numpy(), real["outcome"].to_numpy())
    synthetic_auc = simple_auc_score(synthetic["true_probability"].to_numpy(), synthetic["outcome"].to_numpy())
    utility_gap = float(abs(real_auc - synthetic_auc))

    privacy_risk = nearest_neighbor_privacy_risk(real, synthetic)

    rare_real_rate = float((real["subgroup"] == "C").mean())
    rare_syn_rate = float((synthetic["subgroup"] == "C").mean())
    coverage_gap = abs(rare_real_rate - rare_syn_rate)

    evaluation_risk = float(
        0.30 * fidelity_risk
        + 0.25 * utility_gap
        + 0.25 * privacy_risk
        + 0.20 * coverage_gap
    )

    return {
        "synthetic_mode": mode,
        "fidelity_risk": fidelity_risk,
        "utility_gap": utility_gap,
        "privacy_proximity_risk": privacy_risk,
        "rare_case_coverage_gap": coverage_gap,
        "real_auc": real_auc,
        "synthetic_auc": synthetic_auc,
        "evaluation_risk": evaluation_risk,
    }


def main() -> None:
    """Run synthetic data and evaluation environment review."""
    real = simulate_real_data()
    modes = ["high_fidelity", "moderate_fidelity", "low_privacy_high_fidelity"]

    evaluations = []

    for mode in modes:
        synthetic = generate_synthetic_data(real, mode=mode)
        synthetic.to_csv(OUTPUT_DIR / f"python_synthetic_data_{mode}.csv", index=False)
        evaluations.append(evaluate_synthetic_dataset(real, synthetic, mode))

    evaluation_summary = pd.DataFrame(evaluations)

    evaluation_summary["review_required"] = (
        (evaluation_summary["evaluation_risk"] > 0.18)
        | (evaluation_summary["privacy_proximity_risk"] > 0.05)
        | (evaluation_summary["rare_case_coverage_gap"] > 0.04)
        | (evaluation_summary["utility_gap"] > 0.05)
    )

    evaluation_summary["recommended_action"] = np.select(
        [
            evaluation_summary["privacy_proximity_risk"] > 0.05,
            evaluation_summary["fidelity_risk"] > 0.20,
            evaluation_summary["rare_case_coverage_gap"] > 0.04,
            evaluation_summary["utility_gap"] > 0.05,
        ],
        [
            "open_privacy_disclosure_review",
            "improve_generator_or_limit_use",
            "expand_rare_case_generation_and_review",
            "validate_task_utility_against_real_holdout",
        ],
        default="approve_for_controlled_evaluation_use",
    )

    governance_summary = pd.DataFrame(
        [
            {
                "synthetic_generators_reviewed": len(evaluation_summary),
                "review_required_count": int(evaluation_summary["review_required"].sum()),
                "max_evaluation_risk": evaluation_summary["evaluation_risk"].max(),
                "max_privacy_proximity_risk": evaluation_summary["privacy_proximity_risk"].max(),
                "max_rare_case_coverage_gap": evaluation_summary["rare_case_coverage_gap"].max(),
                "max_utility_gap": evaluation_summary["utility_gap"].max(),
            }
        ]
    )

    real.to_csv(OUTPUT_DIR / "python_real_reference_data.csv", index=False)
    evaluation_summary.to_csv(OUTPUT_DIR / "python_synthetic_evaluation_summary.csv", index=False)
    governance_summary.to_csv(OUTPUT_DIR / "python_synthetic_governance_summary.csv", index=False)

    memo = f"""# Synthetic Data and Evaluation Environment Governance Memo

Synthetic generators reviewed: {int(governance_summary.loc[0, "synthetic_generators_reviewed"])}
Generators requiring review: {int(governance_summary.loc[0, "review_required_count"])}
Maximum evaluation risk: {governance_summary.loc[0, "max_evaluation_risk"]:.4f}
Maximum privacy proximity risk: {governance_summary.loc[0, "max_privacy_proximity_risk"]:.4f}
Maximum rare-case coverage gap: {governance_summary.loc[0, "max_rare_case_coverage_gap"]:.4f}
Maximum utility gap: {governance_summary.loc[0, "max_utility_gap"]:.4f}

Interpretation:
- Synthetic data should be evaluated for fidelity, utility, privacy, and coverage.
- High statistical fidelity can still create privacy proximity risk.
- Rare-case coverage should be reviewed separately from aggregate similarity.
- Synthetic evaluation should be validated against real holdout data whenever possible.
"""

    (OUTPUT_DIR / "python_synthetic_governance_memo.md").write_text(memo)

    print(evaluation_summary)
    print(governance_summary.T)
    print(memo)


if __name__ == "__main__":
    main()
