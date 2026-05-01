"""
Create advanced Jupyter notebooks for AI in Education, Knowledge Work, and Learning Systems.
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
    "01_learning_gain_and_transfer.ipynb": notebook(
        [
            markdown_cell("# Learning Gain and Independent Transfer"),
            code_cell(
                """
import pandas as pd

records = pd.DataFrame({
    "group": ["overall", "high_access", "limited_access", "multilingual"],
    "baseline": [0.52, 0.55, 0.48, 0.50],
    "post_learning": [0.66, 0.71, 0.56, 0.64],
    "independent_transfer": [0.64, 0.69, 0.53, 0.61]
})

records["learning_gain"] = records["post_learning"] - records["baseline"]
records["transfer_gap_from_post"] = records["post_learning"] - records["independent_transfer"]
records
                """
            ),
        ]
    ),
    "02_assistance_gap_review.ipynb": notebook(
        [
            markdown_cell("# AI Assistance Gap Review"),
            code_cell(
                """
import pandas as pd

records = pd.DataFrame({
    "activity": ["essay", "coding", "math_practice", "research_summary"],
    "assisted_performance": [0.82, 0.78, 0.74, 0.86],
    "independent_transfer": [0.61, 0.59, 0.70, 0.58]
})

records["assistance_gap"] = records["assisted_performance"] - records["independent_transfer"]
records["review_required"] = records["assistance_gap"] > 0.20
records
                """
            ),
        ]
    ),
    "03_assessment_validity_review.ipynb": notebook(
        [
            markdown_cell("# Assessment Validity Review"),
            code_cell(
                """
import pandas as pd

assessments = pd.DataFrame({
    "assessment": ["take_home_essay", "oral_defense", "live_coding", "process_portfolio"],
    "ai_substitution_risk": [0.82, 0.18, 0.25, 0.32],
    "process_evidence": [False, True, True, True],
    "independent_demonstration": [False, True, True, True]
})

assessments["redesign_required"] = (
    (assessments["ai_substitution_risk"] > 0.50) &
    (~assessments["independent_demonstration"])
)

assessments
                """
            ),
        ]
    ),
    "04_learning_ai_governance_register.ipynb": notebook(
        [
            markdown_cell("# Learning AI Governance Register"),
            code_cell(
                """
import pandas as pd

register = pd.DataFrame({
    "artifact": [
        "education_ai_system_card",
        "ai_use_policy",
        "assessment_redesign",
        "privacy_review",
        "accessibility_review",
        "bias_equity_review",
        "incident_response",
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
        "Academic Technology",
        "Faculty Governance",
        "Instructional Design",
        "Privacy Office",
        "Accessibility Office",
        "Equity Review",
        "Student Support",
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
