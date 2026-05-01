"""
Create advanced Jupyter notebooks for Representation Learning and Embedding Spaces.
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
    "01_embedding_geometry.ipynb": notebook(
        [
            markdown_cell("# Embedding Geometry"),
            code_cell(
                """
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

vectors = rng.normal(size=(10, 8))
vectors = vectors / np.linalg.norm(vectors, axis=1, keepdims=True)

similarity = vectors @ vectors.T

pd.DataFrame(similarity).round(3)
                """
            ),
        ]
    ),
    "02_semantic_retrieval.ipynb": notebook(
        [
            markdown_cell("# Semantic Retrieval Sketch"),
            code_cell(
                """
import numpy as np
import pandas as pd

documents = pd.DataFrame({
    "doc_id": ["D001", "D002", "D003"],
    "title": ["AI Safety", "Data Governance", "Semantic Search"],
    "similarity": [0.42, 0.31, 0.86],
    "authority_score": [0.92, 0.89, 0.88]
})

documents["retrieval_score"] = 0.75 * documents["similarity"] + 0.25 * documents["authority_score"]
documents.sort_values("retrieval_score", ascending=False)
                """
            ),
        ]
    ),
    "03_embedding_bias_review.ipynb": notebook(
        [
            markdown_cell("# Embedding Bias Review"),
            code_cell(
                """
import pandas as pd

review = pd.DataFrame({
    "test_group": ["group_a", "group_b", "group_c"],
    "mean_similarity_to_positive_terms": [0.62, 0.54, 0.48],
    "mean_similarity_to_negative_terms": [0.22, 0.31, 0.39]
})

review["association_gap"] = (
    review["mean_similarity_to_positive_terms"]
    - review["mean_similarity_to_negative_terms"]
)

review
                """
            ),
        ]
    ),
    "04_vector_system_governance_register.ipynb": notebook(
        [
            markdown_cell("# Vector System Governance Register"),
            code_cell(
                """
import pandas as pd

register = pd.DataFrame({
    "artifact": [
        "embedding_model_card",
        "vector_index_record",
        "retrieval_evaluation_set",
        "bias_review",
        "drift_monitoring_record",
        "refresh_policy"
    ],
    "status": [
        "complete",
        "complete",
        "in_review",
        "planned",
        "active",
        "complete"
    ],
    "owner": [
        "Model Governance",
        "Search Infrastructure",
        "Evaluation Team",
        "Responsible AI",
        "MLOps",
        "Search Infrastructure"
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
