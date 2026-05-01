"""
Create advanced Jupyter notebooks for Robustness and Adversarial Resilience in Machine Learning.
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
    "01_perturbation_testing.ipynb": notebook(
        [
            markdown_cell("# Perturbation Testing"),
            code_cell(
                """
import pandas as pd

tests = pd.DataFrame({
    "case_id": ["C1", "C2", "C3"],
    "clean_performance": [0.92, 0.90, 0.88],
    "perturbed_performance": [0.86, 0.72, 0.80]
})

tests["performance_drop"] = tests["clean_performance"] - tests["perturbed_performance"]
tests["review_required"] = tests["performance_drop"] > 0.15

tests
                """
            ),
        ]
    ),
    "02_attack_type_summary.ipynb": notebook(
        [
            markdown_cell("# Attack-Type Summary"),
            code_cell(
                """
import pandas as pd

attacks = pd.DataFrame({
    "attack_type": ["evasion", "prompt_injection", "retrieval_poisoning", "model_extraction"],
    "attack_success_rate": [0.18, 0.31, 0.26, 0.14],
    "containment_score": [0.84, 0.68, 0.71, 0.76]
})

attacks["review_required"] = (
    (attacks["attack_success_rate"] > 0.25) |
    (attacks["containment_score"] < 0.70)
)

attacks
                """
            ),
        ]
    ),
    "03_red_team_findings.ipynb": notebook(
        [
            markdown_cell("# Red-Team Findings"),
            code_cell(
                """
import pandas as pd

findings = pd.DataFrame({
    "finding_id": ["RT-1", "RT-2", "RT-3"],
    "severity": ["medium", "high", "critical"],
    "status": ["open", "in_progress", "open"],
    "owner": ["ML Engineering", "Security", "Model Governance"]
})

severity_rank = {"low": 1, "medium": 2, "high": 3, "critical": 4}
findings["severity_rank"] = findings["severity"].map(severity_rank)
findings["priority_review"] = findings["severity_rank"] >= 3

findings
                """
            ),
        ]
    ),
    "04_resilience_governance_register.ipynb": notebook(
        [
            markdown_cell("# Resilience Governance Register"),
            code_cell(
                """
import pandas as pd

register = pd.DataFrame({
    "artifact": [
        "threat_model",
        "red_team_review",
        "robustness_evaluation",
        "data_poisoning_review",
        "prompt_injection_incident_plan",
        "resilience_controls",
        "deployment_readiness"
    ],
    "status": [
        "complete",
        "in_review",
        "complete",
        "planned",
        "complete",
        "in_review",
        "planned"
    ],
    "owner": [
        "Security",
        "Red Team",
        "ML Engineering",
        "Data Governance",
        "Operations",
        "Model Governance",
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
