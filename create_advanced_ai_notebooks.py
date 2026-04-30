#!/usr/bin/env python3
"""
Create advanced Jupyter notebooks for the Artificial Intelligence Systems articles.

These notebooks are designed as guided labs:
- concept explanation
- runnable code
- interpretation cells
- audit/governance extension
- reproducible outputs
"""

from __future__ import annotations

import json
from pathlib import Path
from textwrap import dedent


BASE_DIR = Path("articles/artificial-intelligence")


def nb(markdown_title: str, cells: list[dict]) -> dict:
    """Create a minimal Jupyter notebook object."""
    return {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [f"# {markdown_title}\n"],
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


def write_notebook(path: Path, title: str, cells: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(nb(title, cells), indent=2), encoding="utf-8")
    print(f"created {path}")


what_is_dir = BASE_DIR / "what-is-artificial-intelligence" / "notebooks"
history_dir = BASE_DIR / "history-of-artificial-intelligence-from-symbolic-logic-to-machine-learning" / "notebooks"


write_notebook(
    what_is_dir / "01_ai_systems_validation_lab.ipynb",
    "AI Systems Validation Lab",
    [
        md("""
        ## Purpose

        This lab introduces artificial intelligence as a validation problem, not merely a modeling problem.

        You will build a synthetic classification system, train a baseline model, evaluate performance, and produce an audit-ready metrics table.

        Learning goals:

        - Understand the relationship between data, model, prediction, and evaluation.
        - Compute accuracy, precision, recall, F1, and ROC AUC.
        - Separate model capability from system trustworthiness.
        - Prepare outputs that could be used in an AI governance workflow.
        """),
        code("""
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
            classification_report,
        )
        from sklearn.model_selection import train_test_split
        from sklearn.pipeline import Pipeline
        from sklearn.preprocessing import StandardScaler

        RANDOM_SEED = 42
        """),
        md("""
        ## Synthetic AI System Dataset

        This dataset is synthetic. It represents the structure of an AI decision-support problem without using private, regulated, or sensitive data.
        """),
        code("""
        X, y = make_classification(
            n_samples=6000,
            n_features=10,
            n_informative=6,
            n_redundant=2,
            weights=[0.65, 0.35],
            class_sep=0.9,
            random_state=RANDOM_SEED,
        )

        frame = pd.DataFrame(X, columns=[f"feature_{i}" for i in range(X.shape[1])])
        frame["target"] = y

        rng = np.random.default_rng(RANDOM_SEED)
        frame["group"] = rng.choice(["A", "B", "C"], size=len(frame), p=[0.50, 0.30, 0.20])

        frame.head()
        """),
        md("""
        ## Train a Baseline Model

        A baseline model is not the final system. It is a reference point for disciplined comparison.
        """),
        code("""
        features = [c for c in frame.columns if c.startswith("feature_")]

        X_train, X_test, y_train, y_test, group_train, group_test = train_test_split(
            frame[features],
            frame["target"],
            frame["group"],
            test_size=0.30,
            stratify=frame["target"],
            random_state=RANDOM_SEED,
        )

        model = Pipeline(
            steps=[
                ("scaler", StandardScaler()),
                ("classifier", LogisticRegression(max_iter=1000, random_state=RANDOM_SEED)),
            ]
        )

        model.fit(X_train, y_train)

        scores = model.predict_proba(X_test)[:, 1]
        predictions = (scores >= 0.50).astype(int)
        """),
        md("""
        ## Model Evaluation

        Aggregate metrics are necessary but incomplete. They summarize performance but do not reveal who bears different kinds of error.
        """),
        code("""
        metrics = {
            "accuracy": accuracy_score(y_test, predictions),
            "precision": precision_score(y_test, predictions, zero_division=0),
            "recall": recall_score(y_test, predictions, zero_division=0),
            "f1": f1_score(y_test, predictions, zero_division=0),
            "roc_auc": roc_auc_score(y_test, scores),
        }

        pd.DataFrame([metrics])
        """),
        code("""
        print(classification_report(y_test, predictions, zero_division=0))
        print(confusion_matrix(y_test, predictions))
        """),
        md("""
        ## Interpretation Checklist

        Use these prompts before treating model performance as trustworthy:

        1. What does a false positive mean in this domain?
        2. What does a false negative mean?
        3. Are the data representative of deployment conditions?
        4. Are thresholds aligned with the real decision context?
        5. Does performance vary across groups, time periods, or environments?
        """),
    ],
)


write_notebook(
    what_is_dir / "02_grouped_error_and_fairness_diagnostics.ipynb",
    "Grouped Error and Fairness Diagnostics Lab",
    [
        md("""
        ## Purpose

        This lab extends model validation into grouped diagnostics.

        The goal is not to claim that simple metrics solve fairness. The goal is to show how aggregate performance can hide uneven error burdens.
        """),
        code("""
        import numpy as np
        import pandas as pd
        from sklearn.datasets import make_classification
        from sklearn.linear_model import LogisticRegression
        from sklearn.model_selection import train_test_split
        from sklearn.pipeline import Pipeline
        from sklearn.preprocessing import StandardScaler

        RANDOM_SEED = 42
        """),
        code("""
        X, y = make_classification(
            n_samples=6000,
            n_features=10,
            n_informative=6,
            n_redundant=2,
            weights=[0.65, 0.35],
            random_state=RANDOM_SEED,
        )

        frame = pd.DataFrame(X, columns=[f"feature_{i}" for i in range(X.shape[1])])
        frame["target"] = y

        rng = np.random.default_rng(RANDOM_SEED)
        frame["group"] = rng.choice(["A", "B", "C"], size=len(frame), p=[0.50, 0.30, 0.20])
        """),
        code("""
        features = [c for c in frame.columns if c.startswith("feature_")]

        X_train, X_test, y_train, y_test, group_train, group_test = train_test_split(
            frame[features],
            frame["target"],
            frame["group"],
            test_size=0.30,
            stratify=frame["target"],
            random_state=RANDOM_SEED,
        )

        model = Pipeline(
            steps=[
                ("scaler", StandardScaler()),
                ("classifier", LogisticRegression(max_iter=1000, random_state=RANDOM_SEED)),
            ]
        )

        model.fit(X_train, y_train)

        audit = X_test.copy()
        audit["target"] = y_test.to_numpy()
        audit["group"] = group_test.to_numpy()
        audit["score"] = model.predict_proba(X_test)[:, 1]
        audit["prediction"] = (audit["score"] >= 0.50).astype(int)
        """),
        md("""
        ## Grouped Diagnostics Function

        This function computes selection rate, false positive rate, and false negative rate by group.
        """),
        code("""
        def grouped_diagnostics(data: pd.DataFrame) -> pd.DataFrame:
            rows = []

            for group_name, group_frame in data.groupby("group"):
                target = group_frame["target"]
                prediction = group_frame["prediction"]

                tp = ((target == 1) & (prediction == 1)).sum()
                tn = ((target == 0) & (prediction == 0)).sum()
                fp = ((target == 0) & (prediction == 1)).sum()
                fn = ((target == 1) & (prediction == 0)).sum()

                rows.append(
                    {
                        "group": group_name,
                        "n": len(group_frame),
                        "base_rate": target.mean(),
                        "selection_rate": prediction.mean(),
                        "false_positive_rate": fp / max(fp + tn, 1),
                        "false_negative_rate": fn / max(fn + tp, 1),
                    }
                )

            return pd.DataFrame(rows)

        grouped_diagnostics(audit)
        """),
        md("""
        ## Threshold Sensitivity

        Fairness and reliability are often threshold-sensitive. A single threshold can shift who receives false positives or false negatives.
        """),
        code("""
        def diagnostics_at_threshold(data: pd.DataFrame, threshold: float) -> pd.DataFrame:
            temp = data.copy()
            temp["prediction"] = (temp["score"] >= threshold).astype(int)
            result = grouped_diagnostics(temp)
            result["threshold"] = threshold
            return result

        threshold_results = pd.concat(
            [diagnostics_at_threshold(audit, t) for t in np.linspace(0.20, 0.80, 13)],
            ignore_index=True,
        )

        threshold_results.head()
        """),
        code("""
        threshold_results.to_csv("../outputs/threshold_grouped_diagnostics.csv", index=False)
        threshold_results.tail()
        """),
        md("""
        ## Interpretation Checklist

        - Which group has the highest false positive rate?
        - Which group has the highest false negative rate?
        - Does the threshold reduce one harm while increasing another?
        - Are the group labels legally and ethically appropriate to use?
        - Who should review the results before deployment?
        """),
    ],
)


write_notebook(
    what_is_dir / "03_drift_monitoring_and_model_decay.ipynb",
    "Drift Monitoring and Model Decay Lab",
    [
        md("""
        ## Purpose

        This lab introduces model drift.

        A model that performs well at launch can degrade when deployment data diverges from training data.
        """),
        code("""
        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt

        RANDOM_SEED = 42
        rng = np.random.default_rng(RANDOM_SEED)
        """),
        code("""
        n = 5000

        reference = rng.normal(loc=0.0, scale=1.0, size=n)
        mild_drift = rng.normal(loc=0.35, scale=1.05, size=n)
        severe_drift = rng.normal(loc=1.00, scale=1.25, size=n)

        distributions = pd.DataFrame({
            "reference": reference,
            "mild_drift": mild_drift,
            "severe_drift": severe_drift,
        })

        distributions.describe()
        """),
        md("""
        ## Population Stability Index

        Population Stability Index is a simple monitoring signal for distribution shift. It should not be used as a complete drift framework, but it is useful as a dashboard indicator.
        """),
        code("""
        def population_stability_index(reference_values, current_values, bins=10):
            reference_counts, bin_edges = np.histogram(reference_values, bins=bins)
            current_counts, _ = np.histogram(current_values, bins=bin_edges)

            reference_pct = reference_counts / max(reference_counts.sum(), 1)
            current_pct = current_counts / max(current_counts.sum(), 1)

            epsilon = 1e-6
            psi = np.sum(
                (current_pct - reference_pct)
                * np.log((current_pct + epsilon) / (reference_pct + epsilon))
            )

            return psi

        drift_summary = pd.DataFrame([
            {
                "comparison": "reference_vs_mild_drift",
                "psi": population_stability_index(reference, mild_drift),
            },
            {
                "comparison": "reference_vs_severe_drift",
                "psi": population_stability_index(reference, severe_drift),
            },
        ])

        drift_summary
        """),
        code("""
        plt.figure(figsize=(8, 5))
        plt.hist(reference, bins=40, alpha=0.5, label="reference")
        plt.hist(mild_drift, bins=40, alpha=0.5, label="mild drift")
        plt.hist(severe_drift, bins=40, alpha=0.5, label="severe drift")
        plt.legend()
        plt.title("Synthetic Distribution Shift")
        plt.xlabel("Feature value")
        plt.ylabel("Count")
        plt.show()
        """),
        md("""
        ## Governance Questions

        - What level of drift requires review?
        - Who receives the alert?
        - Is retraining automatic or governed?
        - What data is used for retraining?
        - How are model versions documented?
        """),
    ],
)


write_notebook(
    what_is_dir / "04_model_card_and_audit_artifact_lab.ipynb",
    "Model Card and Audit Artifact Lab",
    [
        md("""
        ## Purpose

        This lab creates a simple machine-readable audit artifact.

        Model cards and audit metadata help connect technical performance to governance, intended use, limitations, and oversight.
        """),
        code("""
        import json
        from pathlib import Path
        from datetime import date

        OUTPUT_DIR = Path("../outputs")
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        """),
        code("""
        model_card = {
            "model_name": "Synthetic Logistic Regression Baseline",
            "article": "What Is Artificial Intelligence?",
            "version": "0.1.0",
            "date": str(date.today()),
            "model_family": "Logistic Regression",
            "intended_use": "Educational demonstration of AI validation and grouped diagnostics.",
            "out_of_scope_use": [
                "Production deployment",
                "High-stakes decision-making",
                "Use with private or sensitive data"
            ],
            "training_data": {
                "type": "Synthetic classification data",
                "contains_personal_data": False,
                "known_limitations": [
                    "Synthetic data does not represent a real population.",
                    "Group labels are artificial.",
                    "Performance metrics are not domain-valid."
                ]
            },
            "evaluation": {
                "required_metrics": [
                    "accuracy",
                    "precision",
                    "recall",
                    "f1",
                    "roc_auc",
                    "grouped_false_positive_rate",
                    "grouped_false_negative_rate"
                ]
            },
            "governance": {
                "human_oversight": "Required for interpretation.",
                "review_required_before_deployment": True,
                "monitoring_required": True,
                "risk_notes": [
                    "Aggregate metrics can hide subgroup harms.",
                    "Thresholds encode policy choices.",
                    "Data drift can degrade deployed systems."
                ]
            }
        }

        output_path = OUTPUT_DIR / "synthetic_model_card.json"
        output_path.write_text(json.dumps(model_card, indent=2), encoding="utf-8")

        print(json.dumps(model_card, indent=2))
        """),
        md("""
        ## Extension Exercise

        Add fields for:

        - data provenance
        - evaluation dataset version
        - known failure modes
        - rollback plan
        - stakeholder review
        - incident response owner
        """),
    ],
)


write_notebook(
    history_dir / "01_ai_history_timeline_lab.ipynb",
    "AI History Timeline Lab",
    [
        md("""
        ## Purpose

        This lab builds a reproducible AI history timeline.

        The goal is to treat history as structured evidence: events, sources, paradigms, and interpretive claims.
        """),
        code("""
        import pandas as pd
        from pathlib import Path

        OUTPUT_DIR = Path("../outputs")
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        """),
        code("""
        events = pd.DataFrame([
            {"year": 1950, "event": "Turing publishes Computing Machinery and Intelligence", "paradigm": "computability"},
            {"year": 1956, "event": "Dartmouth workshop names artificial intelligence", "paradigm": "symbolic_ai"},
            {"year": 1960, "event": "Early symbolic AI and search methods expand", "paradigm": "symbolic_ai"},
            {"year": 1980, "event": "Expert systems gain institutional attention", "paradigm": "expert_systems"},
            {"year": 1990, "event": "Statistical learning becomes increasingly central", "paradigm": "statistical_learning"},
            {"year": 2012, "event": "Deep learning breakthrough era accelerates", "paradigm": "deep_learning"},
            {"year": 2017, "event": "Transformer architecture reshapes sequence modeling", "paradigm": "deep_learning"},
            {"year": 2022, "event": "Generative AI enters broad public use", "paradigm": "systems_scale_ai"},
        ])

        events
        """),
        code("""
        events.to_csv(OUTPUT_DIR / "ai_history_events.csv", index=False)
        events.groupby("paradigm").size().reset_index(name="event_count")
        """),
        md("""
        ## Interpretation Prompt

        What is missing from this timeline?

        A serious historical timeline should include:
        - technical papers
        - institutions
        - funding shifts
        - hardware changes
        - benchmark changes
        - public policy shifts
        - ethical controversies
        - global and non-US contributions
        """),
    ],
)


write_notebook(
    history_dir / "02_paradigm_transition_model_lab.ipynb",
    "AI Paradigm Transition Model Lab",
    [
        md("""
        ## Purpose

        This lab models AI history as overlapping paradigms.

        Symbolic AI, statistical learning, deep learning, and systems-scale AI do not simply replace one another. They overlap, recombine, and persist.
        """),
        code("""
        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt
        from pathlib import Path

        OUTPUT_DIR = Path("../outputs")
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        """),
        code("""
        def logistic(year, midpoint, steepness):
            return 1.0 / (1.0 + np.exp(-steepness * (year - midpoint)))

        years = np.arange(1950, 2027)

        symbolic_score = 1.4 * (1.0 - logistic(years, midpoint=1990, steepness=0.08))
        statistical_score = logistic(years, midpoint=1995, steepness=0.08) * (
            1.0 - 0.35 * logistic(years, midpoint=2015, steepness=0.15)
        )
        deep_learning_score = logistic(years, midpoint=2012, steepness=0.20)
        systems_scale_score = logistic(years, midpoint=2020, steepness=0.35)

        scores = np.vstack([
            symbolic_score,
            statistical_score,
            deep_learning_score,
            systems_scale_score,
        ]).T

        shares = scores / scores.sum(axis=1, keepdims=True)

        paradigm_shares = pd.DataFrame({
            "year": years,
            "symbolic_ai": shares[:, 0],
            "statistical_learning": shares[:, 1],
            "deep_learning": shares[:, 2],
            "systems_scale_ai": shares[:, 3],
        })

        paradigm_shares.head()
        """),
        code("""
        paradigm_shares.to_csv(OUTPUT_DIR / "ai_history_paradigm_shares.csv", index=False)

        plt.figure(figsize=(10, 6))
        for column in ["symbolic_ai", "statistical_learning", "deep_learning", "systems_scale_ai"]:
            plt.plot(paradigm_shares["year"], paradigm_shares[column], label=column)

        plt.title("Synthetic AI Paradigm Shares Over Time")
        plt.xlabel("Year")
        plt.ylabel("Relative share")
        plt.legend()
        plt.show()
        """),
        md("""
        ## Interpretation

        This model is synthetic. It should not be presented as historical measurement.

        It is useful because it visualizes a conceptual argument: AI history is layered, not linear.
        """),
    ],
)


write_notebook(
    history_dir / "03_source_metadata_and_reproducible_history_lab.ipynb",
    "Source Metadata and Reproducible History Lab",
    [
        md("""
        ## Purpose

        This lab treats historical research as structured metadata.

        A high-quality AI history article should be able to track claims to sources, dates, paradigms, and interpretive categories.
        """),
        code("""
        import pandas as pd
        from pathlib import Path

        OUTPUT_DIR = Path("../outputs")
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        """),
        code("""
        sources = pd.DataFrame([
            {
                "source_id": "turing-1950",
                "author": "Turing, A.M.",
                "year": 1950,
                "title": "Computing Machinery and Intelligence",
                "category": "primary",
                "paradigm": "computability"
            },
            {
                "source_id": "dartmouth-1955",
                "author": "McCarthy, Minsky, Rochester, Shannon",
                "year": 1955,
                "title": "A Proposal for the Dartmouth Summer Research Project on Artificial Intelligence",
                "category": "primary",
                "paradigm": "symbolic_ai"
            },
            {
                "source_id": "nilsson-2009",
                "author": "Nilsson, N.J.",
                "year": 2009,
                "title": "The Quest for Artificial Intelligence",
                "category": "secondary",
                "paradigm": "ai_history"
            },
            {
                "source_id": "russell-norvig-2021",
                "author": "Russell, S. and Norvig, P.",
                "year": 2021,
                "title": "Artificial Intelligence: A Modern Approach",
                "category": "textbook",
                "paradigm": "general_ai"
            },
        ])

        sources
        """),
        code("""
        sources.to_csv(OUTPUT_DIR / "ai_history_sources_metadata.csv", index=False)

        sources.groupby(["category", "paradigm"]).size().reset_index(name="count")
        """),
        md("""
        ## Extension Exercise

        Add fields for:
        - URL
        - publisher
        - DOI
        - article section supported
        - quotation notes
        - reliability level
        - primary vs. secondary source status
        """),
    ],
)


write_notebook(
    history_dir / "04_symbolic_to_neural_comparison_lab.ipynb",
    "Symbolic to Neural Comparison Lab",
    [
        md("""
        ## Purpose

        This lab compares symbolic and learned approaches using simple examples.

        The goal is to show that symbolic AI and machine learning encode knowledge differently.
        """),
        code("""
        import numpy as np
        import pandas as pd
        from sklearn.tree import DecisionTreeClassifier, export_text
        """),
        md("""
        ## Symbolic Rule Example

        A symbolic system uses explicit rules. This is interpretable but brittle.
        """),
        code("""
        def symbolic_decision(temperature, humidity):
            if temperature > 80 and humidity > 0.60:
                return "high_risk"
            if temperature > 75:
                return "moderate_risk"
            return "low_risk"

        symbolic_decision(82, 0.70)
        """),
        md("""
        ## Learned Rule Example

        A model can infer decision boundaries from examples rather than receiving hand-coded rules.
        """),
        code("""
        rng = np.random.default_rng(42)

        n = 500
        temperature = rng.normal(75, 8, size=n)
        humidity = rng.uniform(0.30, 0.90, size=n)

        target = ((temperature > 80) & (humidity > 0.60)).astype(int)

        data = pd.DataFrame({
            "temperature": temperature,
            "humidity": humidity,
            "target": target,
        })

        model = DecisionTreeClassifier(max_depth=3, random_state=42)
        model.fit(data[["temperature", "humidity"]], data["target"])

        print(export_text(model, feature_names=["temperature", "humidity"]))
        """),
        md("""
        ## Interpretation

        The symbolic rule is explicit from the start. The learned model infers a rule-like structure from data.

        This is a miniature version of a major historical shift in AI:
        - symbolic AI encoded knowledge directly;
        - machine learning estimated patterns from examples;
        - modern systems often combine both.
        """),
    ],
)


readme_text = """# Advanced Notebooks

These notebooks are intended as guided labs for the Artificial Intelligence Systems knowledge series.

Notebook design standard:

1. Conceptual framing
2. Reproducible setup
3. Runnable model or data workflow
4. Evaluation and interpretation
5. Governance or audit extension
6. Exported outputs where useful
7. Exercises for deeper extension

The goal is to make each AI article function not only as a publication, but as a reproducible learning module.
"""

for notebook_dir in [what_is_dir, history_dir]:
    (notebook_dir / "README.md").write_text(readme_text, encoding="utf-8")
    print(f"updated {notebook_dir / 'README.md'}")
