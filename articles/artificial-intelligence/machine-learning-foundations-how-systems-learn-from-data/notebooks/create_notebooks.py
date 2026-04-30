#!/usr/bin/env python3
"""
Create advanced Jupyter notebooks for:
Machine Learning Foundations: How Systems Learn from Data
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
    NOTEBOOK_DIR / "01_learning_from_data_and_empirical_risk_lab.ipynb",
    "Learning from Data and Empirical Risk Lab",
    [
        md("""
        ## Purpose

        This lab introduces machine learning as empirical risk minimization.

        Learning goals:

        - Create synthetic examples.
        - Define a simple loss.
        - Compute empirical risk.
        - Interpret learning as parameter selection under uncertainty.
        """),
        code("""
        import numpy as np
        import pandas as pd

        rng = np.random.default_rng(42)

        n = 200
        x = rng.normal(size=n)
        y = 2.0 * x + 0.5 + rng.normal(scale=0.6, size=n)

        candidates = np.linspace(0.5, 3.5, 31)

        rows = []

        for slope in candidates:
            prediction = slope * x + 0.5
            mse = np.mean((y - prediction) ** 2)
            rows.append({"candidate_slope": slope, "empirical_risk_mse": mse})

        risk_table = pd.DataFrame(rows)

        risk_table.loc[risk_table["empirical_risk_mse"].idxmin()]
        """),
        md("""
        ## Interpretation

        A learning system compares candidate parameter settings and selects the one that reduces measured loss on observed data.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "02_representation_features_and_train_test_evaluation_lab.ipynb",
    "Representation, Features, and Train/Test Evaluation Lab",
    [
        md("""
        ## Purpose

        This lab demonstrates a basic supervised learning workflow.

        Learning goals:

        - Build a synthetic classification dataset.
        - Split training and test data.
        - Train a model.
        - Evaluate held-out performance.
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
            n_samples=4000,
            n_features=12,
            n_informative=7,
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
            ("classifier", LogisticRegression(max_iter=1000, random_state=42)),
        ])

        model.fit(X_train, y_train)

        score = model.predict_proba(X_test)[:, 1]
        prediction = (score >= 0.50).astype(int)

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

        Train/test separation is a basic guard against confusing memorization with generalization.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "03_calibration_uncertainty_and_error_analysis_lab.ipynb",
    "Calibration, Uncertainty, and Error Analysis Lab",
    [
        md("""
        ## Purpose

        This lab examines calibration and grouped error diagnostics.

        Aggregate performance can hide overconfidence and uneven failure patterns.
        """),
        code("""
        import numpy as np
        import pandas as pd

        rng = np.random.default_rng(42)

        n = 2000

        frame = pd.DataFrame({
            "group": rng.choice(["A", "B", "C"], size=n, p=[0.50, 0.30, 0.20]),
            "score": rng.beta(2.0, 3.0, size=n),
        })

        frame["target"] = rng.binomial(1, frame["score"])
        frame["prediction"] = (frame["score"] >= 0.50).astype(int)
        frame["error"] = frame["prediction"] != frame["target"]

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

        grouped = (
            frame
            .groupby("group", as_index=False)
            .agg(
                sample_size=("error", "size"),
                classification_error_rate=("error", "mean"),
                base_rate=("target", "mean"),
                selection_rate=("prediction", "mean"),
            )
        )

        calibration, grouped
        """),
        md("""
        ## Interpretation

        Calibration asks whether probability scores mean what they claim. Grouped diagnostics ask whether model failures are evenly distributed or systematically concentrated.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "04_distribution_shift_feedback_loops_and_governance_lab.ipynb",
    "Distribution Shift, Feedback Loops, and Governance Lab",
    [
        md("""
        ## Purpose

        This lab simulates distribution shift and connects monitoring to governance.

        Learning goals:

        - Compare reference and current feature distributions.
        - Compute a simple drift metric.
        - Document governance questions triggered by drift.
        """),
        code("""
        import numpy as np
        import pandas as pd

        rng = np.random.default_rng(42)

        reference = rng.normal(loc=0.0, scale=1.0, size=5000)
        current_mild = rng.normal(loc=0.30, scale=1.05, size=5000)
        current_severe = rng.normal(loc=0.90, scale=1.25, size=5000)

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
        code("""
        governance_checklist = pd.DataFrame([
            {"layer": "data", "question": "What changed in the data-generating process?"},
            {"layer": "model", "question": "Does current performance still match validation evidence?"},
            {"layer": "decision", "question": "Are outputs still appropriate for operational use?"},
            {"layer": "monitoring", "question": "Who reviews drift alerts and how quickly?"},
            {"layer": "governance", "question": "Should the model be retrained, constrained, paused, or retired?"},
        ])

        governance_checklist
        """),
        md("""
        ## Interpretation

        Drift metrics are signals, not governance by themselves. Responsible systems define review procedures, escalation rules, and human accountability before deployment.
        """),
    ],
)
