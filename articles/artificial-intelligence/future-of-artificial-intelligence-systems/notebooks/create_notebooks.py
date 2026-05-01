#!/usr/bin/env python3
"""
Create advanced Jupyter notebooks for:
The Future of Artificial Intelligence Systems
"""

from __future__ import annotations

import json
from pathlib import Path
from textwrap import dedent


NOTEBOOK_DIR = Path(".")


def md(text: str) -> dict:
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": dedent(text).strip().splitlines(keepends=True),
    }


def code(text: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": dedent(text).strip().splitlines(keepends=True),
    }


def notebook(title: str, cells: list[dict]) -> dict:
    return {
        "cells": [
            {"cell_type": "markdown", "metadata": {}, "source": [f"# {title}\n"]},
            *cells,
        ],
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.x"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def write(path: Path, title: str, cells: list[dict]) -> None:
    path.write_text(json.dumps(notebook(title, cells), indent=2), encoding="utf-8")
    print(f"created {path}")


write(
    NOTEBOOK_DIR / "01_scaling_laws_compute_efficiency_and_capability_trajectories_lab.ipynb",
    "Scaling Laws, Compute Efficiency, and Capability Trajectories Lab",
    [
        md("""
        ## Purpose

        This lab simulates simplified scaling-law behavior and shows diminishing loss improvement with increasing scale.
        """),
        code("""
import numpy as np
import pandas as pd

scale = np.linspace(1, 100, 100)
loss_floor = 1.2
x0 = 35
alpha = 0.32

scaling_curve = pd.DataFrame({
    "scale": scale,
    "loss": loss_floor + (x0 / scale) ** alpha,
})

scaling_curve["marginal_loss_improvement"] = -scaling_curve["loss"].diff()

scaling_curve.head(), scaling_curve.tail()
        """),
        md("""
        ## Interpretation

        Scaling can improve loss predictably in simplified regimes, but marginal improvements may decline and do not automatically imply system-level fitness.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "02_system_fitness_governance_capacity_and_responsible_scaling_lab.ipynb",
    "System Fitness, Governance Capacity, and Responsible Scaling Lab",
    [
        md("""
        ## Purpose

        This lab compares AI systems using capability, efficiency, governance, trust, risk, and cost.
        """),
        code("""
import pandas as pd

systems = pd.DataFrame({
    "system": [
        "centralized_frontier",
        "compute_optimal_specialist",
        "distributed_edge_network",
        "hybrid_governed_platform",
        "undergoverned_agentic_stack",
    ],
    "capability": [0.95, 0.83, 0.74, 0.88, 0.91],
    "efficiency": [0.42, 0.86, 0.78, 0.74, 0.45],
    "governance_capacity": [0.62, 0.78, 0.70, 0.90, 0.38],
    "trust": [0.58, 0.80, 0.72, 0.86, 0.42],
    "systemic_risk": [0.72, 0.38, 0.44, 0.32, 0.86],
    "cost": [0.90, 0.48, 0.55, 0.62, 0.76],
})

systems["responsible_scaling_gap"] = systems["capability"] - systems["governance_capacity"]

systems["system_fitness"] = (
    0.30 * systems["capability"]
    + 0.18 * systems["efficiency"]
    + 0.22 * systems["governance_capacity"]
    + 0.18 * systems["trust"]
    - 0.20 * systems["systemic_risk"]
    - 0.12 * systems["cost"]
)

systems["governance_warning"] = systems["responsible_scaling_gap"] > 0.15

systems.sort_values("system_fitness", ascending=False)
        """),
        md("""
        ## Interpretation

        The best AI system is not necessarily the most capable model. Governance, cost, trust, efficiency, and risk shape practical system value.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "03_distributed_intelligence_platform_power_and_systemic_risk_lab.ipynb",
    "Distributed Intelligence, Platform Power, and Systemic Risk Lab",
    [
        md("""
        ## Purpose

        This lab scores AI architectures by concentration, dependency, resilience, and systemic risk.
        """),
        code("""
import pandas as pd

architectures = pd.DataFrame({
    "architecture": [
        "centralized_cloud_platform",
        "federated_learning_network",
        "edge_ai_mesh",
        "hybrid_cloud_edge_governed",
        "uncoordinated_agentic_ecosystem",
    ],
    "dependency_concentration": [0.90, 0.52, 0.38, 0.58, 0.75],
    "resilience": [0.48, 0.72, 0.80, 0.82, 0.42],
    "interoperability": [0.55, 0.68, 0.62, 0.78, 0.40],
    "governance_visibility": [0.62, 0.70, 0.58, 0.86, 0.35],
})

architectures["systemic_risk_score"] = (
    0.40 * architectures["dependency_concentration"]
    - 0.25 * architectures["resilience"]
    - 0.15 * architectures["interoperability"]
    - 0.20 * architectures["governance_visibility"]
)

architectures.sort_values("systemic_risk_score", ascending=False)
        """),
        md("""
        ## Interpretation

        Systemic risk rises when dependency concentration is high and resilience, interoperability, and governance visibility are weak.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "04_future_scenarios_constraints_and_institutional_capacity_lab.ipynb",
    "Future Scenarios, Constraints, and Institutional Capacity Lab",
    [
        md("""
        ## Purpose

        This lab scores future AI scenarios across capability, infrastructure, governance, resilience, legitimacy, and risk.
        """),
        code("""
import pandas as pd

scenarios = pd.DataFrame({
    "scenario": [
        "centralized_frontier_dominance",
        "distributed_intelligence_networks",
        "hybrid_public_private_infrastructure",
        "regulated_high_risk_ai",
        "governance_lag_and_systemic_fragility",
    ],
    "capability": [0.95, 0.74, 0.86, 0.80, 0.88],
    "infrastructure": [0.88, 0.70, 0.82, 0.75, 0.66],
    "governance": [0.55, 0.68, 0.84, 0.90, 0.35],
    "resilience": [0.52, 0.78, 0.80, 0.74, 0.40],
    "legitimacy": [0.50, 0.72, 0.82, 0.86, 0.34],
    "systemic_risk": [0.78, 0.46, 0.38, 0.42, 0.90],
})

scenarios["scenario_score"] = (
    0.22 * scenarios["capability"]
    + 0.18 * scenarios["infrastructure"]
    + 0.22 * scenarios["governance"]
    + 0.18 * scenarios["resilience"]
    + 0.15 * scenarios["legitimacy"]
    - 0.20 * scenarios["systemic_risk"]
)

scenarios["governance_gap"] = scenarios["capability"] - scenarios["governance"]

scenarios["risk_warning"] = (
    (scenarios["governance_gap"] > 0.20)
    | (scenarios["systemic_risk"] > 0.70)
)

scenarios.sort_values("scenario_score", ascending=False)
        """),
        md("""
        ## Interpretation

        Future AI trajectories should be evaluated through institutional capacity and system constraints, not capability alone.
        """),
    ],
)
