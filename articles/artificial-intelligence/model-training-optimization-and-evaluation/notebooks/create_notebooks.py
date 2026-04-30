#!/usr/bin/env python3
"""
Create advanced Jupyter notebooks for:
Model Training, Optimization, and Evaluation
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
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [f"# {title}\n"],
            },
            *cells,
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "version": "3.x",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def write(path: Path, title: str, cells: list[dict]) -> None:
    path.write_text(json.dumps(notebook(title, cells), indent=2), encoding="utf-8")
    print(f"created {path}")


write(
    NOTEBOOK_DIR / "01_empirical_risk_and_gradient_descent_lab.ipynb",
    "Empirical Risk and Gradient Descent Lab",
    [
        md("""
        ## Purpose

        This lab introduces empirical risk minimization and gradient descent with a simple quadratic loss.

        Learning goals:

        - Define a loss function.
        - Compute gradients.
        - Run iterative parameter updates.
        - Interpret optimization as a trajectory through parameter space.
        """),
        code("""
        import numpy as np
        import pandas as pd

        theta = 5.0
        learning_rate = 0.1

        rows = []

        def loss(theta):
            return (theta - 1.5) ** 2

        def grad(theta):
            return 2 * (theta - 1.5)

        for step in range(30):
            rows.append({"step": step, "theta": theta, "loss": loss(theta)})
            theta = theta - learning_rate * grad(theta)

        trajectory = pd.DataFrame(rows)
        trajectory.tail()
        """),
        md("""
        ## Interpretation

        Even this toy example shows the essential logic of training: define error, compute direction, update parameters, and track improvement.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "02_training_validation_testing_and_metrics_lab.ipynb",
    "Training, Validation, Testing, and Metrics Lab",
    [
        md("""
        ## Purpose

        This lab builds a full train/test evaluation workflow with synthetic data.

        The goal is to separate model fitting from held-out evaluation.
        """),
        code("""
        import numpy as np
        import pandas as pd

        from sklearn.datasets import make_classification
        from sklearn.linear_model import LogisticRegression
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
        from sklearn.model_selection import train_test_split
        from sklearn.pipeline import Pipeline
        from sklearn.preprocessing import StandardScaler

        X, y = make_classification(
            n_samples=5000,
            n_features=10,
            n_informative=6,
            n_redundant=2,
            weights=[0.65, 0.35],
            random_state=42,
        )

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.30,
            stratify=y,
            random_state=42,
        )

        model = Pipeline([
            ("scale", StandardScaler()),
            ("clf", LogisticRegression(max_iter=1000, random_state=42)),
        ])

        model.fit(X_train, y_train)

        score = model.predict_proba(X_test)[:, 1]
        prediction = (score >= 0.5).astype(int)

        metrics = pd.DataFrame([{
            "accuracy": accuracy_score(y_test, prediction),
            "precision": precision_score(y_test, prediction, zero_division=0),
            "recall": recall_score(y_test, prediction, zero_division=0),
            "f1": f1_score(y_test, prediction, zero_division=0),
            "roc_auc": roc_auc_score(y_test, score),
        }])

        metrics
        """),
        md("""
        ## Interpretation

        Metrics are not self-interpreting. Each metric emphasizes different error tradeoffs.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "03_calibration_thresholds_and_decision_diagnostics_lab.ipynb",
    "Calibration, Thresholds, and Decision Diagnostics Lab",
    [
        md("""
        ## Purpose

        This lab explores calibration and threshold choice.

        A model may rank cases well but still produce poorly calibrated probabilities.
        """),
        code("""
        import numpy as np
        import pandas as pd

        rng = np.random.default_rng(42)

        n = 2000
        score = rng.beta(2.2, 3.0, size=n)
        target = rng.binomial(1, score)

        frame = pd.DataFrame({"score": score, "target": target})

        frame["confidence_bin"] = pd.cut(
            frame["score"],
            bins=np.linspace(0, 1, 11),
            include_lowest=True,
        )

        calibration = (
            frame
            .groupby("confidence_bin", observed=True)
            .agg(
                n=("target", "size"),
                mean_confidence=("score", "mean"),
                empirical_rate=("target", "mean"),
            )
            .reset_index()
        )

        calibration["absolute_gap"] = (
            calibration["mean_confidence"] - calibration["empirical_rate"]
        ).abs()

        ece = (
            calibration["n"] / calibration["n"].sum() * calibration["absolute_gap"]
        ).sum()

        calibration, ece
        """),
        code("""
        threshold_rows = []

        for threshold in np.linspace(0.1, 0.9, 9):
            prediction = (frame["score"] >= threshold).astype(int)
            threshold_rows.append({
                "threshold": threshold,
                "selection_rate": prediction.mean(),
                "positive_predictive_value": frame.loc[prediction == 1, "target"].mean(),
            })

        pd.DataFrame(threshold_rows)
        """),
        md("""
        ## Governance Question

        A threshold is not just a technical parameter. It often encodes an operational policy choice.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "04_distribution_shift_monitoring_and_governance_lab.ipynb",
    "Distribution Shift, Monitoring, and Governance Lab",
    [
        md("""
        ## Purpose

        This lab simulates distribution shift between training and deployment data.

        Learning goals:

        - Compare reference and current feature distributions.
        - Compute a simple population stability index.
        - Interpret drift as a monitoring signal, not a complete governance process.
        """),
        code("""
        import numpy as np
        import pandas as pd

        rng = np.random.default_rng(42)

        reference = rng.normal(loc=0.0, scale=1.0, size=5000)
        current_mild = rng.normal(loc=0.35, scale=1.05, size=5000)
        current_severe = rng.normal(loc=1.00, scale=1.25, size=5000)

        def population_stability_index(reference_values, current_values, bins=10):
            reference_counts, bin_edges = np.histogram(reference_values, bins=bins)
            current_counts, _ = np.histogram(current_values, bins=bin_edges)

            reference_pct = reference_counts / max(reference_counts.sum(), 1)
            current_pct = current_counts / max(current_counts.sum(), 1)

            epsilon = 1e-6
            return np.sum(
                (current_pct - reference_pct)
                * np.log((current_pct + epsilon) / (reference_pct + epsilon))
            )

        drift = pd.DataFrame([
            {
                "comparison": "reference_vs_mild_shift",
                "psi": population_stability_index(reference, current_mild),
            },
            {
                "comparison": "reference_vs_severe_shift",
                "psi": population_stability_index(reference, current_severe),
            },
        ])

        drift
        """),
        md("""
        ## Governance Questions

        - What threshold triggers review?
        - Who receives the alert?
        - Is retraining automatic or governed?
        - What data is approved for retraining?
        - How are model versions and rollback plans documented?
        """),
    ],
)
