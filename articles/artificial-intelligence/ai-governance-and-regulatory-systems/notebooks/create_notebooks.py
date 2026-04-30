#!/usr/bin/env python3
"""
Create advanced Jupyter notebooks for:
AI Governance and Regulatory Systems
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
    NOTEBOOK_DIR / "01_ai_system_inventory_and_risk_tiering_lab.ipynb",
    "AI System Inventory and Risk Tiering Lab",
    [
        md("""
        ## Purpose

        This lab introduces the AI governance inventory.

        Learning goals:

        - Build an AI use-case inventory.
        - Assign preliminary risk tiers.
        - Score inherent and residual risk.
        - Identify systems requiring governance review.
        """),
        code("""
        import pandas as pd

        inventory = pd.DataFrame([
            {
                "system_id": "ai-001",
                "system_name": "Customer Support Summarizer",
                "domain": "customer_service",
                "risk_tier": "limited",
                "likelihood": 2,
                "severity": 2,
                "mitigation_maturity": 0.70,
            },
            {
                "system_id": "ai-002",
                "system_name": "Hiring Screening Classifier",
                "domain": "employment",
                "risk_tier": "high",
                "likelihood": 3,
                "severity": 5,
                "mitigation_maturity": 0.45,
            },
            {
                "system_id": "ai-003",
                "system_name": "Medical Triage Assistant",
                "domain": "healthcare",
                "risk_tier": "high",
                "likelihood": 3,
                "severity": 5,
                "mitigation_maturity": 0.60,
            },
        ])

        inventory["inherent_risk"] = inventory["likelihood"] * inventory["severity"]
        inventory["residual_risk"] = inventory["inherent_risk"] * (1 - inventory["mitigation_maturity"])

        inventory.sort_values("residual_risk", ascending=False)
        """),
        md("""
        ## Interpretation

        A governance inventory is the foundation of AI oversight. Institutions cannot govern systems they have not identified.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "02_control_mapping_and_assurance_evidence_lab.ipynb",
    "Control Mapping and Assurance Evidence Lab",
    [
        md("""
        ## Purpose

        This lab maps governance controls to AI systems and evidence status.

        Learning goals:

        - Connect controls to risk tiers.
        - Track whether assurance evidence is missing, partial, or complete.
        - Identify review gaps.
        """),
        code("""
        import pandas as pd

        controls = pd.DataFrame([
            {"control": "data_provenance", "required_for": "high", "category": "documentation"},
            {"control": "bias_audit", "required_for": "high", "category": "bias_fairness"},
            {"control": "human_oversight", "required_for": "high", "category": "human_oversight"},
            {"control": "incident_response_plan", "required_for": "high", "category": "incident_response"},
            {"control": "user_notice", "required_for": "limited", "category": "transparency"},
            {"control": "logging", "required_for": "limited", "category": "monitoring"},
        ])

        evidence = pd.DataFrame([
            {"system_id": "ai-002", "control": "data_provenance", "evidence_status": "complete"},
            {"system_id": "ai-002", "control": "bias_audit", "evidence_status": "partial"},
            {"system_id": "ai-002", "control": "human_oversight", "evidence_status": "complete"},
            {"system_id": "ai-002", "control": "incident_response_plan", "evidence_status": "missing"},
        ])

        evidence_summary = (
            evidence
            .groupby("evidence_status", as_index=False)
            .agg(count=("control", "size"))
        )

        evidence, evidence_summary
        """),
        md("""
        ## Interpretation

        Governance requires evidence. A control that exists only as a policy statement is weaker than a control supported by documented artifacts, logs, tests, and review records.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "03_residual_risk_monitoring_and_incident_response_lab.ipynb",
    "Residual Risk, Monitoring, and Incident Response Lab",
    [
        md("""
        ## Purpose

        This lab connects residual risk to monitoring and incident response.

        Learning goals:

        - Simulate monitoring events.
        - Trigger review flags.
        - Summarize incident severity.
        """),
        code("""
        import numpy as np
        import pandas as pd

        rng = np.random.default_rng(42)

        monitoring = pd.DataFrame({
            "system_id": rng.choice(["ai-001", "ai-002", "ai-003"], size=200),
            "metric_name": rng.choice(["drift_score", "error_rate", "appeal_rate"], size=200),
            "metric_value": rng.uniform(0, 1, size=200),
        })

        thresholds = {
            "drift_score": 0.65,
            "error_rate": 0.25,
            "appeal_rate": 0.15,
        }

        monitoring["threshold"] = monitoring["metric_name"].map(thresholds)
        monitoring["review_required"] = monitoring["metric_value"] > monitoring["threshold"]

        alert_summary = (
            monitoring
            .groupby(["system_id", "metric_name"], as_index=False)
            .agg(
                events=("review_required", "size"),
                alerts=("review_required", "sum"),
                alert_rate=("review_required", "mean"),
            )
        )

        alert_summary.sort_values("alert_rate", ascending=False).head()
        """),
        md("""
        ## Interpretation

        Monitoring is governance only when alerts lead to review, escalation, remediation, or system withdrawal when necessary.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "04_regulatory_framework_mapping_and_governance_dashboard_lab.ipynb",
    "Regulatory Framework Mapping and Governance Dashboard Lab",
    [
        md("""
        ## Purpose

        This lab maps governance controls to framework language.

        The goal is not legal advice. It is a lightweight way to organize evidence across frameworks and internal governance processes.
        """),
        code("""
        import pandas as pd

        framework_map = pd.DataFrame([
            {
                "control": "risk_management_process",
                "nist_ai_rmf": "Govern / Map / Measure / Manage",
                "eu_ai_act_style": "risk management system",
                "oecd_style": "assess and address risks",
                "evidence": "risk register; review records",
            },
            {
                "control": "data_governance",
                "nist_ai_rmf": "Map / Measure",
                "eu_ai_act_style": "data governance and management",
                "oecd_style": "due diligence over inputs and impacts",
                "evidence": "dataset documentation; provenance records",
            },
            {
                "control": "human_oversight",
                "nist_ai_rmf": "Manage",
                "eu_ai_act_style": "human oversight",
                "oecd_style": "human-centered values and accountability",
                "evidence": "oversight procedure; training records",
            },
            {
                "control": "post_deployment_monitoring",
                "nist_ai_rmf": "Measure / Manage",
                "eu_ai_act_style": "post-market monitoring",
                "oecd_style": "track effectiveness and impacts",
                "evidence": "monitoring logs; incident reports",
            },
        ])

        framework_map
        """),
        md("""
        ## Interpretation

        Framework mapping helps organizations avoid fragmented compliance. The same control can often support several governance expectations when evidence is well structured.
        """),
    ],
)
