"""
Create advanced Jupyter notebooks for Artificial Intelligence in Decision Support Systems.
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
    "01_expected_utility_decision_theory.ipynb": notebook(
        [
            markdown_cell("# Expected Utility and Decision Theory"),
            code_cell(
                """
import numpy as np
import pandas as pd

actions = pd.DataFrame({
    "action": ["A", "B", "C"],
    "prob_success": [0.65, 0.45, 0.80],
    "benefit": [100, 150, 70],
    "cost": [30, 40, 20]
})

actions["expected_utility"] = actions["prob_success"] * actions["benefit"] - actions["cost"]
actions.sort_values("expected_utility", ascending=False)
                """
            ),
        ]
    ),
    "02_causal_decision_support.ipynb": notebook(
        [
            markdown_cell("# Causal Decision Support Sketch"),
            code_cell(
                """
import pandas as pd

effects = pd.DataFrame({
    "intervention": ["follow_up", "transport_support", "remote_monitoring"],
    "predicted_risk_reduction": [0.08, 0.12, 0.06],
    "cost": [20, 35, 18]
})

effects["effect_per_cost"] = effects["predicted_risk_reduction"] / effects["cost"]
effects.sort_values("effect_per_cost", ascending=False)
                """
            ),
        ]
    ),
    "03_robust_optimization_scenarios.ipynb": notebook(
        [
            markdown_cell("# Robust Optimization and Scenario Analysis"),
            code_cell(
                """
import numpy as np
import pandas as pd

options = pd.DataFrame({
    "option": ["A", "B", "C", "D"],
    "baseline": [50, 55, 47, 60],
    "optimistic": [70, 66, 62, 75],
    "pessimistic": [20, 35, 42, 10]
})

options["robust_score"] = options[["baseline", "optimistic", "pessimistic"]].min(axis=1)
options.sort_values("robust_score", ascending=False)
                """
            ),
        ]
    ),
    "04_decision_governance_register.ipynb": notebook(
        [
            markdown_cell("# Decision Governance Register"),
            code_cell(
                """
import pandas as pd

register = pd.DataFrame({
    "artifact": [
        "decision_question",
        "utility_function",
        "threshold_record",
        "human_review_policy",
        "override_log",
        "scenario_review"
    ],
    "status": [
        "complete",
        "in_review",
        "complete",
        "complete",
        "active",
        "planned"
    ],
    "owner": [
        "Decision Owner",
        "Analytics",
        "Governance",
        "Operations",
        "Operations",
        "Risk Review"
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
