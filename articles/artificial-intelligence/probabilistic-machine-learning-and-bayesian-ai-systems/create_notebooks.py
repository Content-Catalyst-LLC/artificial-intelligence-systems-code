"""
Create advanced Jupyter notebooks for Probabilistic Machine Learning and Bayesian AI Systems.
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
    "01_bayesian_updating.ipynb": notebook(
        [
            markdown_cell("# Bayesian Updating"),
            code_cell(
                """
import pandas as pd

prior_alpha = 2
prior_beta = 18
observed_events = 7
observations = 40

posterior_alpha = prior_alpha + observed_events
posterior_beta = prior_beta + observations - observed_events
posterior_mean = posterior_alpha / (posterior_alpha + posterior_beta)

pd.DataFrame([{
    "prior_alpha": prior_alpha,
    "prior_beta": prior_beta,
    "posterior_alpha": posterior_alpha,
    "posterior_beta": posterior_beta,
    "posterior_mean": posterior_mean
}])
                """
            ),
        ]
    ),
    "02_calibration_review.ipynb": notebook(
        [
            markdown_cell("# Calibration Review"),
            code_cell(
                """
import pandas as pd

calibration = pd.DataFrame({
    "bin": ["0.0-0.1", "0.1-0.2", "0.2-0.3"],
    "mean_predicted_probability": [0.06, 0.15, 0.26],
    "observed_rate": [0.05, 0.19, 0.22]
})

calibration["absolute_calibration_error"] = (
    calibration["mean_predicted_probability"] - calibration["observed_rate"]
).abs()

calibration
                """
            ),
        ]
    ),
    "03_expected_loss_decision.ipynb": notebook(
        [
            markdown_cell("# Expected-Loss Decision Support"),
            code_cell(
                """
import pandas as pd

cases = pd.DataFrame({
    "case_id": ["A", "B", "C"],
    "posterior_risk": [0.05, 0.18, 0.34],
    "cost_false_negative": [100, 100, 100],
    "cost_intervention": [8, 8, 8]
})

cases["expected_loss_no_action"] = cases["posterior_risk"] * cases["cost_false_negative"]
cases["expected_loss_reduction"] = cases["expected_loss_no_action"] - cases["cost_intervention"]
cases["recommendation"] = cases["expected_loss_reduction"].apply(
    lambda value: "act" if value > 0 else "monitor"
)

cases
                """
            ),
        ]
    ),
    "04_bayesian_governance_register.ipynb": notebook(
        [
            markdown_cell("# Bayesian Governance Register"),
            code_cell(
                """
import pandas as pd

register = pd.DataFrame({
    "artifact": [
        "bayesian_model_card",
        "prior_review",
        "likelihood_review",
        "inference_diagnostics",
        "calibration_audit",
        "decision_threshold_review",
        "uncertainty_communication_plan"
    ],
    "status": [
        "complete",
        "in_review",
        "complete",
        "complete",
        "planned",
        "in_review",
        "planned"
    ],
    "owner": [
        "Model Governance",
        "Domain Expert",
        "Model Validation",
        "Data Science",
        "Risk",
        "Governance",
        "UX Research"
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
