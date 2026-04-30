#!/usr/bin/env python3
"""
Create advanced Jupyter notebooks for:
Asset Management and Predictive Maintenance Systems
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
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [f"# {title}\n"],
            },
            *cells,
        ],
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


def write(path: Path, title: str, cells: list[dict]) -> None:
    path.write_text(json.dumps(notebook(title, cells), indent=2), encoding="utf-8")
    print(f"created {path}")


write(
    NOTEBOOK_DIR / "01_asset_register_condition_and_criticality_lab.ipynb",
    "Asset Register, Condition, and Criticality Lab",
    [
        md("""
        ## Purpose

        This lab introduces asset registers, condition scores, service consequence, and criticality-based prioritization.

        Learning goals:

        - Build a synthetic asset register.
        - Score condition and failure probability.
        - Combine condition and consequence into risk.
        - Rank assets for maintenance review.
        """),
        code("""
        import numpy as np
        import pandas as pd

        rng = np.random.default_rng(42)

        n_assets = 250

        assets = pd.DataFrame({
            "asset_id": [f"A-{i:04d}" for i in range(1, n_assets + 1)],
            "asset_class": rng.choice(
                ["pump", "valve", "bridge_component", "road_segment", "substation_asset"],
                size=n_assets,
                p=[0.20, 0.20, 0.20, 0.25, 0.15],
            ),
            "age_years": rng.integers(1, 60, size=n_assets),
            "condition_score": rng.uniform(0.15, 0.98, size=n_assets),
            "service_consequence": rng.integers(1, 6, size=n_assets),
            "environmental_exposure": rng.uniform(0.0, 1.0, size=n_assets),
        })

        linear_risk = (
            -3.0
            + 0.045 * assets["age_years"]
            + 2.5 * (1 - assets["condition_score"])
            + 0.9 * assets["environmental_exposure"]
        )

        assets["failure_probability"] = 1 / (1 + np.exp(-linear_risk))
        assets["risk_score"] = assets["failure_probability"] * assets["service_consequence"]

        assets.sort_values("risk_score", ascending=False).head(10)
        """),
        md("""
        ## Interpretation

        Asset priority depends on both condition and consequence. A moderately degraded but critical asset may outrank a severely degraded low-consequence asset.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "02_predictive_maintenance_remaining_useful_life_lab.ipynb",
    "Predictive Maintenance and Remaining Useful Life Lab",
    [
        md("""
        ## Purpose

        This lab simulates condition deterioration and remaining useful life.

        Learning goals:

        - Simulate asset condition trajectories.
        - Estimate time to threshold.
        - Interpret remaining useful life as a decision-support concept.
        """),
        code("""
        import numpy as np
        import pandas as pd

        rng = np.random.default_rng(42)

        assets = pd.DataFrame({
            "asset_id": [f"A-{i:03d}" for i in range(1, 31)],
            "initial_condition": rng.uniform(0.55, 0.98, size=30),
            "annual_deterioration": rng.uniform(0.015, 0.065, size=30),
        })

        threshold = 0.35
        horizon = 30

        rows = []

        for _, asset in assets.iterrows():
            for year in range(horizon + 1):
                condition = asset["initial_condition"] - year * asset["annual_deterioration"]
                rows.append({
                    "asset_id": asset["asset_id"],
                    "year": year,
                    "condition": max(condition, 0),
                })

        trajectory = pd.DataFrame(rows)

        rul = (
            trajectory[trajectory["condition"] <= threshold]
            .groupby("asset_id", as_index=False)
            .agg(remaining_useful_life_years=("year", "min"))
        )

        assets.merge(rul, on="asset_id", how="left").head()
        """),
        md("""
        ## Interpretation

        Remaining useful life is not a fixed truth. It depends on deterioration assumptions, intervention effects, condition thresholds, and uncertainty.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "03_lifecycle_cost_and_strategy_comparison_lab.ipynb",
    "Lifecycle Cost and Strategy Comparison Lab",
    [
        md("""
        ## Purpose

        This lab compares simplified maintenance strategies using discounted lifecycle cost.

        Learning goals:

        - Compare reactive, preventive, and condition-based strategies.
        - Include maintenance and expected failure cost.
        - Interpret lifecycle cost as a governance tool.
        """),
        code("""
        import numpy as np
        import pandas as pd

        discount_rate = 0.03
        years = np.arange(0, 31)

        strategies = pd.DataFrame([
            {"strategy": "reactive", "annual_maintenance": 5000, "failure_probability": 0.09, "failure_cost": 250000},
            {"strategy": "preventive", "annual_maintenance": 14000, "failure_probability": 0.045, "failure_cost": 250000},
            {"strategy": "condition_based", "annual_maintenance": 18000, "failure_probability": 0.030, "failure_cost": 250000},
            {"strategy": "predictive", "annual_maintenance": 26000, "failure_probability": 0.020, "failure_cost": 250000},
        ])

        rows = []

        for _, strategy in strategies.iterrows():
            for year in years:
                discount_factor = 1 / ((1 + discount_rate) ** year)
                expected_cost = (
                    strategy["annual_maintenance"]
                    + strategy["failure_probability"] * strategy["failure_cost"]
                ) * discount_factor

                rows.append({
                    "strategy": strategy["strategy"],
                    "year": year,
                    "discounted_expected_cost": expected_cost,
                })

        costs = pd.DataFrame(rows)

        summary = (
            costs
            .groupby("strategy", as_index=False)
            .agg(total_discounted_expected_cost=("discounted_expected_cost", "sum"))
            .sort_values("total_discounted_expected_cost")
        )

        summary
        """),
        md("""
        ## Interpretation

        Higher annual maintenance cost can still reduce lifecycle cost if it meaningfully lowers failure risk and emergency consequence.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "04_governance_digital_twins_and_asset_auditability_lab.ipynb",
    "Governance, Digital Twins, and Asset Auditability Lab",
    [
        md("""
        ## Purpose

        This lab frames asset-management analytics as a governance system.

        Learning goals:

        - Track evidence required for asset decisions.
        - Map analytics outputs to accountable owners.
        - Connect digital-twin assumptions to review procedures.
        """),
        code("""
        import pandas as pd

        governance_checklist = pd.DataFrame([
            {
                "layer": "asset_register",
                "audit_question": "Are all critical assets represented with ownership, location, and class?",
                "evidence": "asset register extract",
                "owner": "Asset Data Steward",
            },
            {
                "layer": "condition_monitoring",
                "audit_question": "How current and reliable are condition scores?",
                "evidence": "inspection records and sensor quality flags",
                "owner": "Maintenance Engineering",
            },
            {
                "layer": "predictive_model",
                "audit_question": "Has the failure model been validated against history and field judgment?",
                "evidence": "validation report and model card",
                "owner": "Analytics Lead",
            },
            {
                "layer": "work_execution",
                "audit_question": "Do predictive alerts translate into work orders and completed interventions?",
                "evidence": "work-order linkage table",
                "owner": "Operations Manager",
            },
            {
                "layer": "budget_governance",
                "audit_question": "Are deferred maintenance risks visible in financial planning?",
                "evidence": "lifecycle cost and renewal plan",
                "owner": "Finance Lead",
            },
            {
                "layer": "digital_twin",
                "audit_question": "Are model assumptions, update frequency, and scenario limits documented?",
                "evidence": "digital twin documentation",
                "owner": "Systems Engineering",
            },
        ])

        governance_checklist
        """),
        md("""
        ## Interpretation

        Predictive maintenance becomes trustworthy when model outputs are connected to evidence, work execution, budget, and accountable governance.
        """),
    ],
)
