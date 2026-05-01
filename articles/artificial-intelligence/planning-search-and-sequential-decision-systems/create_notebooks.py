"""
Create advanced Jupyter notebooks for Planning, Search, and Sequential Decision Systems.
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
    "01_state_space_search.ipynb": notebook(
        [
            markdown_cell("# State-Space Search"),
            code_cell(
                """
import pandas as pd

nodes = pd.DataFrame({
    "node": ["A", "B", "C", "D"],
    "path_cost": [0, 2, 3, 5],
    "heuristic": [6, 4, 2, 0]
})

nodes["priority"] = nodes["path_cost"] + nodes["heuristic"]
nodes.sort_values("priority")
                """
            ),
        ]
    ),
    "02_value_iteration_summary.ipynb": notebook(
        [
            markdown_cell("# Value Iteration Summary"),
            code_cell(
                """
import pandas as pd

states = pd.DataFrame({
    "state": ["s1", "s2", "s3"],
    "value_old": [0.10, 0.35, 0.80],
    "value_new": [0.18, 0.42, 0.92]
})

states["value_change"] = (states["value_new"] - states["value_old"]).abs()
states
                """
            ),
        ]
    ),
    "03_agent_planning_trace.ipynb": notebook(
        [
            markdown_cell("# Agent Planning Trace"),
            code_cell(
                """
import pandas as pd

trace = pd.DataFrame({
    "step": [1, 2, 3, 4],
    "action_type": ["retrieve", "analyze", "tool_call", "human_review"],
    "risk_level": ["low", "low", "medium", "high"],
    "approved": [True, True, True, False]
})

trace["requires_review"] = trace["risk_level"].isin(["medium", "high"])
trace
                """
            ),
        ]
    ),
    "04_planning_governance_register.ipynb": notebook(
        [
            markdown_cell("# Planning Governance Register"),
            code_cell(
                """
import pandas as pd

register = pd.DataFrame({
    "artifact": [
        "planning_system_card",
        "action_registry_review",
        "reward_review",
        "policy_evaluation",
        "human_approval_gate",
        "rollback_readiness",
        "incident_response",
        "deployment_readiness"
    ],
    "status": [
        "complete",
        "in_review",
        "complete",
        "planned",
        "complete",
        "planned",
        "in_review",
        "planned"
    ],
    "owner": [
        "Model Governance",
        "Security",
        "Risk",
        "ML Engineering",
        "Operations",
        "Platform",
        "Incident Response",
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
