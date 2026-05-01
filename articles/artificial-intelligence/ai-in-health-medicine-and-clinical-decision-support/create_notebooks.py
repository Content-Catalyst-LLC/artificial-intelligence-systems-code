"""
Create advanced Jupyter notebooks for AI in Health, Medicine, and Clinical Decision Support.
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
    "01_clinical_calibration_review.ipynb": notebook(
        [
            markdown_cell("# Clinical Calibration Review"),
            code_cell(
                """
import pandas as pd

bins = pd.DataFrame({
    "risk_bin": ["0.0-0.1", "0.1-0.2", "0.2-0.3", "0.3-0.4"],
    "mean_predicted_risk": [0.05, 0.15, 0.25, 0.35],
    "observed_event_rate": [0.04, 0.18, 0.29, 0.31],
    "cases": [900, 1100, 800, 500]
})

bins["calibration_gap"] = (bins["observed_event_rate"] - bins["mean_predicted_risk"]).abs()
bins["weighted_gap"] = bins["cases"] / bins["cases"].sum() * bins["calibration_gap"]
bins
                """
            ),
        ]
    ),
    "02_subgroup_safety_review.ipynb": notebook(
        [
            markdown_cell("# Subgroup Safety Review"),
            code_cell(
                """
import pandas as pd

subgroups = pd.DataFrame({
    "group": ["overall", "site_a", "site_b", "non_english", "85_plus"],
    "sensitivity": [0.78, 0.80, 0.74, 0.65, 0.70],
    "alert_rate": [0.31, 0.30, 0.35, 0.42, 0.39]
})

overall_sensitivity = subgroups.loc[subgroups["group"] == "overall", "sensitivity"].iloc[0]
subgroups["sensitivity_gap"] = subgroups["sensitivity"] - overall_sensitivity
subgroups["review_required"] = subgroups["sensitivity_gap"].abs() > 0.10

subgroups
                """
            ),
        ]
    ),
    "03_alert_burden_threshold_policy.ipynb": notebook(
        [
            markdown_cell("# Alert Burden and Threshold Policy"),
            code_cell(
                """
import pandas as pd

thresholds = pd.DataFrame({
    "threshold": [0.15, 0.20, 0.25, 0.30, 0.35],
    "sensitivity": [0.91, 0.84, 0.78, 0.70, 0.61],
    "alert_rate": [0.55, 0.42, 0.31, 0.23, 0.17],
    "false_negative_rate": [0.09, 0.16, 0.22, 0.30, 0.39]
})

thresholds["review_required"] = (thresholds["alert_rate"] > 0.45) | (thresholds["false_negative_rate"] > 0.25)
thresholds
                """
            ),
        ]
    ),
    "04_clinical_ai_governance_register.ipynb": notebook(
        [
            markdown_cell("# Clinical AI Governance Register"),
            code_cell(
                """
import pandas as pd

register = pd.DataFrame({
    "artifact": [
        "clinical_ai_system_card",
        "intended_use_review",
        "validation_review",
        "bias_equity_review",
        "privacy_security_review",
        "change_control",
        "incident_response",
        "deployment_readiness"
    ],
    "status": [
        "complete",
        "complete",
        "in_review",
        "in_review",
        "planned",
        "planned",
        "complete",
        "planned"
    ],
    "owner": [
        "Clinical Governance",
        "Clinical Owner",
        "Biostatistics",
        "Equity Review",
        "Privacy Office",
        "Model Governance",
        "Patient Safety",
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
