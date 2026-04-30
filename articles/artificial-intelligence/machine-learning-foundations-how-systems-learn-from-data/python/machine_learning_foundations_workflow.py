"""
Machine Learning Foundations Mini-Workflow

This script demonstrates:
- synthetic data generation
- train/test splitting
- model fitting
- evaluation metrics
- calibration diagnostics
- grouped diagnostics

It is educational and does not use private data.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


OUTPUT_DIR = Path("../outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

RANDOM_SEED = 42


def build_dataset(n_samples: int = 4000) -> pd.DataFrame:
    """Create a synthetic classification dataset with group labels."""
    x, y = make_classification(
        n_samples=n_samples,
        n_features=12,
        n_informative=7,
        n_redundant=2,
        weights=[0.65, 0.35],
        random_state=RANDOM_SEED,
    )

    frame = pd.DataFrame(x, columns=[f"feature_{i}" for i in range(x.shape[1])])
    frame["target"] = y

    rng = np.random.default_rng(RANDOM_SEED)
    frame["group"] = rng.choice(["A", "B", "C"], size=len(frame), p=[0.50, 0.30, 0.20])

    return frame


def calibration_table(frame: pd.DataFrame, n_bins: int = 10) -> pd.DataFrame:
    """Create calibration bins from predicted probabilities."""
    temp = frame.copy()

    temp["confidence_bin"] = pd.cut(
        temp["score"],
        bins=np.linspace(0, 1, n_bins + 1),
        include_lowest=True,
    )

    return (
        temp
        .groupby("confidence_bin", observed=True)
        .agg(
            n=("target", "size"),
            mean_confidence=("score", "mean"),
            empirical_rate=("target", "mean"),
        )
        .reset_index()
    )


def grouped_diagnostics(frame: pd.DataFrame) -> pd.DataFrame:
    """Summarize prediction behavior by synthetic group."""
    return (
        frame
        .groupby("group")
        .agg(
            n=("target", "size"),
            base_rate=("target", "mean"),
            selection_rate=("prediction", "mean"),
            mean_score=("score", "mean"),
        )
        .reset_index()
    )


def main() -> None:
    data = build_dataset()

    features = [column for column in data.columns if column.startswith("feature_")]

    x_train, x_test, y_train, y_test, group_train, group_test = train_test_split(
        data[features],
        data["target"],
        data["group"],
        test_size=0.30,
        stratify=data["target"],
        random_state=RANDOM_SEED,
    )

    model = Pipeline(
        steps=[
            ("scale", StandardScaler()),
            ("classifier", LogisticRegression(max_iter=1000, random_state=RANDOM_SEED)),
        ]
    )

    model.fit(x_train, y_train)

    score = model.predict_proba(x_test)[:, 1]
    prediction = (score >= 0.50).astype(int)

    metrics = pd.DataFrame(
        [
            {
                "accuracy": accuracy_score(y_test, prediction),
                "precision": precision_score(y_test, prediction, zero_division=0),
                "recall": recall_score(y_test, prediction, zero_division=0),
                "f1": f1_score(y_test, prediction, zero_division=0),
                "roc_auc": roc_auc_score(y_test, score),
            }
        ]
    )

    audit_frame = pd.DataFrame(
        {
            "target": y_test.to_numpy(),
            "group": group_test.to_numpy(),
            "score": score,
            "prediction": prediction,
        }
    )

    calibration = calibration_table(audit_frame)
    grouped = grouped_diagnostics(audit_frame)

    metrics.to_csv(OUTPUT_DIR / "machine_learning_metrics.csv", index=False)
    calibration.to_csv(OUTPUT_DIR / "calibration_table.csv", index=False)
    grouped.to_csv(OUTPUT_DIR / "grouped_diagnostics.csv", index=False)

    print(metrics)
    print(calibration)
    print(grouped)


if __name__ == "__main__":
    main()
