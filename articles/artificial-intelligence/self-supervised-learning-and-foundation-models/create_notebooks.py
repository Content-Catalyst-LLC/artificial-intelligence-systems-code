"""
Create advanced Jupyter notebooks for Self-Supervised Learning and Foundation Models.
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
    "01_masked_prediction.ipynb": notebook(
        [
            markdown_cell("# Masked Prediction"),
            code_cell(
                """
import pandas as pd

tokens = pd.DataFrame({
    "token_position": [1, 2, 3, 4, 5],
    "is_masked": [False, True, False, True, False],
    "prediction_confidence": [None, 0.72, None, 0.61, None]
})

tokens
                """
            ),
        ]
    ),
    "02_contrastive_learning.ipynb": notebook(
        [
            markdown_cell("# Contrastive Learning"),
            code_cell(
                """
import numpy as np
import pandas as pd

pairs = pd.DataFrame({
    "pair_id": ["P001", "P002", "P003"],
    "positive_similarity": [0.82, 0.76, 0.64],
    "negative_similarity": [0.25, 0.48, 0.59]
})

pairs["contrastive_margin"] = pairs["positive_similarity"] - pairs["negative_similarity"]
pairs
                """
            ),
        ]
    ),
    "03_foundation_model_risk.ipynb": notebook(
        [
            markdown_cell("# Foundation Model Risk Review"),
            code_cell(
                """
import pandas as pd

risk = pd.DataFrame({
    "risk_category": ["data_provenance", "privacy", "bias", "grounding", "broad_reuse"],
    "risk_score": [0.31, 0.18, 0.42, 0.37, 0.50],
    "mitigation_status": ["active", "complete", "planned", "active", "review"]
})

risk["requires_action"] = risk["risk_score"] > 0.40
risk
                """
            ),
        ]
    ),
    "04_governance_register.ipynb": notebook(
        [
            markdown_cell("# Foundation Model Governance Register"),
            code_cell(
                """
import pandas as pd

register = pd.DataFrame({
    "artifact": [
        "foundation_model_card",
        "pretraining_data_record",
        "objective_review",
        "evaluation_report",
        "privacy_review",
        "bias_review",
        "deployment_approval"
    ],
    "status": [
        "complete",
        "in_review",
        "complete",
        "in_review",
        "planned",
        "planned",
        "pending"
    ],
    "owner": [
        "Model Governance",
        "Data Steward",
        "Research",
        "Evaluation",
        "Privacy",
        "Responsible AI",
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
