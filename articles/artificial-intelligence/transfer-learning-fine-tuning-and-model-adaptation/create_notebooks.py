"""
Create advanced Jupyter notebooks for Transfer Learning, Fine-Tuning, and Model Adaptation.
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
    "01_fine_tuning_tradeoffs.ipynb": notebook(
        [
            markdown_cell("# Fine-Tuning Tradeoffs"),
            code_cell(
                """
import pandas as pd

methods = pd.DataFrame({
    "method": ["full_fine_tuning", "adapter_tuning", "lora", "qlora"],
    "target_gain": [0.13, 0.09, 0.10, 0.09],
    "source_retention": [0.78, 0.91, 0.92, 0.89],
    "compute_cost": [0.90, 0.28, 0.24, 0.16]
})

methods["risk_adjusted_score"] = (
    methods["target_gain"]
    + 0.30 * methods["source_retention"]
    - 0.20 * methods["compute_cost"]
)

methods.sort_values("risk_adjusted_score", ascending=False)
                """
            ),
        ]
    ),
    "02_negative_transfer_review.ipynb": notebook(
        [
            markdown_cell("# Negative Transfer Review"),
            code_cell(
                """
import pandas as pd

results = pd.DataFrame({
    "run_id": ["A", "B", "C", "D"],
    "baseline": [0.66, 0.66, 0.66, 0.66],
    "adapted": [0.75, 0.63, 0.78, 0.64]
})

results["transfer_gain"] = results["adapted"] - results["baseline"]
results["negative_transfer"] = results["transfer_gain"] < 0

results
                """
            ),
        ]
    ),
    "03_parameter_efficient_adaptation.ipynb": notebook(
        [
            markdown_cell("# Parameter-Efficient Adaptation"),
            code_cell(
                """
import pandas as pd

peft = pd.DataFrame({
    "method": ["adapter", "lora", "prefix", "qlora"],
    "trainable_parameter_share": [0.04, 0.02, 0.001, 0.02],
    "storage_cost_index": [0.12, 0.08, 0.03, 0.06],
    "deployment_complexity": [0.35, 0.30, 0.25, 0.40]
})

peft
                """
            ),
        ]
    ),
    "04_adaptation_governance_register.ipynb": notebook(
        [
            markdown_cell("# Adaptation Governance Register"),
            code_cell(
                """
import pandas as pd

register = pd.DataFrame({
    "artifact": [
        "base_model_record",
        "target_data_provenance",
        "fine_tuning_config",
        "evaluation_report",
        "forgetting_review",
        "deployment_approval",
        "rollback_plan"
    ],
    "status": [
        "complete",
        "complete",
        "complete",
        "in_review",
        "planned",
        "pending",
        "complete"
    ],
    "owner": [
        "Model Governance",
        "Data Steward",
        "ML Engineering",
        "Model Validation",
        "Responsible AI",
        "Governance",
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
