"""
Create advanced Jupyter notebooks for the AI Safety and System Reliability article.

The notebooks are generated as .ipynb JSON files without requiring nbformat.
"""

from pathlib import Path
import json

ARTICLE_DIR = Path(__file__).resolve().parent
NOTEBOOK_DIR = ARTICLE_DIR / "notebooks"
NOTEBOOK_DIR.mkdir(exist_ok=True)


def markdown_cell(source: str) -> dict:
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": source.strip().splitlines(True),
    }


def code_cell(source: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source.strip().splitlines(True),
    }


def notebook(cells: list[dict]) -> dict:
    return {
        "cells": cells,
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


notebooks = {
    "01_risk_and_reliability_modeling.ipynb": notebook(
        [
            markdown_cell(
                """
                # Risk and Reliability Modeling

                This notebook models deployment risk, failure probability,
                reliability over time, uncertainty routing, and safety thresholds
                for AI systems.
                """
            ),
            code_cell(
                """
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

n = 5000
predicted_risk = rng.beta(2, 5, size=n)
uncertainty = 0.1 + 0.4 * np.exp(-((predicted_risk - 0.5) ** 2) / 0.04)
observed_failure = rng.binomial(1, predicted_risk)

df = pd.DataFrame({
    "predicted_risk": predicted_risk,
    "uncertainty": uncertainty,
    "observed_failure": observed_failure
})

decision_threshold = 0.70
uncertainty_threshold = 0.30

df["flagged"] = df["predicted_risk"] >= decision_threshold
df["review_required"] = df["uncertainty"] > uncertainty_threshold
df["missed_failure"] = (df["flagged"] == False) & (df["observed_failure"] == 1)

df.head()
                """
            ),
            code_cell(
                """
summary = pd.DataFrame({
    "metric": [
        "missed_failure_rate",
        "human_review_rate",
        "mean_predicted_risk",
        "mean_uncertainty"
    ],
    "value": [
        df["missed_failure"].mean(),
        df["review_required"].mean(),
        df["predicted_risk"].mean(),
        df["uncertainty"].mean()
    ]
})

summary
                """
            ),
        ]
    ),

    "02_monitoring_drift_calibration.ipynb": notebook(
        [
            markdown_cell(
                """
                # Monitoring, Drift, and Calibration

                This notebook demonstrates deployment monitoring using
                drift summaries and calibration tables.
                """
            ),
            code_cell(
                """
import numpy as np
import pandas as pd

rng = np.random.default_rng(7)

baseline_feature = rng.normal(0, 1, 3000)
deployment_feature = rng.normal(0.45, 1.2, 3000)

drift_summary = pd.DataFrame({
    "period": ["baseline", "deployment"],
    "mean": [baseline_feature.mean(), deployment_feature.mean()],
    "standard_deviation": [baseline_feature.std(), deployment_feature.std()]
})

drift_summary
                """
            ),
            code_cell(
                """
predicted = rng.uniform(0, 1, 3000)
observed = rng.binomial(1, predicted)

calibration = pd.DataFrame({
    "predicted": predicted,
    "observed": observed
})

calibration["band"] = pd.cut(
    calibration["predicted"],
    bins=np.linspace(0, 1, 11),
    include_lowest=True
)

calibration_table = calibration.groupby("band", observed=True).agg(
    count=("observed", "size"),
    predicted_mean=("predicted", "mean"),
    observed_rate=("observed", "mean")
)

calibration_table["calibration_gap"] = (
    calibration_table["predicted_mean"] - calibration_table["observed_rate"]
)

calibration_table
                """
            ),
        ]
    ),

    "03_adversarial_resilience_stress_tests.ipynb": notebook(
        [
            markdown_cell(
                """
                # Adversarial Resilience and Stress Testing

                This notebook sketches stress tests for perturbation sensitivity,
                missing data, and extreme input conditions.
                """
            ),
            code_cell(
                """
import numpy as np
import pandas as pd

rng = np.random.default_rng(21)

n = 2000
x1 = rng.normal(0, 1, n)
x2 = rng.normal(0, 1, n)

baseline_score = 1 / (1 + np.exp(-(1.2 * x1 - 0.8 * x2)))
perturbed_score = 1 / (1 + np.exp(-(1.2 * (x1 + 0.25) - 0.8 * x2)))

sensitivity = np.abs(perturbed_score - baseline_score)

stress_summary = pd.DataFrame({
    "metric": [
        "mean_score_change",
        "p95_score_change",
        "max_score_change"
    ],
    "value": [
        sensitivity.mean(),
        np.quantile(sensitivity, 0.95),
        sensitivity.max()
    ]
})

stress_summary
                """
            ),
        ]
    ),

    "04_governance_assurance_case.ipynb": notebook(
        [
            markdown_cell(
                """
                # Governance Evidence and Assurance Cases

                This notebook creates a structured governance evidence table
                for an AI safety assurance case.
                """
            ),
            code_cell(
                """
import pandas as pd

evidence = pd.DataFrame({
    "evidence_type": [
        "validation_report",
        "calibration_review",
        "drift_monitoring_plan",
        "stress_test_results",
        "incident_response_playbook",
        "human_oversight_protocol"
    ],
    "status": [
        "complete",
        "complete",
        "complete",
        "in_review",
        "complete",
        "in_review"
    ],
    "owner": [
        "ML Engineering",
        "Model Risk",
        "Data Platform",
        "AI Safety",
        "Operations",
        "Product Governance"
    ]
})

evidence
                """
            ),
        ]
    ),
}

for filename, nb in notebooks.items():
    path = NOTEBOOK_DIR / filename
    path.write_text(json.dumps(nb, indent=2))
    print(f"Created {path}")
