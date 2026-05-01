"""
Create advanced Jupyter notebooks for Generative AI and Synthetic Content Systems.
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
    "01_distribution_learning_and_sampling.ipynb": notebook(
        [
            markdown_cell("# Distribution Learning and Sampling"),
            code_cell(
                """
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

samples = pd.DataFrame({
    "latent_1": rng.normal(0, 1, 500),
    "latent_2": rng.normal(0, 1, 500)
})

samples["quality_proxy"] = 1 / (1 + np.exp(-(1.2 * samples["latent_1"] - 0.4 * samples["latent_2"])))
samples.head()
                """
            ),
        ]
    ),
    "02_decoding_temperature_controls.ipynb": notebook(
        [
            markdown_cell("# Decoding Temperature Controls"),
            code_cell(
                """
import numpy as np
import pandas as pd

tokens = pd.DataFrame({
    "token": ["alpha", "beta", "gamma", "delta", "epsilon"],
    "logit": [3.2, 2.7, 1.8, 0.9, 0.2]
})

def softmax_temperature(logits, temperature):
    scaled = logits / temperature
    exp_values = np.exp(scaled - scaled.max())
    return exp_values / exp_values.sum()

for temperature in [0.5, 1.0, 1.5]:
    tokens[f"prob_T_{temperature}"] = softmax_temperature(tokens["logit"].to_numpy(), temperature)

tokens
                """
            ),
        ]
    ),
    "03_synthetic_content_risk_review.ipynb": notebook(
        [
            markdown_cell("# Synthetic Content Risk Review"),
            code_cell(
                """
import pandas as pd

review = pd.DataFrame({
    "artifact_id": ["G001", "G002", "G003"],
    "grounding_score": [0.82, 0.44, 0.76],
    "provenance_score": [0.91, 0.72, 0.31],
    "policy_risk": [0.12, 0.22, 0.28]
})

review["review_required"] = (
    (review["grounding_score"] < 0.50)
    | (review["provenance_score"] < 0.45)
    | (review["policy_risk"] > 0.45)
)

review
                """
            ),
        ]
    ),
    "04_synthetic_content_governance_register.ipynb": notebook(
        [
            markdown_cell("# Synthetic Content Governance Register"),
            code_cell(
                """
import pandas as pd

register = pd.DataFrame({
    "artifact": [
        "prompt_hash",
        "model_version",
        "output_hash",
        "content_credentials",
        "human_review_record",
        "publication_decision"
    ],
    "status": [
        "complete",
        "complete",
        "complete",
        "in_review",
        "complete",
        "planned"
    ],
    "owner": [
        "AI Operations",
        "Model Governance",
        "Content Operations",
        "Provenance Lead",
        "Editorial Review",
        "Publisher"
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
