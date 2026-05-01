"""
Create advanced Jupyter notebooks for Multimodal AI: Language, Vision, Audio, and Action.
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
    "01_modality_coverage.ipynb": notebook(
        [
            markdown_cell("# Modality Coverage Review"),
            code_cell(
                """
import pandas as pd

records = pd.DataFrame({
    "case_id": ["A", "B", "C"],
    "has_text": [1, 1, 1],
    "has_vision": [1, 0, 1],
    "has_audio": [0, 1, 1],
    "has_sensor": [1, 0, 0]
})

records["modality_count"] = records[["has_text", "has_vision", "has_audio", "has_sensor"]].sum(axis=1)
records["coverage_score"] = (records["modality_count"] / 4).clip(upper=1)

records
                """
            ),
        ]
    ),
    "02_cross_modal_retrieval.ipynb": notebook(
        [
            markdown_cell("# Cross-Modal Retrieval Review"),
            code_cell(
                """
import pandas as pd

retrieval = pd.DataFrame({
    "query_id": ["Q1", "Q2", "Q3"],
    "query_modality": ["text", "image", "audio"],
    "retrieved_modality": ["image", "text", "video"],
    "similarity_score": [0.84, 0.71, 0.66],
    "source_support": [True, True, False]
})

retrieval["review_required"] = (
    (retrieval["similarity_score"] < 0.70) |
    (~retrieval["source_support"])
)

retrieval
                """
            ),
        ]
    ),
    "03_action_safety.ipynb": notebook(
        [
            markdown_cell("# Action Safety Review"),
            code_cell(
                """
import pandas as pd

actions = pd.DataFrame({
    "action_id": ["ACT-1", "ACT-2", "ACT-3"],
    "action_type": ["tool_call", "robot_motion", "record_update"],
    "safety_score": [0.91, 0.62, 0.84],
    "rollback_available": [True, False, True],
    "confirmation_required": [False, True, True]
})

actions["review_required"] = (
    (actions["safety_score"] < 0.80) |
    (~actions["rollback_available"]) |
    (actions["confirmation_required"])
)

actions
                """
            ),
        ]
    ),
    "04_multimodal_governance_register.ipynb": notebook(
        [
            markdown_cell("# Multimodal Governance Register"),
            code_cell(
                """
import pandas as pd

register = pd.DataFrame({
    "artifact": [
        "multimodal_system_card",
        "modality_source_review",
        "fusion_review",
        "action_safety_review",
        "privacy_review",
        "accessibility_review",
        "incident_response_plan"
    ],
    "status": [
        "complete",
        "in_review",
        "in_review",
        "planned",
        "complete",
        "planned",
        "complete"
    ],
    "owner": [
        "Model Governance",
        "Data Stewardship",
        "ML Engineering",
        "Safety",
        "Privacy",
        "Accessibility",
        "Operations"
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
