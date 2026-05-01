"""
Model Validation, Benchmarking, and Generalization Theory Mini-Workflow

This script demonstrates:
- train, validation, and test evaluation
- generalization-gap diagnostics
- distribution-shift performance degradation
- calibration binning
- expected calibration error

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


def build_evaluation_data(n: int = 4000) -> pd.DataFrame:
    """Create synthetic model-evaluation data."""
    evaluation = pd.DataFrame(
        {
            "example_id": [f"ex_{i:05d}" for i in range(1, n + 1)],
            "split": rng.choice(
                ["train", "validation", "test", "shifted_deployment"],
                size=n,
                p=[0.45, 0.20, 0.20, 0.15],
            ),
        }
    )

    base_difficulty = rng.beta(2.0, 5.0, size=n)

    shift_penalty = np.where(
        evaluation["split"] == "shifted_deployment",
        0.18,
        0.0,
    )

    evaluation["true_label"] = rng.binomial(1, 0.45, size=n)

    signal_strength = np.where(
        evaluation["true_label"] == 1,
        0.70,
        0.30,
    )

    noise = rng.normal(0, 0.14 + shift_penalty, size=n)

    evaluation["predicted_probability"] = np.clip(
        signal_strength - 0.20 * base_difficulty + noise,
        0.01,
        0.99,
    )

    evaluation["prediction"] = (
        evaluation["predicted_probability"] >= 0.50
    ).astype(int)

    evaluation["correct"] = (
        evaluation["prediction"] == evaluation["true_label"]
    ).astype(int)

    return evaluation


def summarize_performance(evaluation: pd.DataFrame) -> pd.DataFrame:
    """Summarize model performance by split."""
    return (
        evaluation
        .groupby("split")
        .agg(
            examples=("example_id", "count"),
            accuracy=("correct", "mean"),
            mean_confidence=("predicted_probability", "mean"),
            mean_positive_rate=("prediction", "mean"),
        )
        .reset_index()
    )


def compute_calibration(evaluation: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Compute calibration bins and expected calibration error by split."""
    data = evaluation.copy()
    data["confidence_bin"] = pd.cut(
        data["predicted_probability"],
        bins=np.linspace(0, 1, 11),
        include_lowest=True,
    )

    calibration = (
        data
        .groupby(["split", "confidence_bin"], observed=False)
        .agg(
            n=("example_id", "count"),
            accuracy=("correct", "mean"),
            confidence=("predicted_probability", "mean"),
        )
        .reset_index()
    )

    calibration["abs_calibration_gap"] = (
        calibration["accuracy"] - calibration["confidence"]
    ).abs()

    ece_by_split = (
        calibration
        .dropna()
        .assign(weight=lambda df: df["n"] / df.groupby("split")["n"].transform("sum"))
        .assign(weighted_gap=lambda df: df["weight"] * df["abs_calibration_gap"])
        .groupby("split")
        .agg(expected_calibration_error=("weighted_gap", "sum"))
        .reset_index()
    )

    return calibration, ece_by_split


def compute_diagnostics(summary: pd.DataFrame) -> pd.DataFrame:
    """Compute generalization and shift gaps."""
    train_accuracy = float(summary.loc[summary["split"] == "train", "accuracy"].iloc[0])
    test_accuracy = float(summary.loc[summary["split"] == "test", "accuracy"].iloc[0])
    shift_accuracy = float(summary.loc[summary["split"] == "shifted_deployment", "accuracy"].iloc[0])

    return pd.DataFrame(
        [
            {
                "metric": "generalization_gap_train_minus_test",
                "value": train_accuracy - test_accuracy,
            },
            {
                "metric": "shift_gap_test_minus_shifted_deployment",
                "value": test_accuracy - shift_accuracy,
            },
        ]
    )


def main() -> None:
    evaluation = build_evaluation_data()
    summary = summarize_performance(evaluation)
    calibration, ece_by_split = compute_calibration(evaluation)
    diagnostics = compute_diagnostics(summary)

    evaluation.to_csv(OUTPUT_DIR / "model_validation_evaluation_data.csv", index=False)
    summary.to_csv(OUTPUT_DIR / "model_validation_performance_summary.csv", index=False)
    calibration.to_csv(OUTPUT_DIR / "model_validation_calibration_bins.csv", index=False)
    ece_by_split.to_csv(OUTPUT_DIR / "model_validation_ece_by_split.csv", index=False)
    diagnostics.to_csv(OUTPUT_DIR / "model_validation_diagnostics.csv", index=False)

    print(summary)
    print(ece_by_split)
    print(diagnostics)


if __name__ == "__main__":
    main()
