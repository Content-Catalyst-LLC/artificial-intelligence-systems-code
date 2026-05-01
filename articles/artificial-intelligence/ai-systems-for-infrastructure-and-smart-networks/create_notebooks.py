"""
Create advanced Jupyter notebooks for AI Systems for Infrastructure and Smart Networks.
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
    "01_graph_modeling_for_infrastructure.ipynb": notebook(
        [
            markdown_cell("# Graph Modeling for Infrastructure"),
            code_cell(
                """
import numpy as np
import pandas as pd

nodes = pd.DataFrame({
    "node_id": [f"N{i:03d}" for i in range(20)],
    "asset_age": np.random.default_rng(42).normal(20, 5, 20).clip(1)
})

edges = pd.DataFrame({
    "source": [f"N{i:03d}" for i in range(19)],
    "target": [f"N{i+1:03d}" for i in range(19)]
})

degree = pd.concat([edges["source"], edges["target"]]).value_counts()
nodes["degree_centrality"] = nodes["node_id"].map(degree).fillna(0)
nodes
                """
            ),
        ]
    ),
    "02_digital_twin_scenario_simulation.ipynb": notebook(
        [
            markdown_cell("# Digital Twin Scenario Simulation"),
            code_cell(
                """
import numpy as np
import pandas as pd

rng = np.random.default_rng(7)

days = np.arange(1, 91)
baseline_demand = 100 + 20 * np.sin(days / 14)
heat_stress = np.where(days > 60, 1.25, 1.0)
scenario_demand = baseline_demand * heat_stress + rng.normal(0, 4, len(days))

pd.DataFrame({
    "day": days,
    "baseline_demand": baseline_demand,
    "scenario_demand": scenario_demand
}).head()
                """
            ),
        ]
    ),
    "03_cascade_and_resilience_analysis.ipynb": notebook(
        [
            markdown_cell("# Cascade and Resilience Analysis"),
            code_cell(
                """
import numpy as np
import pandas as pd

days = np.arange(1, 121)
shock_day = 20
performance = []

for day in days:
    if day < shock_day:
        performance.append(1.0)
    else:
        damage = 0.55 * np.exp(-0.045 * (day - shock_day))
        performance.append(max(0, min(1, 1 - damage)))

resilience_index = np.mean(performance)

pd.DataFrame({
    "day": days,
    "normalized_performance": performance
}).assign(resilience_index=resilience_index).head()
                """
            ),
        ]
    ),
    "04_infrastructure_governance_register.ipynb": notebook(
        [
            markdown_cell("# Infrastructure Governance Register"),
            code_cell(
                """
import pandas as pd

register = pd.DataFrame({
    "governance_artifact": [
        "asset_inventory",
        "sensor_calibration_register",
        "digital_twin_scope",
        "equity_review",
        "cybersecurity_review",
        "incident_response_plan"
    ],
    "status": [
        "complete",
        "in_review",
        "complete",
        "planned",
        "in_review",
        "complete"
    ],
    "owner": [
        "Infrastructure Operations",
        "Field Engineering",
        "Digital Twin Team",
        "Public Accountability",
        "Security",
        "Emergency Management"
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
