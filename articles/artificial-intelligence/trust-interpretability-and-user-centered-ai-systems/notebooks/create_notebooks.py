#!/usr/bin/env python3
"""
Create advanced Jupyter notebooks for:
Trust, Interpretability, and User-Centered AI Systems
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
    NOTEBOOK_DIR / "01_trust_calibration_and_reliance_gap_lab.ipynb",
    "Trust Calibration and Reliance Gap Lab",
    [
        md("""
        ## Purpose

        This lab introduces trust calibration.

        Learning goals:

        - Simulate model confidence and correctness.
        - Simulate user reliance.
        - Compute overreliance, underreliance, and reliance gaps.
        - Interpret trust as calibrated reliance.
        """),
        code("""
        import numpy as np
        import pandas as pd

        rng = np.random.default_rng(42)

        n = 1500

        data = pd.DataFrame({
            "case_id": [f"C-{i:04d}" for i in range(1, n + 1)],
            "model_confidence": rng.beta(5, 2, size=n),
            "user_expertise": rng.choice(["novice", "intermediate", "expert"], size=n, p=[0.30, 0.45, 0.25]),
            "risk_level": rng.choice(["low", "medium", "high"], size=n, p=[0.45, 0.35, 0.20]),
        })

        data["model_correct"] = rng.binomial(
            1,
            p=np.clip(0.20 + 0.75 * data["model_confidence"], 0, 1),
            size=n,
        )

        data["user_relied_on_ai"] = rng.binomial(
            1,
            p=np.clip(0.15 + 0.65 * data["model_confidence"], 0.02, 0.98),
            size=n,
        )

        data["overreliance"] = ((data["user_relied_on_ai"] == 1) & (data["model_correct"] == 0)).astype(int)
        data["underreliance"] = ((data["user_relied_on_ai"] == 0) & (data["model_correct"] == 1)).astype(int)
        data["reliance_gap"] = abs(data["user_relied_on_ai"] - data["model_correct"])

        summary = (
            data
            .groupby(["user_expertise", "risk_level"])
            .agg(
                cases=("case_id", "count"),
                accuracy=("model_correct", "mean"),
                reliance_rate=("user_relied_on_ai", "mean"),
                overreliance_rate=("overreliance", "mean"),
                underreliance_rate=("underreliance", "mean"),
                mean_reliance_gap=("reliance_gap", "mean"),
            )
            .reset_index()
        )

        summary
        """),
        md("""
        ## Interpretation

        Trust is best treated as calibrated reliance rather than general confidence in the system.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "02_explanation_quality_and_user_decision_lab.ipynb",
    "Explanation Quality and User Decision Lab",
    [
        md("""
        ## Purpose

        This lab models explanation quality as a composite of fidelity, usefulness, actionability, and stability.

        Learning goals:

        - Simulate explanation-quality dimensions.
        - Compute an explanation-quality score.
        - Explore how explanation quality affects user decisions.
        """),
        code("""
        import numpy as np
        import pandas as pd

        rng = np.random.default_rng(42)

        n = 1000

        explanations = pd.DataFrame({
            "case_id": [f"C-{i:04d}" for i in range(1, n + 1)],
            "fidelity": rng.beta(5, 2, size=n),
            "usefulness": rng.beta(4, 3, size=n),
            "actionability": rng.beta(3.5, 3, size=n),
            "stability": rng.beta(4, 2.5, size=n),
            "risk_level": rng.choice(["low", "medium", "high"], size=n, p=[0.45, 0.35, 0.20]),
        })

        weights = {
            "fidelity": 0.35,
            "usefulness": 0.25,
            "actionability": 0.25,
            "stability": 0.15,
        }

        explanations["explanation_quality"] = (
            weights["fidelity"] * explanations["fidelity"]
            + weights["usefulness"] * explanations["usefulness"]
            + weights["actionability"] * explanations["actionability"]
            + weights["stability"] * explanations["stability"]
        )

        explanations["user_requested_review"] = rng.binomial(
            1,
            p=np.clip(0.45 - 0.35 * explanations["explanation_quality"], 0.05, 0.80),
            size=n,
        )

        explanations.groupby("risk_level").agg(
            mean_explanation_quality=("explanation_quality", "mean"),
            review_request_rate=("user_requested_review", "mean"),
        ).reset_index()
        """),
        md("""
        ## Interpretation

        Better explanations should reduce confusion, but high-risk systems still need review pathways even when explanations are clear.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "03_overreliance_underreliance_and_human_ai_workflow_lab.ipynb",
    "Overreliance, Underreliance, and Human-AI Workflow Lab",
    [
        md("""
        ## Purpose

        This lab treats AI use as a workflow, not just a prediction.

        Learning goals:

        - Simulate accept, override, and escalate decisions.
        - Identify where workflow design may encourage overreliance.
        - Summarize decision-source behavior.
        """),
        code("""
        import numpy as np
        import pandas as pd

        rng = np.random.default_rng(42)

        n = 1200

        workflow = pd.DataFrame({
            "case_id": [f"W-{i:04d}" for i in range(1, n + 1)],
            "model_confidence": rng.beta(5, 2, size=n),
            "explanation_quality": rng.beta(4, 3, size=n),
            "time_pressure": rng.choice(["low", "medium", "high"], size=n, p=[0.35, 0.40, 0.25]),
            "risk_level": rng.choice(["low", "medium", "high"], size=n, p=[0.40, 0.40, 0.20]),
        })

        accept_probability = (
            0.10
            + 0.55 * workflow["model_confidence"]
            + 0.15 * workflow["explanation_quality"]
            + workflow["time_pressure"].map({"low": -0.05, "medium": 0.02, "high": 0.12})
            + workflow["risk_level"].map({"low": 0.08, "medium": 0.00, "high": -0.10})
        )

        workflow["accepted_ai"] = rng.binomial(1, np.clip(accept_probability, 0.02, 0.98), size=n)

        workflow["escalated"] = rng.binomial(
            1,
            np.clip(
                0.05
                + 0.25 * (workflow["risk_level"] == "high").astype(int)
                + 0.20 * (workflow["explanation_quality"] < 0.45).astype(int),
                0.01,
                0.90,
            ),
            size=n,
        )

        workflow["workflow_outcome"] = np.select(
            [
                workflow["escalated"] == 1,
                workflow["accepted_ai"] == 1,
            ],
            [
                "escalated",
                "accepted_ai",
            ],
            default="overrode_or_ignored",
        )

        workflow.groupby(["time_pressure", "risk_level", "workflow_outcome"]).size().reset_index(name="cases")
        """),
        md("""
        ## Interpretation

        Workflow pressure affects reliance. A system can produce the same output but lead to different human decisions under different operational conditions.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "04_user_centered_ai_governance_and_contestability_lab.ipynb",
    "User-Centered AI Governance and Contestability Lab",
    [
        md("""
        ## Purpose

        This lab frames user-centered AI as governance infrastructure.

        Learning goals:

        - Build a design-review checklist.
        - Track contestability and accountability evidence.
        - Connect interaction design to governance review.
        """),
        code("""
        import pandas as pd

        review_checklist = pd.DataFrame([
            {
                "review_area": "intended_users",
                "question": "Have direct users and affected stakeholders been identified?",
                "evidence_status": "complete",
                "owner": "Product Lead",
            },
            {
                "review_area": "validated_scope",
                "question": "Are system capabilities and out-of-scope uses documented?",
                "evidence_status": "partial",
                "owner": "Model Risk Team",
            },
            {
                "review_area": "explanations",
                "question": "Are explanations appropriate for each user role?",
                "evidence_status": "partial",
                "owner": "UX Research",
            },
            {
                "review_area": "uncertainty",
                "question": "Is uncertainty communicated in a way users understand?",
                "evidence_status": "missing",
                "owner": "Design + Data Science",
            },
            {
                "review_area": "contestability",
                "question": "Can affected people challenge or correct AI-influenced outcomes?",
                "evidence_status": "missing",
                "owner": "Policy / Legal",
            },
            {
                "review_area": "monitoring",
                "question": "Are overreliance and underreliance monitored after deployment?",
                "evidence_status": "partial",
                "owner": "MLOps",
            },
        ])

        review_summary = (
            review_checklist
            .groupby("evidence_status", as_index=False)
            .agg(count=("review_area", "size"))
        )

        review_checklist, review_summary
        """),
        md("""
        ## Interpretation

        User-centered AI becomes accountable when design decisions, explanations, uncertainty displays, contestability, and monitoring are documented and reviewed.
        """),
    ],
)
