#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from textwrap import dedent

NOTEBOOK_DIR = Path(".")

def md(text: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": dedent(text).strip().splitlines(keepends=True)}

def code(text: str) -> dict:
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": dedent(text).strip().splitlines(keepends=True)}

def notebook(title: str, cells: list[dict]) -> dict:
    return {
        "cells": [{"cell_type": "markdown", "metadata": {}, "source": [f"# {title}\n"]}, *cells],
        "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}, "language_info": {"name": "python", "version": "3.x"}},
        "nbformat": 4,
        "nbformat_minor": 5,
    }

def write(path: Path, title: str, cells: list[dict]) -> None:
    path.write_text(json.dumps(notebook(title, cells), indent=2), encoding="utf-8")
    print(f"created {path}")

base_code = """
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
n = 1200

df = pd.DataFrame({
    "case_id": [f"HIAI-{i:04d}" for i in range(1, n + 1)],
    "model_confidence": rng.beta(5, 2, size=n),
    "explanation_quality": rng.beta(4, 3, size=n),
    "uncertainty_clarity": rng.beta(3.5, 3, size=n),
    "user_expertise": rng.choice(["novice", "intermediate", "expert"], size=n, p=[0.30, 0.45, 0.25]),
    "risk_level": rng.choice(["low", "medium", "high"], size=n, p=[0.45, 0.35, 0.20]),
    "time_pressure": rng.choice(["low", "medium", "high"], size=n, p=[0.35, 0.40, 0.25]),
})

df["model_correct"] = rng.binomial(1, np.clip(0.20 + 0.75 * df["model_confidence"], 0, 1), size=n)
df.head()
"""

write(
    NOTEBOOK_DIR / "01_human_ai_interaction_reliance_quality_lab.ipynb",
    "Human-AI Interaction Reliance Quality Lab",
    [
        md("""
        ## Purpose

        This lab introduces reliance quality as a human-AI interaction metric.
        """),
        code(base_code),
        code("""
acceptance_probability = np.clip(
    0.10 + 0.55 * df["model_confidence"] + 0.15 * df["explanation_quality"],
    0.02,
    0.98,
)

df["user_accepted_ai"] = rng.binomial(1, acceptance_probability, size=n)
df["overreliance"] = ((df["user_accepted_ai"] == 1) & (df["model_correct"] == 0)).astype(int)
df["underreliance"] = ((df["user_accepted_ai"] == 0) & (df["model_correct"] == 1)).astype(int)
df["reliance_gap"] = abs(df["user_accepted_ai"] - df["model_correct"])

df.groupby(["user_expertise", "risk_level"]).agg(
    cases=("case_id", "count"),
    accuracy=("model_correct", "mean"),
    acceptance_rate=("user_accepted_ai", "mean"),
    overreliance_rate=("overreliance", "mean"),
    underreliance_rate=("underreliance", "mean"),
    reliance_gap=("reliance_gap", "mean"),
).reset_index()
        """),
    ],
)

write(
    NOTEBOOK_DIR / "02_interface_clarity_uncertainty_and_explanation_lab.ipynb",
    "Interface Clarity, Uncertainty, and Explanation Lab",
    [
        md("""
        ## Purpose

        This lab explores how explanation quality and uncertainty clarity may affect escalation.
        """),
        code(base_code),
        code("""
df["should_escalate"] = (
    (df["risk_level"] == "high")
    | (df["uncertainty_clarity"] < 0.35)
    | (df["explanation_quality"] < 0.35)
).astype(int)

df.groupby("risk_level").agg(
    cases=("case_id", "count"),
    mean_explanation_quality=("explanation_quality", "mean"),
    mean_uncertainty_clarity=("uncertainty_clarity", "mean"),
    escalation_need_rate=("should_escalate", "mean"),
).reset_index()
        """),
    ],
)

write(
    NOTEBOOK_DIR / "03_automation_bias_algorithm_aversion_and_workflow_lab.ipynb",
    "Automation Bias, Algorithm Aversion, and Workflow Lab",
    [
        md("""
        ## Purpose

        This lab compares overreliance and underreliance under different workflow pressures.
        """),
        code(base_code),
        code("""
pressure_boost = df["time_pressure"].map({"low": -0.05, "medium": 0.03, "high": 0.14})
risk_adjust = df["risk_level"].map({"low": 0.08, "medium": 0.00, "high": -0.10})

acceptance_probability = np.clip(
    0.12 + 0.50 * df["model_confidence"] + pressure_boost + risk_adjust,
    0.02,
    0.98,
)

df["accepted"] = rng.binomial(1, acceptance_probability, size=n)
df["overreliance"] = ((df["accepted"] == 1) & (df["model_correct"] == 0)).astype(int)
df["underreliance"] = ((df["accepted"] == 0) & (df["model_correct"] == 1)).astype(int)

df.groupby(["time_pressure", "risk_level"]).agg(
    cases=("case_id", "count"),
    acceptance_rate=("accepted", "mean"),
    overreliance_rate=("overreliance", "mean"),
    underreliance_rate=("underreliance", "mean"),
).reset_index()
        """),
    ],
)

write(
    NOTEBOOK_DIR / "04_governance_contestability_and_design_review_lab.ipynb",
    "Governance, Contestability, and Design Review Lab",
    [
        md("""
        ## Purpose

        This lab frames interface design as governance evidence.
        """),
        code("""
import pandas as pd

design_review = pd.DataFrame([
    {"area": "mental_model", "question": "Does the interface communicate capability and limitation?", "status": "partial", "owner": "UX Research"},
    {"area": "uncertainty", "question": "Is uncertainty shown in a user-understandable way?", "status": "partial", "owner": "Design + Data Science"},
    {"area": "override", "question": "Can users override recommendations?", "status": "complete", "owner": "Product"},
    {"area": "escalation", "question": "Can high-risk cases be escalated?", "status": "complete", "owner": "Operations"},
    {"area": "contestability", "question": "Can affected people challenge outcomes?", "status": "missing", "owner": "Policy"},
    {"area": "monitoring", "question": "Are overreliance and underreliance monitored?", "status": "partial", "owner": "MLOps"},
])

design_review.groupby("status").size().reset_index(name="count")
        """),
    ],
)
