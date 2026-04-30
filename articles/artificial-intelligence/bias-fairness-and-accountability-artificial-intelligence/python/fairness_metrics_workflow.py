"""
Bias, Fairness, and Accountability in AI Mini-Workflow

This script demonstrates:
- synthetic classification data with group labels
- model fitting
- group-level fairness metrics
- fairness gaps
- threshold diagnostics

It is educational and does not use private data.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


OUTPUT_DIR = Path("../outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

RANDOM_SEED = 42


def build_dataset(n_samples: int = 5000) -> pd.DataFrame:
    """Create a synthetic binary classification dataset with group labels."""
    rng = np.random.default_rng(RANDOM_SEED)

    x, y = make_classification(
        n_samples=n_samples,
        n_features=10,
        n_informative=6,
        n_redundant=2,
        weights=[0.65, 0.35],
        random_state=RANDOM_SEED,
    )

    frame = pd.DataFrame(x, columns=[f"feature_{i}" for i in range(x.shape[1])])
    frame["target"] = y
    frame["group"] = rng.choice(["A", "B"], size=len(frame), p=[0.55, 0.45])

    return frame


def group_metrics(data: pd.DataFrame) -> pd.DataFrame:
    """Compute group-level fairness and classification metrics."""
    rows = []

    for group_name, group_data in data.groupby("group"):
        tn, fp, fn, tp = confusion_matrix(
            group_data["target"],
            group_data["prediction"],
            labels=[0, 1],
        ).ravel()

        selection_rate = group_data["prediction"].mean()
        base_rate = group_data["target"].mean()
        true_positive_rate = tp / max(tp + fn, 1)
        false_positive_rate = fp / max(fp + tn, 1)
        false_negative_rate = fn / max(tp + fn, 1)
        positive_predictive_value = tp / max(tp + fp, 1)

        rows.append(
            {
                "group": group_name,
                "n": len(group_data),
                "base_rate": base_rate,
                "selection_rate": selection_rate,
                "true_positive_rate": true_positive_rate,
                "false_positive_rate": false_positive_rate,
                "false_negative_rate": false_negative_rate,
                "positive_predictive_value": positive_predictive_value,
            }
        )

    return pd.DataFrame(rows)


def fairness_gaps(metrics: pd.DataFrame) -> pd.DataFrame:
    """Compute common group fairness gaps."""
    return pd.DataFrame(
        [
            {
                "demographic_parity_gap": metrics["selection_rate"].max()
                - metrics["selection_rate"].min(),
                "true_positive_rate_gap": metrics["true_positive_rate"].max()
                - metrics["true_positive_rate"].min(),
                "false_positive_rate_gap": metrics["false_positive_rate"].max()
                - metrics["false_positive_rate"].min(),
                "false_negative_rate_gap": metrics["false_negative_rate"].max()
                - metrics["false_negative_rate"].min(),
                "predictive_parity_gap": metrics["positive_predictive_value"].max()
                - metrics["positive_predictive_value"].min(),
            }
        ]
    )


def threshold_diagnostics(audit: pd.DataFrame) -> pd.DataFrame:
    """Evaluate fairness gaps across decision thresholds."""
    rows = []

    for threshold in np.linspace(0.10, 0.90, 17):
        temp = audit.copy()
        temp["prediction"] = (temp["score"] >= threshold).astype(int)

        metrics = group_metrics(temp)
        gaps = fairness_gaps(metrics).iloc[0].to_dict()
        gaps["threshold"] = threshold

        rows.append(gaps)

    return pd.DataFrame(rows)


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

    audit = pd.DataFrame(
        {
            "target": y_test.to_numpy(),
            "group": group_test.to_numpy(),
            "score": score,
            "prediction": prediction,
        }
    )

    metrics = group_metrics(audit)
    gaps = fairness_gaps(metrics)
    thresholds = threshold_diagnostics(audit)

    audit.to_csv(OUTPUT_DIR / "fairness_audit_frame.csv", index=False)
    metrics.to_csv(OUTPUT_DIR / "group_fairness_metrics.csv", index=False)
    gaps.to_csv(OUTPUT_DIR / "fairness_gaps.csv", index=False)
    thresholds.to_csv(OUTPUT_DIR / "threshold_diagnostics.csv", index=False)

    print(metrics)
    print(gaps)
    print(thresholds.head())


if __name__ == "__main__":
    main()
