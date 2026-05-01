"""
Create advanced Jupyter notebooks for Calibration, Uncertainty, and Probability in AI Systems.
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
    "01_reliability_diagram_data.ipynb": notebook(
        [
            markdown_cell("# Reliability Diagram Data"),
            code_cell(
                """
import pandas as pd

bins = pd.DataFrame({
    "bin": ["0.0-0.1", "0.1-0.2", "0.2-0.3", "0.3-0.4"],
    "mean_confidence": [0.05, 0.15, 0.25, 0.35],
    "observed_rate": [0.04, 0.18, 0.28, 0.32],
    "cases": [120, 180, 240, 210]
})

bins["calibration_gap"] = (bins["observed_rate"] - bins["mean_confidence"]).abs()
bins
                """
            ),
        ]
    ),
    "02_scoring_rules.ipynb": notebook(
        [
            markdown_cell("# Scoring Rules"),
            code_cell(
                """
import numpy as np
import pandas as pd

predictions = pd.DataFrame({
    "p": [0.10, 0.35, 0.62, 0.81, 0.92],
    "y": [0, 0, 1, 1, 0]
})

p = np.clip(predictions["p"].to_numpy(), 1e-9, 1 - 1e-9)
y = predictions["y"].to_numpy()

predictions["brier_component"] = (p - y) ** 2
predictions["nll_component"] = -(y * np.log(p) + (1 - y) * np.log(1 - p))

predictions
                """
            ),
        ]
    ),
    "03_threshold_policy.ipynb": notebook(
        [
            markdown_cell("# Threshold Policy Review"),
            code_cell(
                """
import pandas as pd

cases = pd.DataFrame({
    "case_id": ["A", "B", "C", "D"],
    "predicted_probability": [0.18, 0.48, 0.72, 0.91],
    "entropy": [0.32, 0.69, 0.58, 0.29]
})

cases["route"] = pd.cut(
    cases["predicted_probability"],
    bins=[0, 0.30, 0.75, 1.0],
    labels=["standard_processing", "human_review", "urgent_review"],
    include_lowest=True
)

cases["review_required"] = (cases["entropy"] > 0.62) | (cases["route"] == "human_review")

cases
                """
            ),
        ]
    ),
    "04_uncertainty_governance_register.ipynb": notebook(
        [
            markdown_cell("# Uncertainty Governance Register"),
            code_cell(
                """
import pandas as pd

register = pd.DataFrame({
    "artifact": [
        "calibration_review",
        "uncertainty_system_card",
        "threshold_policy",
        "abstention_review",
        "human_review_escalation",
        "recalibration_review",
        "monitoring_readiness"
    ],
    "status": [
        "complete",
        "complete",
        "in_review",
        "planned",
        "in_review",
        "planned",
        "complete"
    ],
    "owner": [
        "Model Governance",
        "ML Engineering",
        "Risk",
        "Operations",
        "Human Review Team",
        "ML Engineering",
        "MLOps"
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
