"""
Robustness and Adversarial Resilience Mini-Workflow

This script demonstrates:
- synthetic binary classification data
- a lightweight logistic-style model
- clean accuracy
- adversarial-style feature perturbations
- robust accuracy and robustness gaps

It is educational and uses synthetic data.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


OUTPUT_DIR = Path("../outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

RANDOM_SEED = 42


def sigmoid(z: np.ndarray) -> np.ndarray:
    """Numerically stable sigmoid."""
    return 1 / (1 + np.exp(-z))


def build_dataset(n: int = 2000, d: int = 12) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Create synthetic binary classification data."""
    rng = np.random.default_rng(RANDOM_SEED)

    features = rng.normal(size=(n, d))
    true_weights = rng.normal(size=d)
    logits = features @ true_weights
    labels = (logits > 0).astype(int)

    return features, labels, true_weights


def build_model_weights(true_weights: np.ndarray) -> np.ndarray:
    """Create a simple noisy estimate of the true model weights."""
    rng = np.random.default_rng(RANDOM_SEED)
    return true_weights + rng.normal(scale=0.25, size=true_weights.shape[0])


def predict_proba(features: np.ndarray, weights: np.ndarray) -> np.ndarray:
    """Predict probability for the positive class."""
    return sigmoid(features @ weights)


def predict(features: np.ndarray, weights: np.ndarray) -> np.ndarray:
    """Predict binary labels."""
    return (predict_proba(features, weights) >= 0.5).astype(int)


def accuracy(features: np.ndarray, labels: np.ndarray, weights: np.ndarray) -> float:
    """Compute classification accuracy."""
    return float(np.mean(predict(features, weights) == labels))


def adversarial_perturb(
    features: np.ndarray,
    labels: np.ndarray,
    weights: np.ndarray,
    epsilon: float,
) -> np.ndarray:
    """
    Create a simple adversarial-style perturbation for a linear model.

    For positive examples, move features in the negative weight direction.
    For negative examples, move features in the positive weight direction.
    This is a simplified sign-based worst-case perturbation.
    """
    direction = np.where(labels[:, None] == 1, -1.0, 1.0)
    perturbation = epsilon * direction * np.sign(weights)
    return features + perturbation


def run_stress_test() -> pd.DataFrame:
    """Evaluate clean and robust accuracy across perturbation budgets."""
    features, labels, true_weights = build_dataset()
    model_weights = build_model_weights(true_weights)

    clean_acc = accuracy(features, labels, model_weights)
    rows: list[dict[str, float]] = []

    for epsilon in np.linspace(0.0, 0.50, 11):
        attacked_features = adversarial_perturb(
            features,
            labels,
            model_weights,
            epsilon,
        )

        robust_acc = accuracy(attacked_features, labels, model_weights)

        rows.append(
            {
                "epsilon": float(epsilon),
                "clean_accuracy": clean_acc,
                "robust_accuracy": robust_acc,
                "robustness_gap": clean_acc - robust_acc,
            }
        )

    return pd.DataFrame(rows)


def main() -> None:
    results = run_stress_test()

    results.to_csv(
        OUTPUT_DIR / "robustness_adversarial_stress_test.csv",
        index=False,
    )

    print(results)


if __name__ == "__main__":
    main()
