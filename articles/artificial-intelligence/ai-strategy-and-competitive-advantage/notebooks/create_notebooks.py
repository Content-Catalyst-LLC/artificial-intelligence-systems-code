#!/usr/bin/env python3
"""
Create advanced Jupyter notebooks for:
AI Strategy and Competitive Advantage
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


portfolio_code = """
import pandas as pd

initiatives = pd.DataFrame([
    {
        "initiative": "customer_support_copilot",
        "business_value": 0.75,
        "defensibility": 0.35,
        "data_readiness": 0.70,
        "workflow_fit": 0.80,
        "governance_maturity": 0.65,
        "platform_dependence": 0.70,
        "value_capture": 0.45,
    },
    {
        "initiative": "proprietary_workflow_intelligence",
        "business_value": 0.70,
        "defensibility": 0.85,
        "data_readiness": 0.75,
        "workflow_fit": 0.78,
        "governance_maturity": 0.72,
        "platform_dependence": 0.35,
        "value_capture": 0.80,
    },
    {
        "initiative": "regulated_decision_support",
        "business_value": 0.82,
        "defensibility": 0.78,
        "data_readiness": 0.62,
        "workflow_fit": 0.70,
        "governance_maturity": 0.88,
        "platform_dependence": 0.45,
        "value_capture": 0.76,
    },
])

initiatives
"""

write(
    NOTEBOOK_DIR / "01_ai_strategy_portfolio_scoring_lab.ipynb",
    "AI Strategy Portfolio Scoring Lab",
    [
        md("""
        ## Purpose

        This lab scores AI initiatives across business value, readiness, governance, defensibility, dependence, and value capture.
        """),
        code(portfolio_code),
        code("""
initiatives["capability_score"] = (
    0.25 * initiatives["business_value"]
    + 0.20 * initiatives["data_readiness"]
    + 0.20 * initiatives["workflow_fit"]
    + 0.20 * initiatives["governance_maturity"]
    + 0.15 * initiatives["defensibility"]
)

initiatives["strategic_advantage_score"] = (
    initiatives["capability_score"]
    * initiatives["defensibility"]
    * initiatives["value_capture"]
    * (1 - 0.40 * initiatives["platform_dependence"])
)

initiatives.sort_values("strategic_advantage_score", ascending=False)
        """),
        md("""
        ## Interpretation

        High business value does not guarantee durable advantage when defensibility or value capture is weak.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "02_vrio_resources_and_defensibility_lab.ipynb",
    "VRIO Resources and Defensibility Lab",
    [
        md("""
        ## Purpose

        This lab applies a VRIO-style lens to AI-linked resources.
        """),
        code("""
import pandas as pd

resources = pd.DataFrame([
    {"resource": "proprietary_workflow_data", "valuable": 0.90, "rare": 0.80, "hard_to_imitate": 0.85, "organized": 0.75},
    {"resource": "generic_model_api_access", "valuable": 0.70, "rare": 0.10, "hard_to_imitate": 0.10, "organized": 0.70},
    {"resource": "trusted_regulated_brand", "valuable": 0.82, "rare": 0.65, "hard_to_imitate": 0.80, "organized": 0.72},
    {"resource": "workflow_specific_evaluation_system", "valuable": 0.78, "rare": 0.60, "hard_to_imitate": 0.74, "organized": 0.68},
])

resources["vrio_score"] = (
    0.30 * resources["valuable"]
    + 0.20 * resources["rare"]
    + 0.30 * resources["hard_to_imitate"]
    + 0.20 * resources["organized"]
)

resources.sort_values("vrio_score", ascending=False)
        """),
        md("""
        ## Interpretation

        Generic tool access is useful but rarely rare or hard to imitate. Proprietary data and organizational systems can be more defensible.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "03_make_buy_partner_and_platform_dependence_lab.ipynb",
    "Make, Buy, Partner, and Platform Dependence Lab",
    [
        md("""
        ## Purpose

        This lab compares sourcing options and platform dependence.
        """),
        code("""
import pandas as pd

sourcing = pd.DataFrame([
    {"option": "make", "control": 0.90, "defensibility": 0.85, "speed": 0.35, "cost": 0.80, "risk": 0.45},
    {"option": "buy", "control": 0.35, "defensibility": 0.25, "speed": 0.90, "cost": 0.35, "risk": 0.55},
    {"option": "partner", "control": 0.65, "defensibility": 0.60, "speed": 0.70, "cost": 0.55, "risk": 0.45},
    {"option": "hybrid", "control": 0.75, "defensibility": 0.72, "speed": 0.62, "cost": 0.60, "risk": 0.40},
])

sourcing["sourcing_fit"] = (
    0.25 * sourcing["control"]
    + 0.30 * sourcing["defensibility"]
    + 0.20 * sourcing["speed"]
    - 0.15 * sourcing["cost"]
    - 0.10 * sourcing["risk"]
)

sourcing.sort_values("sourcing_fit", ascending=False)
        """),
        md("""
        ## Interpretation

        The best sourcing choice is not always the fastest or cheapest. It depends on control, defensibility, speed, cost, and strategic risk.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "04_value_capture_governance_and_scaled_adoption_lab.ipynb",
    "Value Capture, Governance, and Scaled Adoption Lab",
    [
        md("""
        ## Purpose

        This lab models how value capture and governance affect strategic advantage.
        """),
        code("""
import pandas as pd

portfolio = pd.DataFrame([
    {"initiative": "generic_productivity_tools", "ai_value": 0.80, "defensibility": 0.20, "value_capture": 0.35, "governance": 0.55},
    {"initiative": "workflow_reinvention", "ai_value": 0.72, "defensibility": 0.75, "value_capture": 0.78, "governance": 0.70},
    {"initiative": "regulated_ai_decision_support", "ai_value": 0.68, "defensibility": 0.80, "value_capture": 0.74, "governance": 0.90},
    {"initiative": "customer_data_learning_loop", "ai_value": 0.76, "defensibility": 0.88, "value_capture": 0.82, "governance": 0.76},
])

portfolio["trust_adjusted_advantage"] = (
    portfolio["ai_value"]
    * portfolio["defensibility"]
    * portfolio["value_capture"]
    * portfolio["governance"]
)

portfolio.sort_values("trust_adjusted_advantage", ascending=False)
        """),
        md("""
        ## Interpretation

        AI value becomes strategically meaningful when firms capture the surplus and govern the system well enough to scale it.
        """),
    ],
)
