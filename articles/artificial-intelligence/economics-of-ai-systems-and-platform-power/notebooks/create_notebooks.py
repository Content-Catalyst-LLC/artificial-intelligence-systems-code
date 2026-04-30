#!/usr/bin/env python3
"""
Create advanced Jupyter notebooks for:
Economics of AI Systems and Platform Power
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


ecosystem_code = """
import pandas as pd

actors = pd.DataFrame([
    {"actor": "cloud_compute_provider", "layer": "infrastructure", "market_share": 0.36, "captured_surplus": 35.0},
    {"actor": "foundation_model_provider", "layer": "model", "market_share": 0.28, "captured_surplus": 25.0},
    {"actor": "enterprise_application_firm", "layer": "application", "market_share": 0.18, "captured_surplus": 20.0},
    {"actor": "downstream_users", "layer": "user", "market_share": 0.18, "captured_surplus": 20.0},
])

actors["value_capture_share"] = actors["captured_surplus"] / actors["captured_surplus"].sum()
actors
"""

write(
    NOTEBOOK_DIR / "01_ai_value_chain_and_surplus_distribution_lab.ipynb",
    "AI Value Chain and Surplus Distribution Lab",
    [
        md("""
        ## Purpose

        This lab examines how AI-created surplus can be distributed across infrastructure, model, application, and user layers.
        """),
        code(ecosystem_code),
        code("""
total_surplus = actors["captured_surplus"].sum()

summary = actors[["actor", "layer", "captured_surplus", "value_capture_share"]].sort_values(
    "captured_surplus",
    ascending=False,
)

total_surplus, summary
        """),
        md("""
        ## Interpretation

        Value creation and value capture are not the same. Surplus may shift toward actors with bottleneck control.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "02_platform_power_concentration_and_gatekeeping_lab.ipynb",
    "Platform Power, Concentration, and Gatekeeping Lab",
    [
        md("""
        ## Purpose

        This lab scores platform power using concentration, data control, distribution control, switching costs, and gatekeeping.
        """),
        code("""
import pandas as pd

actors = pd.DataFrame([
    {"actor": "cloud_compute_provider", "market_share": 0.36, "data_control": 0.45, "distribution_control": 0.55, "switching_costs": 0.80, "gatekeeping_power": 0.85},
    {"actor": "foundation_model_provider", "market_share": 0.28, "data_control": 0.70, "distribution_control": 0.60, "switching_costs": 0.65, "gatekeeping_power": 0.72},
    {"actor": "enterprise_application_firm", "market_share": 0.18, "data_control": 0.55, "distribution_control": 0.45, "switching_costs": 0.40, "gatekeeping_power": 0.35},
    {"actor": "downstream_users", "market_share": 0.18, "data_control": 0.20, "distribution_control": 0.10, "switching_costs": 0.25, "gatekeeping_power": 0.10},
])

concentration_score = (actors["market_share"] ** 2).sum()

actors["platform_power_score"] = (
    0.25 * actors["market_share"]
    + 0.20 * actors["data_control"]
    + 0.20 * actors["distribution_control"]
    + 0.20 * actors["switching_costs"]
    + 0.15 * actors["gatekeeping_power"]
)

actors.sort_values("platform_power_score", ascending=False), concentration_score
        """),
        md("""
        ## Interpretation

        Platform power is multidimensional. A firm may gain leverage through switching costs and gatekeeping even when market share alone is incomplete.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "03_compute_bottlenecks_cloud_dependence_and_switching_costs_lab.ipynb",
    "Compute Bottlenecks, Cloud Dependence, and Switching Costs Lab",
    [
        md("""
        ## Purpose

        This lab models dependency risk across compute, cloud, model APIs, and distribution layers.
        """),
        code("""
import pandas as pd

dependencies = pd.DataFrame([
    {"dependency": "GPU_cluster_access", "criticality": 0.90, "substitutability": 0.25, "switching_cost": 0.80},
    {"dependency": "cloud_AI_platform", "criticality": 0.82, "substitutability": 0.35, "switching_cost": 0.75},
    {"dependency": "foundation_model_API", "criticality": 0.76, "substitutability": 0.45, "switching_cost": 0.60},
    {"dependency": "enterprise_distribution_channel", "criticality": 0.70, "substitutability": 0.40, "switching_cost": 0.65},
])

dependencies["dependency_risk"] = (
    0.45 * dependencies["criticality"]
    + 0.35 * dependencies["switching_cost"]
    + 0.20 * (1 - dependencies["substitutability"])
)

dependencies.sort_values("dependency_risk", ascending=False)
        """),
        md("""
        ## Interpretation

        Dependency risk rises when a layer is critical, hard to substitute, and costly to switch away from.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "04_public_capacity_competition_policy_and_governance_lab.ipynb",
    "Public Capacity, Competition Policy, and Governance Lab",
    [
        md("""
        ## Purpose

        This lab frames AI platform economics as a governance evidence problem.
        """),
        code("""
import pandas as pd

governance_review = pd.DataFrame([
    {
        "area": "compute_access",
        "question": "Are critical compute dependencies documented?",
        "status": "partial",
        "owner": "Infrastructure / Procurement",
    },
    {
        "area": "interoperability",
        "question": "Can the organization switch providers without excessive lock-in?",
        "status": "partial",
        "owner": "Architecture",
    },
    {
        "area": "value_capture",
        "question": "Who captures the surplus generated by AI use?",
        "status": "missing",
        "owner": "Strategy",
    },
    {
        "area": "public_capacity",
        "question": "Can public institutions independently evaluate the AI stack?",
        "status": "missing",
        "owner": "Policy",
    },
    {
        "area": "competition_risk",
        "question": "Are vertical leverage and gatekeeping risks monitored?",
        "status": "partial",
        "owner": "Legal / Governance",
    },
])

governance_review.groupby("status").size().reset_index(name="count")
        """),
        md("""
        ## Interpretation

        AI platform governance requires evidence about dependence, interoperability, value capture, public capacity, and competition risk.
        """),
    ],
)
