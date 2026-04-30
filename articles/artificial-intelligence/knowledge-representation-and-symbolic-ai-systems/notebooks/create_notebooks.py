#!/usr/bin/env python3
"""
Create advanced Jupyter notebooks for:
Knowledge Representation and Symbolic AI Systems
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
    NOTEBOOK_DIR / "01_symbolic_facts_semantic_triples_and_inference_lab.ipynb",
    "Symbolic Facts, Semantic Triples, and Inference Lab",
    [
        md("""
        ## Purpose

        This lab introduces facts, triples, rules, and inference traces.

        Learning goals:

        - Represent facts as subject-predicate-object triples.
        - Apply a symbolic rule.
        - Produce an inferred conclusion.
        - Store an inference trace for auditability.
        """),
        code("""
        import pandas as pd

        facts = pd.DataFrame([
            {"subject": "ModelA", "predicate": "type", "object": "HighImpactSystem"},
            {"subject": "DatasetB", "predicate": "type", "object": "SensitiveDataset"},
            {"subject": "ModelA", "predicate": "trainedOn", "object": "DatasetB"},
            {"subject": "ModelC", "predicate": "type", "object": "LowImpactSystem"},
            {"subject": "DatasetD", "predicate": "type", "object": "PublicDataset"},
            {"subject": "ModelC", "predicate": "trainedOn", "object": "DatasetD"},
        ])

        def has_fact(subject, predicate, object_value):
            return len(
                facts[
                    (facts["subject"] == subject)
                    & (facts["predicate"] == predicate)
                    & (facts["object"] == object_value)
                ]
            ) > 0

        inferences = []

        for _, row in facts[facts["predicate"] == "trainedOn"].iterrows():
            model = row["subject"]
            dataset = row["object"]

            if has_fact(model, "type", "HighImpactSystem") and has_fact(dataset, "type", "SensitiveDataset"):
                inferences.append({
                    "subject": model,
                    "predicate": "requires",
                    "object": "FairnessReview",
                    "rule": "high_impact_sensitive_data_requires_fairness_review",
                    "support": f"{model} trainedOn {dataset}",
                })

        pd.DataFrame(inferences)
        """),
        md("""
        ## Interpretation

        Symbolic inference is useful because it can produce both a conclusion and an explanation trace.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "02_ontologies_taxonomies_and_frame_systems_lab.ipynb",
    "Ontologies, Taxonomies, and Frame Systems Lab",
    [
        md("""
        ## Purpose

        This lab demonstrates simple taxonomy and frame structures.

        Learning goals:

        - Represent class hierarchies.
        - Represent frames as slot-value structures.
        - Use frames to organize domain knowledge.
        """),
        code("""
        import pandas as pd

        class_hierarchy = pd.DataFrame([
            {"class": "AI_System", "parent": None},
            {"class": "HighImpactSystem", "parent": "AI_System"},
            {"class": "LowImpactSystem", "parent": "AI_System"},
            {"class": "Dataset", "parent": None},
            {"class": "SensitiveDataset", "parent": "Dataset"},
            {"class": "PublicDataset", "parent": "Dataset"},
            {"class": "GovernanceReview", "parent": None},
            {"class": "FairnessReview", "parent": "GovernanceReview"},
        ])

        frames = pd.DataFrame([
            {"frame": "AI_System", "slot": "owner", "required": True, "default": None},
            {"frame": "AI_System", "slot": "model_version", "required": True, "default": None},
            {"frame": "AI_System", "slot": "risk_tier", "required": True, "default": "unknown"},
            {"frame": "GovernanceReview", "slot": "reviewer", "required": True, "default": None},
            {"frame": "GovernanceReview", "slot": "status", "required": True, "default": "draft"},
        ])

        class_hierarchy, frames
        """),
        md("""
        ## Interpretation

        Ontologies and frames define the structure of the domain before inference begins.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "03_rules_defaults_exceptions_and_traceability_lab.ipynb",
    "Rules, Defaults, Exceptions, and Traceability Lab",
    [
        md("""
        ## Purpose

        This lab demonstrates default reasoning and exception handling.

        Learning goals:

        - Apply a default rule.
        - Override the default with an exception.
        - Record which rule governed the conclusion.
        """),
        code("""
        import pandas as pd

        entities = pd.DataFrame([
            {"entity": "BirdA", "type": "Bird"},
            {"entity": "PenguinB", "type": "Penguin"},
            {"entity": "BirdC", "type": "Bird"},
        ])

        traces = []

        for _, row in entities.iterrows():
            entity = row["entity"]
            entity_type = row["type"]

            if entity_type == "Penguin":
                traces.append({
                    "entity": entity,
                    "conclusion": "DoesNotFly",
                    "rule_applied": "penguin_exception",
                    "reason": "Penguins are exceptions to the bird default."
                })
            elif entity_type == "Bird":
                traces.append({
                    "entity": entity,
                    "conclusion": "Flies",
                    "rule_applied": "bird_default",
                    "reason": "Birds fly by default unless an exception is known."
                })

        pd.DataFrame(traces)
        """),
        md("""
        ## Interpretation

        Real symbolic systems need defaults and exceptions because practical domains rarely follow universal rules without qualification.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "04_knowledge_graphs_governance_and_ai_lifecycle_metadata_lab.ipynb",
    "Knowledge Graphs, Governance, and AI Lifecycle Metadata Lab",
    [
        md("""
        ## Purpose

        This lab frames knowledge representation as AI governance infrastructure.

        Learning goals:

        - Represent AI lifecycle metadata as triples.
        - Connect models, datasets, evaluations, risks, and controls.
        - Query governance relationships.
        """),
        code("""
        import pandas as pd

        lifecycle_triples = pd.DataFrame([
            {"subject": "ModelA", "predicate": "trainedOn", "object": "DatasetB"},
            {"subject": "ModelA", "predicate": "evaluatedBy", "object": "EvaluationRun17"},
            {"subject": "EvaluationRun17", "predicate": "measured", "object": "CalibrationError"},
            {"subject": "ModelA", "predicate": "hasRisk", "object": "Risk42"},
            {"subject": "Risk42", "predicate": "mitigatedBy", "object": "Control9"},
            {"subject": "Control9", "predicate": "ownedBy", "object": "GovernanceTeam"},
            {"subject": "ModelA", "predicate": "approvedBy", "object": "ReviewBoard3"},
        ])

        model_a_relations = lifecycle_triples[lifecycle_triples["subject"] == "ModelA"]

        risks = lifecycle_triples[
            (lifecycle_triples["subject"] == "ModelA")
            & (lifecycle_triples["predicate"] == "hasRisk")
        ]["object"].tolist()

        controls = lifecycle_triples[
            lifecycle_triples["subject"].isin(risks)
            & (lifecycle_triples["predicate"] == "mitigatedBy")
        ]

        model_a_relations, controls
        """),
        md("""
        ## Interpretation

        Governance metadata becomes more useful when represented as explicit relationships that can be queried and audited.
        """),
    ],
)
