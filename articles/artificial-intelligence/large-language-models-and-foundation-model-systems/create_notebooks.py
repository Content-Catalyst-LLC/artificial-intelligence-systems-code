"""
Create advanced Jupyter notebooks for Large Language Models and Foundation Model Systems.
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
    "01_prompt_evaluation.ipynb": notebook(
        [
            markdown_cell("# Prompt Evaluation"),
            code_cell(
                """
import pandas as pd

records = pd.DataFrame({
    "prompt_version": ["v1", "v2", "v3"],
    "task_quality": [0.76, 0.84, 0.81],
    "factuality": [0.72, 0.86, 0.79],
    "safety": [0.88, 0.90, 0.93]
})

records["overall_score"] = records[["task_quality", "factuality", "safety"]].mean(axis=1)
records
                """
            ),
        ]
    ),
    "02_retrieval_grounding.ipynb": notebook(
        [
            markdown_cell("# Retrieval Grounding"),
            code_cell(
                """
import pandas as pd

retrieval = pd.DataFrame({
    "query_id": ["Q1", "Q2", "Q3", "Q4"],
    "retrieved_sources": [4, 3, 5, 2],
    "source_support_rate": [0.75, 0.33, 0.80, 0.50],
    "citation_fidelity": [0.70, 0.40, 0.85, 0.55]
})

retrieval["review_required"] = (
    (retrieval["source_support_rate"] < 0.60) |
    (retrieval["citation_fidelity"] < 0.60)
)

retrieval
                """
            ),
        ]
    ),
    "03_cost_latency_review.ipynb": notebook(
        [
            markdown_cell("# Cost and Latency Review"),
            code_cell(
                """
import pandas as pd

usage = pd.DataFrame({
    "request_id": ["R1", "R2", "R3"],
    "input_tokens": [1200, 6400, 8500],
    "output_tokens": [400, 1200, 1600],
    "latency_seconds": [2.1, 6.8, 9.4]
})

usage["total_tokens"] = usage["input_tokens"] + usage["output_tokens"]
usage["high_cost_review"] = usage["total_tokens"] > 9000

usage
                """
            ),
        ]
    ),
    "04_llm_governance_register.ipynb": notebook(
        [
            markdown_cell("# LLM Governance Register"),
            code_cell(
                """
import pandas as pd

register = pd.DataFrame({
    "artifact": [
        "llm_system_card",
        "prompt_review",
        "retrieval_evaluation",
        "tool_use_approval",
        "safety_review",
        "incident_response_plan",
        "monitoring_dashboard"
    ],
    "status": [
        "complete",
        "in_review",
        "in_review",
        "planned",
        "complete",
        "complete",
        "active"
    ],
    "owner": [
        "Model Governance",
        "Product",
        "Search Infrastructure",
        "Security",
        "Responsible AI",
        "Operations",
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
