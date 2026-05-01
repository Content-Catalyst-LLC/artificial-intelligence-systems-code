"""
Create advanced Jupyter notebooks for Model Monitoring, Drift, and AI Observability.
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
    "01_feature_and_prediction_drift.ipynb": notebook(
        [
            markdown_cell("# Feature and Prediction Drift"),
            code_cell(
                """
import pandas as pd

monitoring = pd.DataFrame({
    "batch": [1, 2, 3, 4],
    "max_feature_psi": [0.05, 0.18, 0.31, 0.22],
    "prediction_psi": [0.04, 0.12, 0.16, 0.29]
})

monitoring["drift_review_required"] = (
    (monitoring["max_feature_psi"] > 0.25) |
    (monitoring["prediction_psi"] > 0.25)
)

monitoring
                """
            ),
        ]
    ),
    "02_delayed_label_performance.ipynb": notebook(
        [
            markdown_cell("# Delayed Label Performance"),
            code_cell(
                """
import pandas as pd

labels = pd.DataFrame({
    "batch": [1, 2, 3, 4],
    "label_available": [True, True, False, False],
    "accuracy": [0.88, 0.82, None, None],
    "human_override_rate": [0.04, 0.09, 0.13, 0.16]
})

labels["review_required"] = (
    (labels["accuracy"].fillna(1.0) < 0.78) |
    (labels["human_override_rate"] > 0.12)
)

labels
                """
            ),
        ]
    ),
    "03_slice_monitoring.ipynb": notebook(
        [
            markdown_cell("# Slice-Level Monitoring"),
            code_cell(
                """
import pandas as pd

slices = pd.DataFrame({
    "slice": ["overall", "region_a", "region_b", "new_source"],
    "accuracy": [0.84, 0.86, 0.79, 0.69],
    "missing_rate": [0.02, 0.01, 0.03, 0.11]
})

slices["review_required"] = (
    (slices["accuracy"] < 0.78) |
    (slices["missing_rate"] > 0.08)
)

slices
                """
            ),
        ]
    ),
    "04_observability_governance_register.ipynb": notebook(
        [
            markdown_cell("# Observability Governance Register"),
            code_cell(
                """
import pandas as pd

register = pd.DataFrame({
    "artifact": [
        "observability_system_card",
        "drift_review",
        "retraining_review",
        "rollback_readiness",
        "incident_response_plan",
        "threshold_review",
        "model_lifecycle_governance"
    ],
    "status": [
        "complete",
        "in_review",
        "planned",
        "in_review",
        "complete",
        "planned",
        "complete"
    ],
    "owner": [
        "MLOps",
        "Model Governance",
        "ML Engineering",
        "Platform Engineering",
        "Operations",
        "Risk",
        "Governance"
    ]
})

register
                """
            ),
        ]
    ),
}

for filename, nb in notebooks.items():
    path = NOTEBOOK_DIR / filename
    path.write_text(json.dumps(nb, indent=2))
    print(f"Created {path}")
