#!/usr/bin/env python3
"""
Create advanced Jupyter notebooks for:
Bias, Fairness, and Accountability in Artificial Intelligence
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
    NOTEBOOK_DIR / "01_fairness_metrics_and_group_diagnostics_lab.ipynb",
    "Fairness Metrics and Group Diagnostics Lab",
    [
        md("""
        ## Purpose

        This lab introduces group fairness metrics.

        Learning goals:

        - Build a synthetic classification dataset.
        - Train a classifier.
        - Compute selection rates, true positive rates, false positive rates, and predictive values.
        - Interpret fairness gaps as governance signals.
        """),
        code("""
        import numpy as np
        import pandas as pd

        from sklearn.datasets import make_classification
        from sklearn.linear_model import LogisticRegression
        from sklearn.metrics import confusion_matrix
        from sklearn.model_selection import train_test_split
        from sklearn.pipeline import Pipeline
        from sklearn.preprocessing import StandardScaler

        rng = np.random.default_rng(42)

        X, y = make_classification(
            n_samples=5000,
            n_features=10,
            n_informative=6,
            n_redundant=2,
            weights=[0.65, 0.35],
            random_state=42,
        )

        group = rng.choice(["A", "B"], size=len(y), p=[0.55, 0.45])

        X_train, X_test, y_train, y_test, group_train, group_test = train_test_split(
            X,
            y,
            group,
            test_size=0.30,
            stratify=y,
            random_state=42,
        )

        model = Pipeline([
            ("scale", StandardScaler()),
            ("classifier", LogisticRegression(max_iter=1000, random_state=42)),
        ])

        model.fit(X_train, y_train)

        score = model.predict_proba(X_test)[:, 1]
        prediction = (score >= 0.5).astype(int)

        audit = pd.DataFrame({
            "target": y_test,
            "group": group_test,
            "score": score,
            "prediction": prediction,
        })

        rows = []

        for group_name, data in audit.groupby("group"):
            tn, fp, fn, tp = confusion_matrix(data["target"], data["prediction"], labels=[0, 1]).ravel()

            rows.append({
                "group": group_name,
                "selection_rate": data["prediction"].mean(),
                "base_rate": data["target"].mean(),
                "true_positive_rate": tp / max(tp + fn, 1),
                "false_positive_rate": fp / max(fp + tn, 1),
                "positive_predictive_value": tp / max(tp + fp, 1),
            })

        metrics = pd.DataFrame(rows)
        metrics
        """),
        md("""
        ## Interpretation

        Group metrics are not final moral answers. They are evidence used in governance review.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "02_threshold_tradeoffs_and_equalized_odds_lab.ipynb",
    "Threshold Tradeoffs and Equalized Odds Lab",
    [
        md("""
        ## Purpose

        This lab explores how decision thresholds change fairness metrics.

        Learning goals:

        - Sweep thresholds.
        - Compare selection-rate gaps and error-rate gaps.
        - Interpret fairness as a tradeoff rather than a single optimum.
        """),
        code("""
        import numpy as np
        import pandas as pd

        rng = np.random.default_rng(42)

        n = 3000

        audit = pd.DataFrame({
            "group": rng.choice(["A", "B"], size=n, p=[0.55, 0.45]),
            "target": rng.binomial(1, 0.40, size=n),
        })

        audit["score"] = np.where(
            audit["target"] == 1,
            rng.beta(5, 3, size=n),
            rng.beta(3, 5, size=n),
        )

        audit.loc[audit["group"] == "B", "score"] = np.clip(
            audit.loc[audit["group"] == "B", "score"] - 0.04,
            0,
            1,
        )

        def summarize_at_threshold(frame, threshold):
            temp = frame.copy()
            temp["prediction"] = (temp["score"] >= threshold).astype(int)

            rows = []

            for group_name, data in temp.groupby("group"):
                tp = ((data["prediction"] == 1) & (data["target"] == 1)).sum()
                fp = ((data["prediction"] == 1) & (data["target"] == 0)).sum()
                fn = ((data["prediction"] == 0) & (data["target"] == 1)).sum()
                tn = ((data["prediction"] == 0) & (data["target"] == 0)).sum()

                rows.append({
                    "group": group_name,
                    "selection_rate": data["prediction"].mean(),
                    "tpr": tp / max(tp + fn, 1),
                    "fpr": fp / max(fp + tn, 1),
                })

            metrics = pd.DataFrame(rows)

            return {
                "threshold": threshold,
                "selection_gap": metrics["selection_rate"].max() - metrics["selection_rate"].min(),
                "tpr_gap": metrics["tpr"].max() - metrics["tpr"].min(),
                "fpr_gap": metrics["fpr"].max() - metrics["fpr"].min(),
            }

        threshold_table = pd.DataFrame([
            summarize_at_threshold(audit, threshold)
            for threshold in np.linspace(0.10, 0.90, 17)
        ])

        threshold_table
        """),
        md("""
        ## Interpretation

        Changing a threshold can improve one fairness metric while worsening another. Threshold policy should be approved and documented.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "03_calibration_counterfactual_fairness_and_proxy_risk_lab.ipynb",
    "Calibration, Counterfactual Fairness, and Proxy Risk Lab",
    [
        md("""
        ## Purpose

        This lab introduces calibration diagnostics and proxy-risk thinking.

        Learning goals:

        - Build calibration bins by group.
        - Simulate proxy variables.
        - Connect statistical audit to causal questions.
        """),
        code("""
        import numpy as np
        import pandas as pd

        rng = np.random.default_rng(42)

        n = 2500

        frame = pd.DataFrame({
            "group": rng.choice(["A", "B"], size=n, p=[0.55, 0.45]),
        })

        frame["proxy_variable"] = np.where(
            frame["group"] == "A",
            rng.normal(0.25, 1.0, size=n),
            rng.normal(-0.25, 1.0, size=n),
        )

        raw_score = 1 / (1 + np.exp(-(0.8 * frame["proxy_variable"] + rng.normal(0, 1, size=n))))
        frame["score"] = raw_score
        frame["target"] = rng.binomial(1, frame["score"])

        frame["confidence_bin"] = pd.cut(
            frame["score"],
            bins=np.linspace(0, 1, 11),
            include_lowest=True,
        )

        calibration = (
            frame
            .groupby(["group", "confidence_bin"], observed=True)
            .agg(
                n=("target", "size"),
                mean_confidence=("score", "mean"),
                empirical_rate=("target", "mean"),
            )
            .reset_index()
        )

        proxy_summary = (
            frame
            .groupby("group", as_index=False)
            .agg(
                mean_proxy=("proxy_variable", "mean"),
                mean_score=("score", "mean"),
                base_rate=("target", "mean"),
            )
        )

        calibration.head(), proxy_summary
        """),
        md("""
        ## Interpretation

        Calibration tells whether scores behave like probabilities. Proxy analysis asks whether variables transmit protected-attribute structure through the model.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "04_fairness_audit_governance_and_accountability_lab.ipynb",
    "Fairness Audit, Governance, and Accountability Lab",
    [
        md("""
        ## Purpose

        This lab frames fairness auditing as a governance process.

        Learning goals:

        - Build an audit checklist.
        - Track evidence status.
        - Connect metrics to owners, decisions, and remedy.
        """),
        code("""
        import pandas as pd

        audit_checklist = pd.DataFrame([
            {
                "audit_area": "decision_context",
                "question": "What decision does the system support or automate?",
                "evidence_status": "complete",
                "owner": "Governance Lead",
            },
            {
                "audit_area": "data_provenance",
                "question": "What datasets and labels shaped the model?",
                "evidence_status": "partial",
                "owner": "Data Steward",
            },
            {
                "audit_area": "protected_attributes",
                "question": "Which attributes are available for fairness auditing?",
                "evidence_status": "complete",
                "owner": "Legal / Privacy",
            },
            {
                "audit_area": "fairness_metrics",
                "question": "Which fairness definitions were evaluated and why?",
                "evidence_status": "partial",
                "owner": "Model Risk Team",
            },
            {
                "audit_area": "human_oversight",
                "question": "Who reviews decisions and under what conditions?",
                "evidence_status": "missing",
                "owner": "Operations",
            },
            {
                "audit_area": "contestability",
                "question": "Can affected people challenge outcomes?",
                "evidence_status": "missing",
                "owner": "Policy / Legal",
            },
            {
                "audit_area": "monitoring",
                "question": "What fairness metrics are monitored after deployment?",
                "evidence_status": "partial",
                "owner": "MLOps",
            },
        ])

        audit_summary = (
            audit_checklist
            .groupby("evidence_status", as_index=False)
            .agg(count=("audit_area", "size"))
        )

        audit_checklist, audit_summary
        """),
        md("""
        ## Interpretation

        A fairness audit is incomplete unless it connects metrics to evidence, owners, review procedures, and remedy.
        """),
    ],
)
