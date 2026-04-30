#!/usr/bin/env python3
"""
Create advanced Jupyter notebooks for:
Supervised, Unsupervised, and Reinforcement Learning
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
    NOTEBOOK_DIR / "01_supervised_learning_classification_lab.ipynb",
    "Supervised Learning Classification Lab",
    [
        md("""
        ## Purpose

        This lab introduces supervised learning as conditional estimation from labeled examples.

        Learning goals:

        - Build a synthetic classification dataset.
        - Train a supervised model.
        - Evaluate held-out performance.
        - Interpret label quality as part of system trust.
        """),
        code("""
        import numpy as np
        import pandas as pd

        from sklearn.datasets import make_classification
        from sklearn.linear_model import LogisticRegression
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
        from sklearn.model_selection import train_test_split
        from sklearn.pipeline import Pipeline
        from sklearn.preprocessing import StandardScaler

        X, y = make_classification(
            n_samples=2000,
            n_features=8,
            n_informative=5,
            n_redundant=1,
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

        prediction = model.predict(X_test)

        metrics = pd.DataFrame([{
            "accuracy": accuracy_score(y_test, prediction),
            "precision": precision_score(y_test, prediction, zero_division=0),
            "recall": recall_score(y_test, prediction, zero_division=0),
            "f1": f1_score(y_test, prediction, zero_division=0),
        }])

        metrics
        """),
        md("""
        ## Interpretation

        Supervised learning depends on labels. Evaluation should ask whether those labels are valid, representative, current, and aligned with real-world use.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "02_unsupervised_learning_clustering_and_representation_lab.ipynb",
    "Unsupervised Learning, Clustering, and Representation Lab",
    [
        md("""
        ## Purpose

        This lab introduces unsupervised learning as structure discovery from unlabeled data.

        Learning goals:

        - Cluster synthetic observations.
        - Compare discovered clusters with hidden reference labels.
        - Understand why unsupervised structure requires interpretation.
        """),
        code("""
        import numpy as np
        import pandas as pd

        from sklearn.datasets import make_blobs
        from sklearn.cluster import KMeans
        from sklearn.decomposition import PCA
        from sklearn.metrics import adjusted_rand_score

        X, true_group = make_blobs(
            n_samples=1500,
            centers=3,
            n_features=6,
            cluster_std=1.4,
            random_state=42,
        )

        cluster_model = KMeans(n_clusters=3, random_state=42, n_init="auto")
        predicted_cluster = cluster_model.fit_predict(X)

        ari = adjusted_rand_score(true_group, predicted_cluster)

        pca = PCA(n_components=2, random_state=42)
        coordinates = pca.fit_transform(X)

        result = pd.DataFrame({
            "pc1": coordinates[:, 0],
            "pc2": coordinates[:, 1],
            "predicted_cluster": predicted_cluster,
            "hidden_reference_group": true_group,
        })

        pd.DataFrame([{
            "adjusted_rand_index": ari,
            "explained_variance_pc1": pca.explained_variance_ratio_[0],
            "explained_variance_pc2": pca.explained_variance_ratio_[1],
        }])
        """),
        md("""
        ## Interpretation

        In real unsupervised learning, hidden reference labels may not exist. That makes domain interpretation, stability testing, and downstream validation essential.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "03_reinforcement_learning_q_learning_lab.ipynb",
    "Reinforcement Learning and Q-Learning Lab",
    [
        md("""
        ## Purpose

        This lab introduces reinforcement learning through a tiny tabular Q-learning example.

        Learning goals:

        - Understand states, actions, rewards, and transitions.
        - Update a Q-table from experience.
        - Interpret reward design as a governance problem.
        """),
        code("""
        import numpy as np
        import pandas as pd

        states = [0, 1, 2]
        actions = [0, 1]

        q = np.zeros((len(states), len(actions)))

        alpha = 0.30
        gamma = 0.90

        experience = [
            (0, 1, 0.0, 1),
            (1, 1, 1.0, 2),
            (2, 0, 0.0, 2),
            (0, 0, 0.2, 0),
            (1, 0, -0.1, 0),
        ]

        rows = []

        for step, (state, action, reward, next_state) in enumerate(experience):
            old_value = q[state, action]
            target = reward + gamma * np.max(q[next_state])
            q[state, action] = old_value + alpha * (target - old_value)

            rows.append({
                "step": step,
                "state": state,
                "action": action,
                "reward": reward,
                "next_state": next_state,
                "old_q": old_value,
                "target": target,
                "new_q": q[state, action],
            })

        updates = pd.DataFrame(rows)
        q_table = pd.DataFrame(q, columns=["action_0", "action_1"])

        updates, q_table
        """),
        md("""
        ## Governance Extension

        A reward is not neutral. In real systems, reward functions encode values, incentives, and tradeoffs. Poor reward design can produce unintended behavior.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "04_self_supervised_and_hybrid_learning_governance_lab.ipynb",
    "Self-Supervised and Hybrid Learning Governance Lab",
    [
        md("""
        ## Purpose

        This lab introduces hybrid learning systems.

        Modern AI systems often combine self-supervised pretraining, supervised fine-tuning, human feedback, and reinforcement-style optimization.
        """),
        code("""
        import pandas as pd

        pipeline = pd.DataFrame([
            {
                "stage": "self_supervised_pretraining",
                "signal": "structure inside unlabeled data",
                "objective": "predict masked or related content",
                "governance_risk": "opaque data provenance and representation bias",
            },
            {
                "stage": "supervised_fine_tuning",
                "signal": "labeled examples or demonstrations",
                "objective": "imitate desired outputs",
                "governance_risk": "label bias and annotator disagreement",
            },
            {
                "stage": "reward_modeling",
                "signal": "human preferences",
                "objective": "learn preference score",
                "governance_risk": "preference aggregation and value mismatch",
            },
            {
                "stage": "policy_optimization",
                "signal": "reward estimates",
                "objective": "maximize learned reward",
                "governance_risk": "reward hacking and overoptimization",
            },
        ])

        pipeline
        """),
        md("""
        ## Interpretation

        Hybrid systems require stage-by-stage documentation.

        Ask:

        - What data shaped each stage?
        - What objective was optimized?
        - What feedback was used?
        - What risks were introduced?
        - What monitoring is required after deployment?
        """),
    ],
)
