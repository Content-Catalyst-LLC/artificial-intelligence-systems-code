"""
Create advanced Jupyter notebooks for Retrieval-Augmented Generation and AI Knowledge Systems.
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
    "01_chunking_diagnostics.ipynb": notebook(
        [
            markdown_cell("# Chunking Diagnostics"),
            code_cell(
                """
import pandas as pd

chunks = pd.DataFrame({
    "chunk_id": ["C1", "C2", "C3", "C4"],
    "tokens": [420, 880, 1250, 310],
    "has_section_title": [True, True, False, True],
    "has_source_date": [True, False, True, True]
})

chunks["review_required"] = (
    (chunks["tokens"] > 1000) |
    (~chunks["has_section_title"]) |
    (~chunks["has_source_date"])
)

chunks
                """
            ),
        ]
    ),
    "02_retrieval_evaluation.ipynb": notebook(
        [
            markdown_cell("# Retrieval Evaluation"),
            code_cell(
                """
import pandas as pd

retrieval = pd.DataFrame({
    "query_id": ["Q1", "Q2", "Q3"],
    "retrieved_k": [5, 5, 5],
    "relevant_retrieved": [4, 2, 0],
    "gold_source_retrieved": [True, False, False]
})

retrieval["recall_at_k"] = retrieval["relevant_retrieved"] / retrieval["retrieved_k"]
retrieval
                """
            ),
        ]
    ),
    "03_citation_support.ipynb": notebook(
        [
            markdown_cell("# Citation Support Review"),
            code_cell(
                """
import pandas as pd

citations = pd.DataFrame({
    "claim_id": ["CL1", "CL2", "CL3", "CL4"],
    "citation_present": [True, True, False, True],
    "source_supports_claim": [True, False, False, True]
})

citations["citation_failure"] = (
    (~citations["citation_present"]) |
    (~citations["source_supports_claim"])
)

citations
                """
            ),
        ]
    ),
    "04_rag_governance_register.ipynb": notebook(
        [
            markdown_cell("# RAG Governance Register"),
            code_cell(
                """
import pandas as pd

register = pd.DataFrame({
    "artifact": [
        "rag_system_card",
        "source_registry_review",
        "chunking_review",
        "retrieval_evaluation",
        "citation_audit",
        "access_control_review",
        "prompt_injection_test"
    ],
    "status": [
        "complete",
        "in_review",
        "complete",
        "in_review",
        "planned",
        "complete",
        "planned"
    ],
    "owner": [
        "Model Governance",
        "Knowledge Management",
        "Search Engineering",
        "Evaluation",
        "Editorial Review",
        "Security",
        "Security"
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
