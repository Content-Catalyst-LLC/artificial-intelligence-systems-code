"""
Data Quality, Bias, and Measurement in Machine Learning Mini-Workflow

This script demonstrates:
- missingness diagnostics
- subgroup representation analysis
- label-noise simulation
- subgroup error-rate comparison
- fairness metric calculation

It is educational and uses synthetic data.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


OUTPUT_DIR = Path("../outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

RANDOM_SEED = 42
rng = np.random.default_rng(RANDOM_SEED)


def build_synthetic_quality_data(n: int = 5000) -> tuple[pd.DataFrame, np.ndarray]:
    """Create synthetic data with representation imbalance, missingness, and label noise."""
    data = pd.DataFrame(
        {
            "unit_id": [f"unit_{i:05d}" for i in range(1, n + 1)],
            "group": rng.choice(["A", "B"], size=n, p=[0.82, 0.18]),
            "feature_signal": rng.normal(0, 1, size=n),
            "measurement_quality": rng.choice(
                ["high", "medium", "low"],
                size=n,
                p=[0.55, 0.30, 0.15],
            ),
        }
    )

    data["measurement_error_sd"] = np.where(data["group"] == "B", 0.45, 0.20)

    data["measured_feature"] = (
        data["feature_signal"]
        + rng.normal(0, data["measurement_error_sd"], size=n)
    )

    logit = -0.10 + 1.20 * data["feature_signal"] + np.where(data["group"] == "B", -0.15, 0)
    probability = 1 / (1 + np.exp(-logit))

    data["true_label"] = rng.binomial(1, probability)

    label_flip_probability = np.where(
        data["measurement_quality"] == "low",
        0.18,
        np.where(data["measurement_quality"] == "medium", 0.08, 0.03),
    )

    label_flip = rng.binomial(1, label_flip_probability)

    data["observed_label"] = np.where(
        label_flip == 1,
        1 - data["true_label"],
        data["true_label"],
    )

    missing_probability = np.where(data["group"] == "B", 0.20, 0.06)
    data["measured_feature_missing"] = rng.binomial(1, missing_probability)

    data.loc[data["measured_feature_missing"] == 1, "measured_feature"] = np.nan

    imputed_feature = data["measured_feature"].fillna(data["measured_feature"].mean())
    score = 1 / (1 + np.exp(-(-0.05 + 1.05 * imputed_feature)))

    data["model_score"] = score
    data["predicted_label"] = (score >= 0.50).astype(int)

    data["prediction_error"] = (
        data["predicted_label"] != data["true_label"]
    ).astype(int)

    return data, label_flip


def summarize_representation(data: pd.DataFrame) -> pd.DataFrame:
    """Summarize representation, missingness, labels, and error rates by group."""
    return (
        data
        .groupby("group")
        .agg(
            units=("unit_id", "count"),
            share=("unit_id", lambda x: len(x) / len(data)),
            missing_rate=("measured_feature_missing", "mean"),
            observed_label_rate=("observed_label", "mean"),
            true_label_rate=("true_label", "mean"),
            positive_prediction_rate=("predicted_label", "mean"),
            error_rate=("prediction_error", "mean"),
        )
        .reset_index()
    )


def compute_quality_diagnostics(data: pd.DataFrame, label_flip: np.ndarray) -> pd.DataFrame:
    """Compute high-level data-quality and fairness diagnostics."""
    positive_rates = (
        data
        .groupby("group")
        .agg(positive_prediction_rate=("predicted_label", "mean"))
        .reset_index()
    )

    rate_a = float(
        positive_rates.loc[
            positive_rates["group"] == "A",
            "positive_prediction_rate"
        ].iloc[0]
    )

    rate_b = float(
        positive_rates.loc[
            positive_rates["group"] == "B",
            "positive_prediction_rate"
        ].iloc[0]
    )

    statistical_parity_difference = rate_a - rate_b

    return pd.DataFrame(
        [
            {"metric": "overall_missing_rate", "value": data["measured_feature_missing"].mean()},
            {"metric": "label_noise_rate", "value": label_flip.mean()},
            {"metric": "statistical_parity_difference_A_minus_B", "value": statistical_parity_difference},
            {"metric": "overall_prediction_error", "value": data["prediction_error"].mean()},
        ]
    )


def main() -> None:
    data, label_flip = build_synthetic_quality_data()
    representation = summarize_representation(data)
    diagnostics = compute_quality_diagnostics(data, label_flip)

    data.to_csv(OUTPUT_DIR / "data_quality_bias_synthetic_data.csv", index=False)
    representation.to_csv(OUTPUT_DIR / "data_quality_bias_group_summary.csv", index=False)
    diagnostics.to_csv(OUTPUT_DIR / "data_quality_bias_diagnostics.csv", index=False)

    print(representation)
    print(diagnostics)


if __name__ == "__main__":
    main()
