#!/usr/bin/env python3
"""
Create advanced Jupyter notebooks for:
AI Systems in Organizations and Institutions
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


use_case_setup = """
import pandas as pd

use_cases = pd.DataFrame({
    "use_case": [
        "customer_support_routing",
        "employee_performance_review",
        "clinical_triage_support",
        "procurement_anomaly_detection",
        "public_benefits_eligibility",
        "infrastructure_emergency_response",
    ],
    "data_quality": [0.86, 0.62, 0.78, 0.82, 0.66, 0.74],
    "infrastructure": [0.82, 0.70, 0.76, 0.84, 0.68, 0.80],
    "staff_ai_literacy": [0.74, 0.58, 0.72, 0.76, 0.60, 0.70],
    "governance_maturity": [0.72, 0.50, 0.74, 0.78, 0.55, 0.82],
    "workflow_fit": [0.88, 0.44, 0.70, 0.86, 0.52, 0.68],
    "trust": [0.78, 0.42, 0.66, 0.80, 0.48, 0.70],
    "harm_potential": [0.20, 0.74, 0.86, 0.40, 0.88, 0.94],
    "rights_impact": [0.18, 0.82, 0.72, 0.24, 0.92, 0.70],
    "irreversibility": [0.14, 0.68, 0.78, 0.32, 0.75, 0.90],
    "opacity": [0.40, 0.66, 0.58, 0.50, 0.72, 0.52],
})
"""

write(
    NOTEBOOK_DIR / "01_organizational_information_processing_and_bounded_rationality_lab.ipynb",
    "Organizational Information Processing and Bounded Rationality Lab",
    [
        md("""
        ## Purpose

        This lab frames organizational AI adoption as an information-processing and bounded-rationality problem.
        """),
        code(use_case_setup),
        code("""
use_cases["ai_readiness"] = (
    0.20 * use_cases["data_quality"]
    + 0.16 * use_cases["infrastructure"]
    + 0.16 * use_cases["staff_ai_literacy"]
    + 0.22 * use_cases["governance_maturity"]
    + 0.16 * use_cases["workflow_fit"]
    + 0.10 * use_cases["trust"]
)

use_cases[["use_case", "ai_readiness"]].sort_values("ai_readiness", ascending=False)
        """),
        md("""
        ## Interpretation

        AI readiness depends on organizational capacity, not only technical access to AI tools.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "02_human_ai_decision_structures_and_workflow_allocation_lab.ipynb",
    "Human-AI Decision Structures and Workflow Allocation Lab",
    [
        md("""
        ## Purpose

        This lab assigns human-AI decision modes based on risk and readiness.
        """),
        code(use_case_setup),
        code("""
use_cases["ai_readiness"] = (
    0.20 * use_cases["data_quality"]
    + 0.16 * use_cases["infrastructure"]
    + 0.16 * use_cases["staff_ai_literacy"]
    + 0.22 * use_cases["governance_maturity"]
    + 0.16 * use_cases["workflow_fit"]
    + 0.10 * use_cases["trust"]
)

use_cases["decision_risk"] = (
    0.40 * use_cases["harm_potential"]
    + 0.30 * use_cases["rights_impact"]
    + 0.20 * use_cases["irreversibility"]
    + 0.10 * use_cases["opacity"]
)

def recommend_mode(row):
    if row["decision_risk"] >= 0.70:
        return "human_led_with_strong_review"
    if row["decision_risk"] >= 0.40:
        return "human_in_the_loop"
    if row["ai_readiness"] >= 0.70:
        return "monitored_automation"
    return "ai_decision_support_only"

use_cases["recommended_mode"] = use_cases.apply(recommend_mode, axis=1)

use_cases[["use_case", "decision_risk", "ai_readiness", "recommended_mode"]].sort_values("decision_risk", ascending=False)
        """),
        md("""
        ## Interpretation

        Decision allocation should be based on risk, reversibility, rights impact, interpretability, and organizational readiness.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "03_authority_power_legitimacy_and_institutional_ai_adoption_lab.ipynb",
    "Authority, Power, Legitimacy, and Institutional AI Adoption Lab",
    [
        md("""
        ## Purpose

        This lab scores institutional legitimacy and authority-risk concerns in AI adoption.
        """),
        code("""
import pandas as pd

institutional_factors = pd.DataFrame({
    "use_case": [
        "employee_performance_review",
        "public_benefits_eligibility",
        "procurement_anomaly_detection",
        "clinical_triage_support",
    ],
    "legal_alignment": [0.62, 0.58, 0.82, 0.74],
    "professional_norm_alignment": [0.48, 0.55, 0.78, 0.70],
    "stakeholder_trust": [0.42, 0.38, 0.76, 0.66],
    "contestability": [0.35, 0.44, 0.70, 0.60],
    "authority_shift_risk": [0.78, 0.86, 0.46, 0.62],
})

institutional_factors["legitimacy_score"] = (
    0.30 * institutional_factors["legal_alignment"]
    + 0.25 * institutional_factors["professional_norm_alignment"]
    + 0.25 * institutional_factors["stakeholder_trust"]
    + 0.20 * institutional_factors["contestability"]
)

institutional_factors["legitimacy_gap"] = (
    institutional_factors["authority_shift_risk"]
    - institutional_factors["legitimacy_score"]
)

institutional_factors.sort_values("legitimacy_gap", ascending=False)
        """),
        md("""
        ## Interpretation

        AI adoption becomes institutionally fragile when authority shifts faster than legitimacy, contestability, and stakeholder trust.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "04_public_sector_ai_governance_risk_and_accountability_lab.ipynb",
    "Public-Sector AI Governance, Risk, and Accountability Lab",
    [
        md("""
        ## Purpose

        This lab models public-sector AI accountability review for rights- and safety-affecting use cases.
        """),
        code("""
import pandas as pd

public_ai_reviews = pd.DataFrame({
    "use_case": [
        "public_benefits_eligibility",
        "infrastructure_emergency_response",
        "service_request_prioritization",
        "fraud_detection_triage",
    ],
    "rights_impact": [0.92, 0.70, 0.42, 0.78],
    "safety_impact": [0.50, 0.95, 0.30, 0.40],
    "transparency": [0.42, 0.58, 0.74, 0.46],
    "appeal_process": [0.55, 0.62, 0.80, 0.50],
    "human_oversight": [0.60, 0.78, 0.72, 0.54],
    "monitoring": [0.50, 0.80, 0.68, 0.56],
})

public_ai_reviews["public_risk"] = (
    0.45 * public_ai_reviews["rights_impact"]
    + 0.35 * public_ai_reviews["safety_impact"]
    + 0.20 * (1 - public_ai_reviews["transparency"])
)

public_ai_reviews["accountability_capacity"] = (
    0.30 * public_ai_reviews["transparency"]
    + 0.25 * public_ai_reviews["appeal_process"]
    + 0.25 * public_ai_reviews["human_oversight"]
    + 0.20 * public_ai_reviews["monitoring"]
)

public_ai_reviews["accountability_gap"] = (
    public_ai_reviews["public_risk"]
    - public_ai_reviews["accountability_capacity"]
)

public_ai_reviews.sort_values("accountability_gap", ascending=False)
        """),
        md("""
        ## Interpretation

        Public-sector AI use requires accountability capacity proportional to rights impact, safety impact, transparency needs, and contestability.
        """),
    ],
)
