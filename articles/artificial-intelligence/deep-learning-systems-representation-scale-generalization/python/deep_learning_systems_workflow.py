"""
Deep Learning Systems Mini-Workflow

This script demonstrates:
- synthetic high-dimensional data
- representation geometry with PCA
- scaling-law simulation
- generalization-gap diagnostics

It is educational and does not require private data.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.datasets import make_classification
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


OUTPUT_DIR = Path("../outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

RANDOM_SEED = 42


def representation_geometry() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Create synthetic data and project it into a simple representation space."""
    x, y = make_classification(
        n_samples=3000,
        n_features=50,
        n_informative=12,
        n_redundant=8,
        class_sep=1.2,
        random_state=RANDOM_SEED,
    )

    pca = PCA(n_components=2, random_state=RANDOM_SEED)
    z = pca.fit_transform(x)

    representation = pd.DataFrame(
        {
            "z1": z[:, 0],
            "z2": z[:, 1],
            "target": y,
        }
    )

    summary = pd.DataFrame(
        [
            {
                "pc1_explained_variance": pca.explained_variance_ratio_[0],
                "pc2_explained_variance": pca.explained_variance_ratio_[1],
                "total_explained_variance": pca.explained_variance_ratio_.sum(),
            }
        ]
    )

    return representation, summary


def generalization_diagnostics() -> pd.DataFrame:
    """Train a simple model and compute a generalization gap."""
    x, y = make_classification(
        n_samples=3000,
        n_features=50,
        n_informative=12,
        n_redundant=8,
        class_sep=1.2,
        random_state=RANDOM_SEED,
    )

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.30,
        stratify=y,
        random_state=RANDOM_SEED,
    )

    model = Pipeline(
        [
            ("scale", StandardScaler()),
            ("classifier", LogisticRegression(max_iter=1000, random_state=RANDOM_SEED)),
        ]
    )

    model.fit(x_train, y_train)

    train_accuracy = accuracy_score(y_train, model.predict(x_train))
    test_accuracy = accuracy_score(y_test, model.predict(x_test))

    return pd.DataFrame(
        [
            {
                "train_accuracy": train_accuracy,
                "test_accuracy": test_accuracy,
                "generalization_gap": train_accuracy - test_accuracy,
            }
        ]
    )


def scaling_law_simulation() -> pd.DataFrame:
    """Simulate a simple power-law relationship between scale and loss."""
    scale = np.logspace(2, 7, 40)
    alpha = 0.08
    a = 2.0
    b = 0.9

    loss = a * scale ** (-alpha) + b

    return pd.DataFrame(
        {
            "scale": scale,
            "simulated_loss": loss,
        }
    )


def main() -> None:
    representation, representation_summary = representation_geometry()
    generalization = generalization_diagnostics()
    scaling_curve = scaling_law_simulation()

    representation.to_csv(OUTPUT_DIR / "representation_projection.csv", index=False)
    representation_summary.to_csv(OUTPUT_DIR / "representation_summary.csv", index=False)
    generalization.to_csv(OUTPUT_DIR / "generalization_diagnostics.csv", index=False)
    scaling_curve.to_csv(OUTPUT_DIR / "scaling_law_simulation.csv", index=False)

    print(representation_summary)
    print(generalization)
    print(scaling_curve.head())


if __name__ == "__main__":
    main()
