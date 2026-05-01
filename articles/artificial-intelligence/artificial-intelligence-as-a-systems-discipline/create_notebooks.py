"""
Create advanced Jupyter notebooks for Artificial Intelligence as a Systems Discipline.
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
    "01_ai_system_maturity_scoring.ipynb": notebook(
        [
            markdown_cell("# AI System Maturity Scoring"),
            code_cell(
                """
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

systems = pd.DataFrame({
    "system_id": [f"AI-SYS-{i:03d}" for i in range(50)],
    "technical_maturity": rng.uniform(0.4, 0.95, 50),
    "governance_maturity": rng.uniform(0.3, 0.95, 50),
    "external_impact": rng.uniform(0.05, 0.9, 50)
})

systems["system_maturity"] = 0.5 * systems["technical_maturity"] + 0.5 * systems["governance_maturity"]
systems["systemic_risk"] = 0.6 * (1 - systems["system_maturity"]) + 0.4 * systems["external_impact"]
systems.sort_values("systemic_risk", ascending=False).head()
                """
            ),
        ]
    ),
    "02_feedback_loops_lifecycle_risk.ipynb": notebook(
        [
            markdown_cell("# Feedback Loops and Lifecycle Risk"),
            code_cell(
                """
import numpy as np
import pandas as pd

periods = np.arange(1, 61)
data_quality = 0.8 - 0.003 * periods + np.random.default_rng(7).normal(0, 0.02, len(periods))
monitoring_strength = 0.65 + 0.002 * periods
risk = 0.55 * (1 - data_quality) + 0.45 * (1 - monitoring_strength)

pd.DataFrame({
    "period": periods,
    "data_quality": data_quality,
    "monitoring_strength": monitoring_strength,
    "systemic_risk": risk
}).head()
                """
            ),
        ]
    ),
    "03_governance_evidence_register.ipynb": notebook(
        [
            markdown_cell("# Governance Evidence Register"),
            code_cell(
                """
import pandas as pd

register = pd.DataFrame({
    "artifact": [
        "intended_use_statement",
        "data_provenance_record",
        "validation_report",
        "subgroup_performance_review",
        "monitoring_plan",
        "incident_response_plan",
        "retirement_criteria"
    ],
    "status": [
        "complete",
        "complete",
        "in_review",
        "planned",
        "complete",
        "complete",
        "planned"
    ],
    "owner": [
        "Product Owner",
        "Data Steward",
        "Model Validation",
        "Governance",
        "MLOps",
        "Risk",
        "Governance"
    ]
})

register
                """
            ),
        ]
    ),
    "04_portfolio_remediation_planning.ipynb": notebook(
        [
            markdown_cell("# Portfolio Remediation Planning"),
            code_cell(
                """
import pandas as pd

portfolio = pd.DataFrame({
    "system_id": ["AI-SYS-001", "AI-SYS-002", "AI-SYS-003"],
    "systemic_risk": [0.28, 0.61, 0.47],
    "governance_gap": [0.10, 0.42, 0.31],
    "monitoring_gap": [0.12, 0.36, 0.44]
})

portfolio["priority"] = pd.cut(
    portfolio["systemic_risk"],
    bins=[0, 0.35, 0.55, 1.0],
    labels=["monitor", "review", "remediate"]
)

portfolio
                """
            ),
        ]
    ),
}

for filename, nb in notebooks.items():
    path = NOTEBOOK_DIR / filename
    path.write_text(json.dumps(nb, indent=2))
    print(f"Created {path}")
