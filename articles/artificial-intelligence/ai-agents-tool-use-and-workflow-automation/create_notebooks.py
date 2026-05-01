"""
Create advanced Jupyter notebooks for AI Agents, Tool Use, and Workflow Automation.
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
    "01_tool_call_evaluation.ipynb": notebook(
        [
            markdown_cell("# Tool-Call Evaluation"),
            code_cell(
                """
import pandas as pd

tool_calls = pd.DataFrame({
    "tool_call_id": ["TC1", "TC2", "TC3", "TC4"],
    "tool_risk": ["read_only", "compute", "write", "sensitive"],
    "argument_validity": [0.95, 0.72, 0.66, 0.89],
    "permission_compliance": [0.98, 0.91, 0.82, 0.76],
    "execution_success": [True, True, False, True]
})

tool_calls["review_required"] = (
    (tool_calls["argument_validity"] < 0.70) |
    (tool_calls["permission_compliance"] < 0.80) |
    (~tool_calls["execution_success"]) |
    (tool_calls["tool_risk"].isin(["sensitive"]))
)

tool_calls
                """
            ),
        ]
    ),
    "02_workflow_trace_review.ipynb": notebook(
        [
            markdown_cell("# Workflow Trace Review"),
            code_cell(
                """
import pandas as pd

trace = pd.DataFrame({
    "step": [1, 2, 3, 4],
    "action": ["retrieve", "calculate", "draft", "request_approval"],
    "status": ["success", "success", "success", "pending"],
    "requires_review": [False, False, False, True]
})

trace
                """
            ),
        ]
    ),
    "03_permission_testing.ipynb": notebook(
        [
            markdown_cell("# Permission Testing"),
            code_cell(
                """
import pandas as pd

permissions = pd.DataFrame({
    "user_group": ["analyst", "analyst", "admin", "guest"],
    "tool": ["query_db", "delete_record", "delete_record", "query_db"],
    "expected_decision": ["allow", "deny", "allow", "deny"],
    "actual_decision": ["allow", "deny", "allow", "allow"]
})

permissions["permission_test_passed"] = (
    permissions["expected_decision"] == permissions["actual_decision"]
)

permissions
                """
            ),
        ]
    ),
    "04_agent_governance_register.ipynb": notebook(
        [
            markdown_cell("# Agent Governance Register"),
            code_cell(
                """
import pandas as pd

register = pd.DataFrame({
    "artifact": [
        "agent_system_card",
        "tool_registry_review",
        "permission_review",
        "sandbox_review",
        "human_approval_review",
        "incident_response_plan",
        "deployment_readiness_checklist"
    ],
    "status": [
        "complete",
        "in_review",
        "complete",
        "planned",
        "in_review",
        "complete",
        "planned"
    ],
    "owner": [
        "Model Governance",
        "Platform Engineering",
        "Security",
        "Security",
        "Operations",
        "Operations",
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
