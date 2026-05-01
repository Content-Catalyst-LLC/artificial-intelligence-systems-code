"""
Create advanced Jupyter notebooks for Explainable AI and Model Interpretability.
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
    "01_feature_attribution_and_surrogates.ipynb": notebook(
        [
            markdown_cell("# Feature Attribution and Local Surrogates"),
            code_cell(
                """
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

features = ["asset_age", "sensor_load", "maintenance_gap", "weather_stress", "inspection_score"]
attributions = pd.Series(rng.normal(0, 0.25, len(features)), index=features)

attributions.sort_values(key=np.abs, ascending=False)
                """
            ),
        ]
    ),
    "02_counterfactual_explanations.ipynb": notebook(
        [
            markdown_cell("# Counterfactual Explanations"),
            code_cell(
                """
import pandas as pd

original = pd.Series({
    "asset_age": 14.2,
    "sensor_load": 0.77,
    "maintenance_gap": 130,
    "weather_stress": 0.66,
    "inspection_score": 0.61
})

counterfactual = original.copy()
counterfactual["sensor_load"] = 0.59
counterfactual["maintenance_gap"] = 82
counterfactual["weather_stress"] = 0.48

pd.DataFrame({
    "original": original,
    "counterfactual": counterfactual,
    "change": counterfactual - original
})
                """
            ),
        ]
    ),
    "03_explanation_stability_audit.ipynb": notebook(
        [
            markdown_cell("# Explanation Stability Audit"),
            code_cell(
                """
import numpy as np
import pandas as pd

rng = np.random.default_rng(11)

base_explanations = rng.normal(0, 1, size=(100, 6))
perturbed_explanations = base_explanations + rng.normal(0, 0.15, size=(100, 6))

distances = np.linalg.norm(base_explanations - perturbed_explanations, axis=1)
stability = 1 / (1 + distances)

pd.Series(stability).describe()
                """
            ),
        ]
    ),
    "04_explainability_governance_register.ipynb": notebook(
        [
            markdown_cell("# Explainability Governance Register"),
            code_cell(
                """
import pandas as pd

register = pd.DataFrame({
    "artifact": [
        "model_card",
        "explanation_method_record",
        "counterfactual_audit",
        "stability_report",
        "contestation_process"
    ],
    "status": [
        "complete",
        "complete",
        "in_review",
        "complete",
        "planned"
    ],
    "owner": [
        "Model Governance",
        "ML Engineering",
        "Risk Review",
        "AI Safety",
        "Policy"
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
