"""
Create advanced Jupyter notebooks for Synthetic Data, Simulation, and AI Evaluation Environments.
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
    "01_fidelity_diagnostics.ipynb": notebook(
        [
            markdown_cell("# Synthetic Data Fidelity Diagnostics"),
            code_cell(
                """
import pandas as pd

fidelity = pd.DataFrame({
    "feature": ["age_like", "exposure", "sensor_score", "subgroup"],
    "distribution_gap": [0.04, 0.09, 0.06, 0.03],
    "status": ["normal", "warning", "normal", "normal"]
})

fidelity["review_required"] = fidelity["distribution_gap"] > 0.08
fidelity
                """
            ),
        ]
    ),
    "02_privacy_proximity.ipynb": notebook(
        [
            markdown_cell("# Privacy Proximity Review"),
            code_cell(
                """
import pandas as pd

privacy = pd.DataFrame({
    "artifact": ["high_fidelity", "moderate_fidelity", "low_privacy_high_fidelity"],
    "nearest_neighbor_risk": [0.02, 0.01, 0.17],
    "membership_inference_risk": [0.03, 0.02, 0.15]
})

privacy["privacy_review_required"] = (
    (privacy["nearest_neighbor_risk"] > 0.05) |
    (privacy["membership_inference_risk"] > 0.05)
)

privacy
                """
            ),
        ]
    ),
    "03_rare_case_coverage.ipynb": notebook(
        [
            markdown_cell("# Rare-Case Coverage"),
            code_cell(
                """
import pandas as pd

coverage = pd.DataFrame({
    "scenario_family": ["routine", "missing_data", "conflicting_evidence", "rare_high_impact"],
    "target_share": [0.50, 0.20, 0.20, 0.10],
    "synthetic_share": [0.54, 0.18, 0.21, 0.07]
})

coverage["coverage_gap"] = (coverage["target_share"] - coverage["synthetic_share"]).abs()
coverage["review_required"] = coverage["coverage_gap"] > 0.03

coverage
                """
            ),
        ]
    ),
    "04_synthetic_governance_register.ipynb": notebook(
        [
            markdown_cell("# Synthetic Evaluation Governance Register"),
            code_cell(
                """
import pandas as pd

register = pd.DataFrame({
    "artifact": [
        "synthetic_data_card",
        "simulation_environment_card",
        "benchmark_environment_card",
        "privacy_review",
        "utility_review",
        "sim_to_real_validation",
        "scenario_review",
        "deployment_readiness"
    ],
    "status": [
        "complete",
        "in_review",
        "complete",
        "planned",
        "in_review",
        "planned",
        "complete",
        "planned"
    ],
    "owner": [
        "Data Governance",
        "Simulation Team",
        "Model Evaluation",
        "Privacy",
        "ML Engineering",
        "Domain Experts",
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
