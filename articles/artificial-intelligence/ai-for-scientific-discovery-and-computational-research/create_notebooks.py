"""
Create advanced Jupyter notebooks for AI for Scientific Discovery and Computational Research.
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
    "01_representation_learning_sketch.ipynb": notebook(
        [
            markdown_cell("# Representation Learning Sketch"),
            code_cell(
                """
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

data = pd.DataFrame({
    "feature_1": rng.normal(0, 1, 500),
    "feature_2": rng.normal(0, 1, 500),
    "feature_3": rng.normal(0, 1, 500)
})

data["latent_representation"] = (
    0.5 * data["feature_1"]
    - 0.2 * data["feature_2"]
    + 0.8 * data["feature_3"]
)

data.head()
                """
            ),
        ]
    ),
    "02_active_learning_candidate_selection.ipynb": notebook(
        [
            markdown_cell("# Active Learning Candidate Selection"),
            code_cell(
                """
import numpy as np
import pandas as pd

rng = np.random.default_rng(7)

candidates = pd.DataFrame({
    "candidate_id": [f"C{i:03d}" for i in range(100)],
    "predicted_property": rng.normal(1.5, 0.4, 100),
    "uncertainty": rng.uniform(0, 1, 100),
    "cost": rng.uniform(0.2, 0.9, 100),
    "safety_penalty": rng.choice([0, 0.25], size=100, p=[0.85, 0.15])
})

candidates["acquisition_score"] = (
    0.60 * candidates["predicted_property"]
    + 0.30 * candidates["uncertainty"]
    - 0.20 * candidates["cost"]
    - 0.40 * candidates["safety_penalty"]
)

candidates.sort_values("acquisition_score", ascending=False).head()
                """
            ),
        ]
    ),
    "03_surrogate_modeling_and_validation.ipynb": notebook(
        [
            markdown_cell("# Surrogate Modeling and Validation"),
            code_cell(
                """
import numpy as np
import pandas as pd

rng = np.random.default_rng(11)

x = rng.uniform(0, 1, 200)
true_y = np.sin(np.pi * x) + rng.normal(0, 0.05, 200)

approx_y = np.polyval(np.polyfit(x, true_y, deg=3), x)
rmse = np.sqrt(np.mean((true_y - approx_y) ** 2))

pd.DataFrame({
    "metric": ["surrogate_rmse"],
    "value": [rmse]
})
                """
            ),
        ]
    ),
    "04_reproducibility_governance_register.ipynb": notebook(
        [
            markdown_cell("# Reproducibility Governance Register"),
            code_cell(
                """
import pandas as pd

register = pd.DataFrame({
    "artifact": [
        "dataset_manifest",
        "code_version",
        "environment_file",
        "random_seed_record",
        "validation_report",
        "reproducibility_review"
    ],
    "status": [
        "complete",
        "complete",
        "complete",
        "complete",
        "in_review",
        "planned"
    ],
    "owner": [
        "Data Steward",
        "Research Software",
        "Research Software",
        "Modeling Team",
        "Scientific Reviewer",
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
