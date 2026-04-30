"""
Supervised, Unsupervised, and Reinforcement Learning Mini-Workflow

This script demonstrates:
- supervised classification
- unsupervised clustering
- a tiny Q-learning update table

It is educational and does not require private data.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.datasets import make_classification
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, adjusted_rand_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


OUTPUT_DIR = Path("../outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

RANDOM_SEED = 42
rng = np.random.default_rng(RANDOM_SEED)


def run_supervised_and_unsupervised() -> dict:
    """Train a supervised model and compare with unsupervised clustering."""
    x, y = make_classification(
        n_samples=1500,
        n_features=6,
        n_informative=4,
        n_redundant=1,
        n_clusters_per_class=2,
        random_state=RANDOM_SEED,
    )

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.30,
        stratify=y,
        random_state=RANDOM_SEED,
    )

    supervised_model = Pipeline(
        steps=[
            ("scale", StandardScaler()),
            ("classifier", LogisticRegression(max_iter=1000, random_state=RANDOM_SEED)),
        ]
    )

    supervised_model.fit(x_train, y_train)
    supervised_prediction = supervised_model.predict(x_test)

    supervised_accuracy = accuracy_score(y_test, supervised_prediction)

    cluster_model = KMeans(n_clusters=2, random_state=RANDOM_SEED, n_init="auto")
    cluster_labels = cluster_model.fit_predict(x)

    cluster_alignment = adjusted_rand_score(y, cluster_labels)

    return {
        "supervised_accuracy": supervised_accuracy,
        "unsupervised_cluster_alignment_adjusted_rand": cluster_alignment,
    }


def run_q_learning_demo() -> pd.DataFrame:
    """Run a tiny tabular Q-learning demonstration."""
    states = [0, 1, 2]
    actions = [0, 1]

    q = np.zeros((len(states), len(actions)))

    alpha = 0.30
    gamma = 0.90

    experience = [
        (0, 1, 0.0, 1),
        (1, 1, 1.0, 2),
        (2, 0, 0.0, 2),
    ]

    for state, action, reward, next_state in experience:
        target = reward + gamma * np.max(q[next_state])
        q[state, action] += alpha * (target - q[state, action])

    return pd.DataFrame(q, columns=["action_0", "action_1"])


def main() -> None:
    summary = run_supervised_and_unsupervised()
    q_table = run_q_learning_demo()

    summary_frame = pd.DataFrame([summary])

    summary_frame.to_csv(OUTPUT_DIR / "learning_paradigms_summary.csv", index=False)
    q_table.to_csv(OUTPUT_DIR / "q_learning_demo_table.csv", index=False)

    print(summary_frame)
    print(q_table)


if __name__ == "__main__":
    main()
