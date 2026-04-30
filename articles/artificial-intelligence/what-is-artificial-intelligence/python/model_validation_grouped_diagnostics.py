"""
Model Validation and Grouped Diagnostics

Synthetic educational workflow for the article:
"What Is Artificial Intelligence?"

This script demonstrates:
- synthetic data generation
- train/test validation
- grouped error diagnostics
- audit report export
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


RANDOM_SEED = 42
OUTPUT_DIR = Path("../outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def build_dataset(n_samples: int = 4000) -> pd.DataFrame:
    """Create a synthetic binary classification dataset with group labels."""
    x, y = make_classification(
        n_samples=n_samples,
        n_features=8,
        n_informative=5,
        n_redundant=1,
        weights=[0.65, 0.35],
        random_state=RANDOM_SEED,
    )

    frame = pd.DataFrame(x, columns=[f"feature_{i}" for i in range(x.shape[1])])
    frame["target"] = y

    rng = np.random.default_rng(RANDOM_SEED)
    frame["group"] = rng.choice(["A", "B", "C"], size=n_samples, p=[0.50, 0.30, 0.20])

    return frame


def grouped_diagnostics(frame: pd.DataFrame) -> pd.DataFrame:
    """Compute group-level selection and error rates."""
    rows = []

    for group_name, group_frame in frame.groupby("group"):
        target = group_frame["target"]
        prediction = group_frame["prediction"]

        true_positive = ((target == 1) & (prediction == 1)).sum()
        true_negative = ((target == 0) & (prediction == 0)).sum()
        false_positive = ((target == 0) & (prediction == 1)).sum()
        false_negative = ((target == 1) & (prediction == 0)).sum()

        rows.append(
            {
                "group": group_name,
                "n": int(len(group_frame)),
                "selection_rate": float(prediction.mean()),
                "false_positive_rate": float(false_positive / max(false_positive + true_negative, 1)),
                "false_negative_rate": float(false_negative / max(false_negative + true_positive, 1)),
            }
        )

    return pd.DataFrame(rows)


def main() -> None:
    data = build_dataset()

    features = [column for column in data.columns if column.startswith("feature_")]
    x = data[features]
    y = data["target"]

    x_train, x_test, y_train, y_test, group_train, group_test = train_test_split(
        x,
        y,
        data["group"],
        test_size=0.30,
        random_state=RANDOM_SEED,
        stratify=y,
    )

    model = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("classifier", LogisticRegression(max_iter=1000, random_state=RANDOM_SEED)),
        ]
    )

    model.fit(x_train, y_train)

    score = model.predict_proba(x_test)[:, 1]
    prediction = (score >= 0.50).astype(int)

    audit_frame = x_test.copy()
    audit_frame["target"] = y_test.to_numpy()
    audit_frame["group"] = group_test.to_numpy()
    audit_frame["score"] = score
    audit_frame["prediction"] = prediction

    metrics = {
        "accuracy": float(accuracy_score(y_test, prediction)),
        "precision": float(precision_score(y_test, prediction, zero_division=0)),
        "recall": float(recall_score(y_test, prediction, zero_division=0)),
        "f1": float(f1_score(y_test, prediction, zero_division=0)),
        "roc_auc": float(roc_auc_score(y_test, score)),
    }

    grouped = grouped_diagnostics(audit_frame)

    report = {
        "article": "What Is Artificial Intelligence?",
        "model_family": "Logistic Regression",
        "data_type": "Synthetic binary classification data",
        "metrics": metrics,
        "grouped_diagnostics": grouped.to_dict(orient="records"),
        "notes": [
            "This is a synthetic educational example.",
            "Real AI audits require domain context, privacy review, governance, stakeholder analysis, and monitoring.",
            "Aggregate metrics do not establish safety, fairness, reliability, or fitness for use."
        ],
    }

    (OUTPUT_DIR / "model_validation_report.json").write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )

    grouped.to_csv(OUTPUT_DIR / "grouped_diagnostics.csv", index=False)

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
