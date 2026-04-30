#!/usr/bin/env python3
"""
Create advanced Jupyter notebooks for:
Deep Learning Systems: Representation, Scale, and Generalization
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
    NOTEBOOK_DIR / "01_representation_geometry_and_manifold_intuition_lab.ipynb",
    "Representation Geometry and Manifold Intuition Lab",
    [
        md("""
        ## Purpose

        This lab introduces representation geometry.

        Deep learning systems learn transformations that reorganize high-dimensional data into useful representation spaces.
        """),
        code("""
        import numpy as np
        import pandas as pd

        from sklearn.datasets import make_classification
        from sklearn.decomposition import PCA

        X, y = make_classification(
            n_samples=3000,
            n_features=50,
            n_informative=12,
            n_redundant=8,
            class_sep=1.2,
            random_state=42,
        )

        pca = PCA(n_components=2, random_state=42)
        Z = pca.fit_transform(X)

        representation = pd.DataFrame({
            "z1": Z[:, 0],
            "z2": Z[:, 1],
            "target": y,
        })

        summary = pd.DataFrame([{
            "pc1_explained_variance": pca.explained_variance_ratio_[0],
            "pc2_explained_variance": pca.explained_variance_ratio_[1],
            "total_explained_variance": pca.explained_variance_ratio_.sum(),
        }])

        summary
        """),
        md("""
        ## Interpretation

        PCA is not deep learning, but it provides a transparent way to see the idea of representation: data can be transformed into spaces where structure becomes easier to analyze.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "02_scaling_laws_and_compute_tradeoffs_lab.ipynb",
    "Scaling Laws and Compute Tradeoffs Lab",
    [
        md("""
        ## Purpose

        This lab simulates scaling-law behavior.

        Learning goals:

        - Model loss as a power-law function of scale.
        - Compare model-size and data-size tradeoffs.
        - Interpret scale as a systems variable.
        """),
        code("""
        import numpy as np
        import pandas as pd

        scale = np.logspace(2, 8, 100)

        def scaling_loss(scale, a=2.0, alpha=0.08, b=0.9):
            return a * scale ** (-alpha) + b

        curve = pd.DataFrame({
            "scale": scale,
            "simulated_loss": scaling_loss(scale),
        })

        curve.head()
        """),
        code("""
        budgets = pd.DataFrame([
            {"model_parameters": 1e7, "training_tokens": 1e9},
            {"model_parameters": 1e8, "training_tokens": 1e10},
            {"model_parameters": 1e9, "training_tokens": 1e11},
            {"model_parameters": 1e10, "training_tokens": 1e12},
        ])

        budgets["simplified_compute_proxy"] = budgets["model_parameters"] * budgets["training_tokens"]

        budgets
        """),
        md("""
        ## Interpretation

        Scaling is not only a model-size question. Compute-optimal training depends on balancing model size, data, and training budget.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "03_overparameterization_double_descent_and_generalization_lab.ipynb",
    "Overparameterization, Double Descent, and Generalization Lab",
    [
        md("""
        ## Purpose

        This lab simulates a double-descent-like diagnostic curve.

        The values are synthetic. The goal is conceptual: test error can behave non-monotonically as model capacity changes.
        """),
        code("""
        import numpy as np
        import pandas as pd

        capacity = np.linspace(50, 5000, 120)

        train_error = 0.45 * np.exp(-capacity / 800) + 0.02

        interpolation_peak = 0.07 * np.exp(-((capacity - 950) ** 2) / (2 * 230 ** 2))
        test_error = 0.30 * np.exp(-capacity / 1500) + 0.08 + interpolation_peak

        diagnostics = pd.DataFrame({
            "capacity": capacity,
            "train_error": train_error,
            "test_error": test_error,
            "generalization_gap": test_error - train_error,
        })

        diagnostics.loc[diagnostics["test_error"].idxmin()]
        """),
        md("""
        ## Interpretation

        The double descent idea warns against using simple capacity intuition without considering data, optimization, architecture, and evaluation design.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "04_attention_loss_landscapes_and_governance_lab.ipynb",
    "Attention, Loss Landscapes, and Governance Lab",
    [
        md("""
        ## Purpose

        This lab connects attention intuition, optimization geometry, and governance documentation.

        It uses lightweight synthetic examples rather than large model training.
        """),
        code("""
        import numpy as np
        import pandas as pd

        rng = np.random.default_rng(42)

        tokens = ["deep", "learning", "systems", "generalize"]
        d_model = 8

        H = rng.normal(size=(len(tokens), d_model))

        Q = H
        K = H
        V = H

        scores = Q @ K.T / np.sqrt(d_model)

        def softmax(x):
            shifted = x - x.max(axis=1, keepdims=True)
            exp = np.exp(shifted)
            return exp / exp.sum(axis=1, keepdims=True)

        attention = softmax(scores)

        pd.DataFrame(attention, index=tokens, columns=tokens)
        """),
        code("""
        governance_checklist = pd.DataFrame([
            {"layer": "data", "audit_question": "What datasets shaped the learned representation?"},
            {"layer": "architecture", "audit_question": "What inductive biases are encoded in the model design?"},
            {"layer": "optimization", "audit_question": "What optimizer, schedule, and compute budget were used?"},
            {"layer": "evaluation", "audit_question": "Which robustness, calibration, and subgroup tests were performed?"},
            {"layer": "deployment", "audit_question": "How is drift, misuse, or degradation monitored?"},
        ])

        governance_checklist
        """),
        md("""
        ## Interpretation

        Attention helps models route information, but governance requires more than inspecting attention weights. Responsible deep learning systems require auditability across data, training, evaluation, deployment, and monitoring.
        """),
    ],
)
