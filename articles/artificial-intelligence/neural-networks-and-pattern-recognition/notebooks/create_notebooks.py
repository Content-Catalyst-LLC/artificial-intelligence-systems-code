#!/usr/bin/env python3
"""
Create advanced Jupyter notebooks for:
Neural Networks and Pattern Recognition
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
    NOTEBOOK_DIR / "01_mlp_pattern_recognition_lab.ipynb",
    "MLP Pattern Recognition Lab",
    [
        md("""
        ## Purpose

        This lab introduces neural networks as nonlinear pattern-recognition systems.

        Learning goals:

        - Build a synthetic nonlinear dataset.
        - Train a multilayer perceptron.
        - Evaluate held-out performance.
        - Interpret neural networks as learned function approximators.
        """),
        code("""
        import numpy as np
        import pandas as pd

        from sklearn.datasets import make_moons
        from sklearn.metrics import accuracy_score, f1_score
        from sklearn.model_selection import train_test_split
        from sklearn.neural_network import MLPClassifier
        from sklearn.pipeline import Pipeline
        from sklearn.preprocessing import StandardScaler

        X, y = make_moons(
            n_samples=2500,
            noise=0.25,
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
            (
                "mlp",
                MLPClassifier(
                    hidden_layer_sizes=(32, 16),
                    activation="relu",
                    solver="adam",
                    max_iter=600,
                    random_state=42,
                ),
            ),
        ])

        model.fit(X_train, y_train)

        prediction = model.predict(X_test)

        metrics = pd.DataFrame([{
            "accuracy": accuracy_score(y_test, prediction),
            "f1": f1_score(y_test, prediction),
        }])

        metrics
        """),
        md("""
        ## Interpretation

        A neural network learns a nonlinear decision function. Its pattern-recognition ability depends on representation, optimization, and evaluation.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "02_activation_functions_and_backpropagation_lab.ipynb",
    "Activation Functions and Backpropagation Lab",
    [
        md("""
        ## Purpose

        This lab introduces activation functions and gradient-based learning using lightweight NumPy examples.

        Learning goals:

        - Compare common activation functions.
        - Understand why nonlinearity matters.
        - See the structure of a simple gradient update.
        """),
        code("""
        import numpy as np
        import pandas as pd

        z = np.linspace(-4, 4, 17)

        def sigmoid(z):
            return 1 / (1 + np.exp(-z))

        def tanh(z):
            return np.tanh(z)

        def relu(z):
            return np.maximum(0, z)

        activations = pd.DataFrame({
            "z": z,
            "sigmoid": sigmoid(z),
            "tanh": tanh(z),
            "relu": relu(z),
        })

        activations
        """),
        code("""
        # A tiny one-parameter gradient descent example.
        theta = 4.0
        learning_rate = 0.1

        rows = []

        def loss(theta):
            return (theta - 1.5) ** 2

        def gradient(theta):
            return 2 * (theta - 1.5)

        for step in range(20):
            rows.append({
                "step": step,
                "theta": theta,
                "loss": loss(theta),
                "gradient": gradient(theta),
            })
            theta = theta - learning_rate * gradient(theta)

        pd.DataFrame(rows).tail()
        """),
        md("""
        ## Interpretation

        Backpropagation in a real network applies this same principle through many composed layers using the chain rule.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "03_representation_geometry_and_latent_space_lab.ipynb",
    "Representation Geometry and Latent Space Lab",
    [
        md("""
        ## Purpose

        This lab explores latent-space geometry.

        Neural networks learn representations that can make patterns easier to separate, compare, retrieve, or classify.
        """),
        code("""
        import numpy as np
        import pandas as pd

        from sklearn.datasets import make_classification
        from sklearn.decomposition import PCA
        from sklearn.preprocessing import StandardScaler

        X, y = make_classification(
            n_samples=2500,
            n_features=20,
            n_informative=8,
            n_redundant=4,
            class_sep=1.2,
            random_state=42,
        )

        X_scaled = StandardScaler().fit_transform(X)

        pca = PCA(n_components=2, random_state=42)
        Z = pca.fit_transform(X_scaled)

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

        PCA is not a neural network, but it gives a transparent view of representation geometry. Neural networks learn more flexible transformations of this kind.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "04_generalization_interpretability_and_governance_lab.ipynb",
    "Generalization, Interpretability, and Governance Lab",
    [
        md("""
        ## Purpose

        This lab simulates grouped error diagnostics for neural-network systems.

        The central point: aggregate accuracy can hide uneven performance across groups and deployment conditions.
        """),
        code("""
        import numpy as np
        import pandas as pd

        rng = np.random.default_rng(42)
        n = 1800

        data = pd.DataFrame({
            "group": rng.choice(["A", "B", "C"], size=n, p=[0.50, 0.30, 0.20]),
            "condition": rng.choice(["training_like", "moderate_shift", "high_shift"], size=n),
            "target": rng.binomial(1, 0.45, size=n),
        })

        condition_error = data["condition"].map({
            "training_like": 0.08,
            "moderate_shift": 0.15,
            "high_shift": 0.26,
        })

        group_multiplier = data["group"].map({
            "A": 1.00,
            "B": 1.15,
            "C": 1.35,
        })

        error_probability = np.minimum(condition_error * group_multiplier, 0.90)

        is_error = rng.binomial(1, error_probability)

        data["prediction"] = np.where(
            is_error == 1,
            1 - data["target"],
            data["target"],
        )

        data["error"] = data["prediction"] != data["target"]

        summary = (
            data
            .groupby(["group", "condition"], as_index=False)
            .agg(
                sample_size=("error", "size"),
                classification_error_rate=("error", "mean"),
            )
        )

        summary
        """),
        code("""
        governance_checklist = pd.DataFrame([
            {"layer": "data", "question": "What data shaped the learned patterns?"},
            {"layer": "labels", "question": "Are targets valid, biased, noisy, or incomplete?"},
            {"layer": "architecture", "question": "What inductive biases are built into the network?"},
            {"layer": "optimization", "question": "What objective and training procedure shaped parameters?"},
            {"layer": "evaluation", "question": "How does performance vary across conditions?"},
            {"layer": "deployment", "question": "How are drift, errors, and user harms monitored?"},
        ])

        governance_checklist
        """),
        md("""
        ## Interpretation

        Interpretability tools are useful, but governance also requires documentation, evaluation, monitoring, and human oversight.
        """),
    ],
)
