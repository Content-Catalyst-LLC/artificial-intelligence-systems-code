#!/usr/bin/env python3
"""
Create advanced Jupyter notebooks for:
Model Validation, Benchmarking, and Generalization Theory
"""

from __future__ import annotations

import json
from pathlib import Path
from textwrap import dedent


NOTEBOOK_DIR = Path(".")


def md(text: str) -> dict:
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": dedent(text).strip().splitlines(keepends=True),
    }


def code(text: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": dedent(text).strip().splitlines(keepends=True),
    }


def notebook(title: str, cells: list[dict]) -> dict:
    return {
        "cells": [
            {"cell_type": "markdown", "metadata": {}, "source": [f"# {title}\n"]},
            *cells,
        ],
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.x"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def write(path: Path, title: str, cells: list[dict]) -> None:
    path.write_text(json.dumps(notebook(title, cells), indent=2), encoding="utf-8")
    print(f"created {path}")


validation_setup = """
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

n = 4000

evaluation = pd.DataFrame({
    "example_id": [f"ex_{i:05d}" for i in range(1, n + 1)],
    "split": rng.choice(
        ["train", "validation", "test", "shifted_deployment"],
        size=n,
        p=[0.45, 0.20, 0.20, 0.15],
    ),
})

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

evaluation["prediction"] = (evaluation["predicted_probability"] >= 0.50).astype(int)
evaluation["correct"] = (evaluation["prediction"] == evaluation["true_label"]).astype(int)

evaluation.head()
"""

write(
    NOTEBOOK_DIR / "01_empirical_risk_generalization_gap_and_validation_splits_lab.ipynb",
    "Empirical Risk, Generalization Gap, and Validation Splits Lab",
    [
        md("""
        ## Purpose

        This lab compares training, validation, test, and shifted-deployment performance.
        """),
        code(validation_setup),
        code("""
summary = (
    evaluation
    .groupby("split")
    .agg(
        examples=("example_id", "count"),
        accuracy=("correct", "mean"),
        mean_confidence=("predicted_probability", "mean"),
    )
    .reset_index()
)

train_accuracy = summary.loc[summary["split"] == "train", "accuracy"].iloc[0]
test_accuracy = summary.loc[summary["split"] == "test", "accuracy"].iloc[0]
shift_accuracy = summary.loc[summary["split"] == "shifted_deployment", "accuracy"].iloc[0]

diagnostics = pd.DataFrame([
    {"metric": "train_minus_test_gap", "value": train_accuracy - test_accuracy},
    {"metric": "test_minus_shifted_deployment_gap", "value": test_accuracy - shift_accuracy},
])

summary, diagnostics
        """),
        md("""
        ## Interpretation

        Validation asks whether apparent performance survives outside the training sample and under shifted deployment conditions.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "02_cross_validation_resampling_and_model_selection_lab.ipynb",
    "Cross-Validation, Resampling, and Model Selection Lab",
    [
        md("""
        ## Purpose

        This lab simulates cross-validation performance across models and folds.
        """),
        code("""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

models = ["baseline_linear", "random_forest", "gradient_boosted", "neural_network"]
folds = [f"fold_{i}" for i in range(1, 11)]

rows = []

for model in models:
    base = {
        "baseline_linear": 0.74,
        "random_forest": 0.81,
        "gradient_boosted": 0.84,
        "neural_network": 0.85,
    }[model]

    for fold in folds:
        rows.append({
            "model": model,
            "fold": fold,
            "validation_accuracy": float(np.clip(rng.normal(base, 0.025), 0.50, 0.99)),
        })

cv_results = pd.DataFrame(rows)

cv_summary = (
    cv_results
    .groupby("model")
    .agg(
        mean_accuracy=("validation_accuracy", "mean"),
        sd_accuracy=("validation_accuracy", "std"),
        min_accuracy=("validation_accuracy", "min"),
        max_accuracy=("validation_accuracy", "max"),
    )
    .reset_index()
    .sort_values("mean_accuracy", ascending=False)
)

cv_summary
        """),
        md("""
        ## Interpretation

        Cross-validation summarizes expected performance and variation across folds, but fold design must match data structure.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "03_calibration_uncertainty_and_distribution_shift_lab.ipynb",
    "Calibration, Uncertainty, and Distribution Shift Lab",
    [
        md("""
        ## Purpose

        This lab computes confidence-bin calibration and expected calibration error.
        """),
        code(validation_setup),
        code("""
evaluation["confidence_bin"] = pd.cut(
    evaluation["predicted_probability"],
    bins=np.linspace(0, 1, 11),
    include_lowest=True,
)

calibration = (
    evaluation
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

ece_by_split
        """),
        md("""
        ## Interpretation

        Calibration evaluates whether model confidence matches empirical correctness, especially under shifted deployment.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "04_benchmark_saturation_external_validation_and_governance_lab.ipynb",
    "Benchmark Saturation, External Validation, and Governance Lab",
    [
        md("""
        ## Purpose

        This lab compares public benchmark scores with external and shifted-deployment scores.
        """),
        code("""
import numpy as np
import pandas as pd

benchmark_results = pd.DataFrame({
    "model": ["baseline_linear", "random_forest", "gradient_boosted", "neural_network"],
    "public_benchmark_score": [0.78, 0.86, 0.89, 0.90],
    "external_validation_score": [0.74, 0.80, 0.82, 0.79],
    "shifted_deployment_score": [0.70, 0.76, 0.77, 0.72],
})

benchmark_results["external_gap"] = (
    benchmark_results["public_benchmark_score"]
    - benchmark_results["external_validation_score"]
)

benchmark_results["shift_gap"] = (
    benchmark_results["external_validation_score"]
    - benchmark_results["shifted_deployment_score"]
)

top_scores = benchmark_results["public_benchmark_score"].sort_values(ascending=False).head(3)

benchmark_saturation_indicator = 1 - (
    top_scores.std() / benchmark_results["public_benchmark_score"].std()
)

governance_review = pd.DataFrame([
    {
        "area": "intended_use",
        "question": "Is the benchmark aligned with the deployment task?",
        "status": "partial",
        "owner": "Evaluation",
    },
    {
        "area": "external_validation",
        "question": "Has the model been tested outside the benchmark environment?",
        "status": "partial",
        "owner": "Validation",
    },
    {
        "area": "calibration",
        "question": "Is confidence reliable under distribution shift?",
        "status": "missing",
        "owner": "Model Risk",
    },
    {
        "area": "monitoring",
        "question": "Is post-deployment degradation monitored?",
        "status": "partial",
        "owner": "MLOps",
    },
])

benchmark_results, benchmark_saturation_indicator, governance_review
        """),
        md("""
        ## Interpretation

        Public benchmark performance should be interpreted alongside external validation, shift testing, calibration, and governance documentation.
        """),
    ],
)
