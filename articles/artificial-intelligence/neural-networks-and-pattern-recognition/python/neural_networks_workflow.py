"""
Neural Networks and Pattern Recognition Mini-Workflow

This script demonstrates:
- synthetic nonlinear classification data
- neural-network model fitting
- held-out evaluation
- representation projection using PCA

It is educational and does not require private data.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.datasets import make_moons
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


OUTPUT_DIR = Path("../outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

RANDOM_SEED = 42


def build_dataset() -> tuple[np.ndarray, np.ndarray]:
    """Create a synthetic nonlinear classification dataset."""
    x, y = make_moons(
        n_samples=2500,
        noise=0.25,
        random_state=RANDOM_SEED,
    )
    return x, y


def train_model(x: np.ndarray, y: np.ndarray) -> tuple[Pipeline, pd.DataFrame]:
    """Train a small multilayer perceptron and return evaluation metrics."""
    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.30,
        stratify=y,
        random_state=RANDOM_SEED,
    )

    model = Pipeline(
        steps=[
            ("scale", StandardScaler()),
            (
                "mlp",
                MLPClassifier(
                    hidden_layer_sizes=(32, 16),
                    activation="relu",
                    solver="adam",
                    max_iter=600,
                    random_state=RANDOM_SEED,
                ),
            ),
        ]
    )

    model.fit(x_train, y_train)

    prediction = model.predict(x_test)

    metrics = pd.DataFrame(
        [
            {
                "accuracy": accuracy_score(y_test, prediction),
                "f1": f1_score(y_test, prediction),
            }
        ]
    )

    return model, metrics


def representation_projection(model: Pipeline, x: np.ndarray, y: np.ndarray) -> pd.DataFrame:
    """Project standardized input data into a lightweight representation space."""
    scaled_x = model.named_steps["scale"].transform(x)

    pca = PCA(n_components=2, random_state=RANDOM_SEED)
    z = pca.fit_transform(scaled_x)

    return pd.DataFrame(
        {
            "z1": z[:, 0],
            "z2": z[:, 1],
            "target": y,
        }
    )


def main() -> None:
    x, y = build_dataset()
    model, metrics = train_model(x, y)
    representation = representation_projection(model, x, y)

    metrics.to_csv(OUTPUT_DIR / "neural_network_metrics.csv", index=False)
    representation.to_csv(OUTPUT_DIR / "representation_projection.csv", index=False)

    print(metrics)
    print(representation.head())


if __name__ == "__main__":
    main()
