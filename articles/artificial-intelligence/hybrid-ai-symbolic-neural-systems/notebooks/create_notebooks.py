#!/usr/bin/env python3
"""
Create advanced Jupyter notebooks for:
Hybrid AI: Symbolic + Neural Systems
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
    NOTEBOOK_DIR / "01_symbolic_facts_rules_and_knowledge_graph_lab.ipynb",
    "Symbolic Facts, Rules, and Knowledge Graph Lab",
    [
        md("""
        ## Purpose

        This lab introduces the symbolic side of hybrid AI.

        Learning goals:

        - Represent facts as triples.
        - Represent rules as structured conditions.
        - Build a lightweight knowledge graph table.
        - Interpret symbolic knowledge as an auditable AI layer.
        """),
        code("""
        import pandas as pd

        triples = pd.DataFrame([
            {"subject": "Asset A-001", "predicate": "isA", "object": "CriticalAsset"},
            {"subject": "Asset A-001", "predicate": "hasCondition", "object": "LowCondition"},
            {"subject": "CriticalAsset", "predicate": "requires", "object": "HumanReview"},
            {"subject": "LowCondition", "predicate": "increases", "object": "FailureRisk"},
            {"subject": "Hybrid AI", "predicate": "combines", "object": "NeuralLearning"},
            {"subject": "Hybrid AI", "predicate": "combines", "object": "SymbolicReasoning"},
        ])

        rules = pd.DataFrame([
            {
                "rule_name": "critical_low_condition_review",
                "premise": "CriticalAsset AND LowCondition",
                "conclusion": "HumanReviewRequired",
                "severity": "high",
            },
            {
                "rule_name": "sensitive_workflow_review",
                "premise": "SensitiveWorkflow AND RiskScore >= 0.45",
                "conclusion": "HumanReviewRequired",
                "severity": "medium",
            },
        ])

        triples, rules
        """),
        md("""
        ## Interpretation

        Symbolic layers are useful because they make domain knowledge explicit, reviewable, and versionable.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "02_neural_scores_and_hybrid_decision_pipeline_lab.ipynb",
    "Neural Scores and Hybrid Decision Pipeline Lab",
    [
        md("""
        ## Purpose

        This lab combines neural scores with symbolic rules.

        Learning goals:

        - Simulate neural risk scores.
        - Apply symbolic constraints.
        - Produce a hybrid decision.
        - Track the decision source.
        """),
        code("""
        import numpy as np
        import pandas as pd

        rng = np.random.default_rng(42)

        n = 500

        records = pd.DataFrame({
            "entity_id": [f"E-{i:04d}" for i in range(1, n + 1)],
            "neural_risk_score": rng.beta(2.2, 4.0, size=n),
            "condition_score": rng.uniform(0.10, 0.98, size=n),
            "criticality": rng.choice(["low", "medium", "high"], size=n, p=[0.45, 0.35, 0.20]),
            "sensitive_workflow": rng.choice([0, 1], size=n, p=[0.80, 0.20]),
        })

        records["neural_recommendation"] = (records["neural_risk_score"] >= 0.55).astype(int)

        records["symbolic_review_required"] = (
            ((records["criticality"] == "high") & (records["condition_score"] <= 0.35))
            | ((records["sensitive_workflow"] == 1) & (records["neural_risk_score"] >= 0.45))
            | ((records["criticality"] == "medium") & (records["condition_score"] <= 0.25))
        ).astype(int)

        records["hybrid_decision"] = (
            (records["neural_recommendation"] == 1)
            | (records["symbolic_review_required"] == 1)
        ).astype(int)

        records["decision_source"] = np.select(
            [
                (records["neural_recommendation"] == 1) & (records["symbolic_review_required"] == 1),
                (records["neural_recommendation"] == 1) & (records["symbolic_review_required"] == 0),
                (records["neural_recommendation"] == 0) & (records["symbolic_review_required"] == 1),
            ],
            [
                "neural_and_symbolic",
                "neural_only",
                "symbolic_only",
            ],
            default="no_review",
        )

        records.head()
        """),
        code("""
        summary = (
            records
            .groupby("decision_source")
            .agg(
                n=("entity_id", "count"),
                mean_score=("neural_risk_score", "mean"),
                mean_condition=("condition_score", "mean"),
                review_rate=("hybrid_decision", "mean"),
            )
            .reset_index()
        )

        summary
        """),
        md("""
        ## Interpretation

        Hybrid diagnostics should show how often decisions come from neural scores, symbolic rules, or both.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "03_constraint_violations_audit_traces_and_human_review_lab.ipynb",
    "Constraint Violations, Audit Traces, and Human Review Lab",
    [
        md("""
        ## Purpose

        This lab shows how hybrid systems can generate audit traces.

        Learning goals:

        - Identify rule triggers.
        - Build a trace table.
        - Link neural outputs to symbolic review.
        - Identify cases requiring human oversight.
        """),
        code("""
        import numpy as np
        import pandas as pd

        rng = np.random.default_rng(42)

        records = pd.DataFrame({
            "entity_id": [f"E-{i:04d}" for i in range(1, 101)],
            "neural_output": rng.uniform(0, 1, size=100),
            "criticality": rng.choice(["low", "medium", "high"], size=100),
            "condition_score": rng.uniform(0.10, 0.98, size=100),
        })

        trace_rows = []

        for _, row in records.iterrows():
            if row["neural_output"] >= 0.55:
                trace_rows.append({
                    "entity_id": row["entity_id"],
                    "step_type": "neural_prediction",
                    "step_summary": "Neural score exceeded threshold",
                    "review_required": True,
                })

            if row["criticality"] == "high" and row["condition_score"] <= 0.35:
                trace_rows.append({
                    "entity_id": row["entity_id"],
                    "step_type": "symbolic_rule_check",
                    "step_summary": "Critical asset with low condition triggered symbolic rule",
                    "review_required": True,
                })

        trace = pd.DataFrame(trace_rows)

        trace.head(), trace["step_type"].value_counts()
        """),
        md("""
        ## Interpretation

        Audit traces are central to governable hybrid AI because they record which component contributed to a decision.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "04_retrieval_knowledge_graphs_and_governance_lab.ipynb",
    "Retrieval, Knowledge Graphs, and Governance Lab",
    [
        md("""
        ## Purpose

        This lab frames retrieval and knowledge graphs as governance layers.

        Learning goals:

        - Track retrieved facts.
        - Connect facts to provenance.
        - Map retrieved knowledge to output review.
        - Build a governance checklist.
        """),
        code("""
        import pandas as pd

        retrieved_facts = pd.DataFrame([
            {
                "fact_id": "F-001",
                "subject": "Hybrid AI",
                "predicate": "combines",
                "object": "neural learning and symbolic reasoning",
                "provenance": "knowledge_base:v1",
            },
            {
                "fact_id": "F-002",
                "subject": "Symbolic layer",
                "predicate": "supports",
                "object": "constraint checking",
                "provenance": "governance_rules:v3",
            },
            {
                "fact_id": "F-003",
                "subject": "Neural layer",
                "predicate": "supports",
                "object": "pattern recognition",
                "provenance": "model_card:v2",
            },
        ])

        governance_checklist = pd.DataFrame([
            {"question": "Which facts were retrieved?", "evidence": "retrieval log"},
            {"question": "Which knowledge base version was used?", "evidence": "knowledge base metadata"},
            {"question": "Which rules were applied?", "evidence": "rule trace"},
            {"question": "Were any constraints violated?", "evidence": "constraint violation table"},
            {"question": "Was human review triggered?", "evidence": "decision trace"},
        ])

        retrieved_facts, governance_checklist
        """),
        md("""
        ## Interpretation

        Retrieval makes hybrid AI stronger only when facts, sources, rule versions, and decisions are traceable.
        """),
    ],
)
