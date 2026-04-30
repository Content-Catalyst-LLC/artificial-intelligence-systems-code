"""
AI System Validation Audit

This script demonstrates a reproducible audit workflow for a simple binary
classification model using synthetic data.

It covers:
- Synthetic data generation
- Train/test splitting
- Logistic regression baseline
- Accuracy, precision, recall, F1, ROC AUC
- Grouped error-rate diagnostics
- Basic drift signal calculation
- JSON audit report export
"""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline


RANDOM_SEED = 42
OUTPUT_DIR = Path("../outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


@dataclass
class ModelMetrics:
    accuracy: float
    precision: float
    recall: float
    f1: float
    roc_auc: float


def make_synthetic_ai_dataset(n_samples: int = 5000) -> pd.DataFrame:
    """Create a synthetic dataset with a group attribute for audit examples."""
    x, y = make_classification(
        n_samples=n_samples,
        n_features=8,
        n_informative=5,
        n_redundant=1,
        n_clusters_per_class=2,
        class_sep=1.0,
        weights=[0.65, 0.35],
        random_state=RANDOM_SEED,
    )

    data = pd.DataFrame(x, columns=[f"feature_{i}" for i in range(x.shape[1])])
    data["target"] = y

    rng = np.random.default_rng(RANDOM_SEED)
    data["group"] = rng.choice(["A", "B", "C"], size=n_samples, p=[0.5, 0.3, 0.2])

    return data


def evaluate_model(y_true: np.ndarray, y_pred: np.ndarray, y_score: np.ndarray) -> ModelMetrics:
    """Compute common model-performance metrics."""
    return ModelMetrics(
        accuracy=float(accuracy_score(y_true, y_pred)),
        precision=float(precision_score(y_true, y_pred, zero_division=0)),
        recall=float(recall_score(y_true, y_pred, zero_division=0)),
        f1=float(f1_score(y_true, y_pred, zero_division=0)),
        roc_auc=float(roc_auc_score(y_true, y_score)),
    )


def grouped_error_diagnostics(frame: pd.DataFrame) -> pd.DataFrame:
    """Compute subgroup error rates for model audit reporting."""
    diagnostics = []

    for group_name, group_frame in frame.groupby("group"):
        y_true = group_frame["target"].to_numpy()
        y_pred = group_frame["prediction"].to_numpy()

        tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()

        false_positive_rate = fp / (fp + tn) if (fp + tn) > 0 else np.nan
        false_negative_rate = fn / (fn + tp) if (fn + tp) > 0 else np.nan
        selection_rate = float(np.mean(y_pred))

        diagnostics.append(
            {
                "group": group_name,
                "n": int(len(group_frame)),
                "selection_rate": selection_rate,
                "false_positive_rate": float(false_positive_rate),
                "false_negative_rate": float(false_negative_rate),
            }
        )

    return pd.DataFrame(diagnostics)


def population_stability_index(reference: np.ndarray, current: np.ndarray, bins: int = 10) -> float:
    """Estimate population stability index for a single numerical feature."""
    reference_counts, bin_edges = np.histogram(reference, bins=bins)
    current_counts, _ = np.histogram(current, bins=bin_edges)

    reference_pct = reference_counts / max(reference_counts.sum(), 1)
    current_pct = current_counts / max(current_counts.sum(), 1)

    epsilon = 1e-6
    psi = np.sum(
        (current_pct - reference_pct)
        * np.log((current_pct + epsilon) / (reference_pct + epsilon))
    )

    return float(psi)


def main() -> None:
    data = make_synthetic_ai_dataset()

    feature_columns = [col for col in data.columns if col.startswith("feature_")]
    x = data[feature_columns]
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
            ("scale", StandardScaler()),
            ("classifier", LogisticRegression(max_iter=1000, random_state=RANDOM_SEED)),
        ]
    )

    model.fit(x_train, y_train)

    y_score = model.predict_proba(x_test)[:, 1]
    y_pred = (y_score >= 0.50).astype(int)

    metrics = evaluate_model(y_test.to_numpy(), y_pred, y_score)

    audit_frame = x_test.copy()
    audit_frame["target"] = y_test.to_numpy()
    audit_frame["group"] = group_test.to_numpy()
    audit_frame["score"] = y_score
    audit_frame["prediction"] = y_pred

    grouped_diagnostics = grouped_error_diagnostics(audit_frame)

    drift_signal = population_stability_index(
        reference=x_train["feature_0"].to_numpy(),
        current=x_test["feature_0"].to_numpy(),
    )

    report = {
        "article": "Artificial Intelligence",
        "model_family": "Logistic Regression Baseline",
        "data_type": "Synthetic classification data",
        "metrics": asdict(metrics),
        "drift_signal": {
            "feature": "feature_0",
            "population_stability_index": drift_signal,
        },
        "grouped_error_diagnostics": grouped_diagnostics.to_dict(orient="records"),
        "notes": [
            "This is a synthetic demonstration.",
            "Real-world AI audits require domain context, stakeholder review, privacy safeguards, and governance controls.",
            "Performance metrics alone are not sufficient to establish safety, fairness, reliability, or fitness for use.",
        ],
    }

    output_path = OUTPUT_DIR / "ai_system_validation_audit.json"
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    grouped_diagnostics.to_csv(OUTPUT_DIR / "grouped_error_diagnostics.csv", index=False)

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
