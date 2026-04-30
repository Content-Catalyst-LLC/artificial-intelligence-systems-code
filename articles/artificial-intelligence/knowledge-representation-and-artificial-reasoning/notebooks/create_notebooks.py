#!/usr/bin/env python3
"""
Create advanced Jupyter notebooks for:
Knowledge Representation and Artificial Reasoning
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
    NOTEBOOK_DIR / "01_symbolic_triples_and_knowledge_graph_lab.ipynb",
    "Symbolic Triples and Knowledge Graph Lab",
    [
        md("""
        ## Purpose

        This lab introduces symbolic triples and knowledge graph structure.

        Learning goals:

        - Represent facts as subject-predicate-object triples.
        - Build a lightweight graph table.
        - Query relations by subject, predicate, or object.
        - Interpret knowledge graphs as semantic infrastructure.
        """),
        code("""
        import pandas as pd

        triples = pd.DataFrame([
            {"subject": "Socrates", "predicate": "isA", "object": "Human"},
            {"subject": "Human", "predicate": "subClassOf", "object": "Mortal"},
            {"subject": "Mortal", "predicate": "subClassOf", "object": "Entity"},
            {"subject": "Knowledge Representation", "predicate": "supports", "object": "Auditability"},
            {"subject": "Ontology", "predicate": "supports", "object": "Semantic Interoperability"},
            {"subject": "Knowledge Graph", "predicate": "represents", "object": "Entity Relations"},
        ])

        triples
        """),
        code("""
        def query_triples(frame, subject=None, predicate=None, object_=None):
            result = frame.copy()

            if subject is not None:
                result = result[result["subject"] == subject]

            if predicate is not None:
                result = result[result["predicate"] == predicate]

            if object_ is not None:
                result = result[result["object"] == object_]

            return result

        query_triples(triples, predicate="supports")
        """),
        md("""
        ## Interpretation

        Triples are simple, but they provide a durable foundation for semantic structure, entity linking, and explainable retrieval.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "02_rule_based_inference_and_forward_chaining_lab.ipynb",
    "Rule-Based Inference and Forward Chaining Lab",
    [
        md("""
        ## Purpose

        This lab demonstrates forward chaining.

        The system starts with explicit facts and applies rules until no new conclusions can be derived.
        """),
        code("""
        from dataclasses import dataclass
        from typing import Callable
        import pandas as pd

        Fact = tuple[str, str, str]

        @dataclass(frozen=True)
        class Rule:
            name: str
            apply: Callable[[set[Fact]], set[Fact]]

        def subclass_inheritance(facts: set[Fact]) -> set[Fact]:
            inferred = set()

            memberships = [
                (entity, parent_class)
                for entity, predicate, parent_class in facts
                if predicate == "isA"
            ]

            subclass_edges = [
                (child_class, parent_class)
                for child_class, predicate, parent_class in facts
                if predicate == "subClassOf"
            ]

            for entity, entity_class in memberships:
                for child_class, parent_class in subclass_edges:
                    if entity_class == child_class:
                        inferred.add((entity, "isA", parent_class))

            return inferred

        facts = {
            ("Socrates", "isA", "Human"),
            ("Human", "subClassOf", "Mortal"),
            ("Mortal", "subClassOf", "Entity"),
        }

        rule = Rule("subclass_inheritance", subclass_inheritance)

        inferred = rule.apply(facts)

        pd.DataFrame(
            [{"subject": s, "predicate": p, "object": o} for s, p, o in sorted(inferred)]
        )
        """),
        md("""
        ## Interpretation

        Forward chaining is auditable because each conclusion can be connected to facts and rules.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "03_uncertainty_abduction_and_belief_revision_lab.ipynb",
    "Uncertainty, Abduction, and Belief Revision Lab",
    [
        md("""
        ## Purpose

        This lab introduces probabilistic belief updating and abductive explanation.

        Learning goals:

        - Represent hypotheses and evidence.
        - Update beliefs with Bayes' rule.
        - Select plausible explanations under uncertainty.
        """),
        code("""
        import pandas as pd

        hypotheses = pd.DataFrame([
            {"hypothesis": "sensor_failure", "prior": 0.20, "likelihood_evidence": 0.70},
            {"hypothesis": "infrastructure_stress", "prior": 0.35, "likelihood_evidence": 0.55},
            {"hypothesis": "measurement_noise", "prior": 0.45, "likelihood_evidence": 0.25},
        ])

        hypotheses["unnormalized_posterior"] = (
            hypotheses["prior"] * hypotheses["likelihood_evidence"]
        )

        evidence_probability = hypotheses["unnormalized_posterior"].sum()

        hypotheses["posterior"] = (
            hypotheses["unnormalized_posterior"] / evidence_probability
        )

        hypotheses.sort_values("posterior", ascending=False)
        """),
        md("""
        ## Interpretation

        Abduction asks which hypothesis best explains the evidence. Bayesian updating provides one disciplined way to revise belief when evidence changes.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "04_hybrid_ai_governance_and_auditability_lab.ipynb",
    "Hybrid AI, Governance, and Auditability Lab",
    [
        md("""
        ## Purpose

        This lab frames hybrid AI as a governance architecture.

        Modern AI systems may combine neural models, retrieval systems, symbolic constraints, knowledge graphs, and human review.
        """),
        code("""
        import pandas as pd

        hybrid_layers = pd.DataFrame([
            {
                "layer": "neural_model",
                "role": "pattern recognition and generation",
                "governance_question": "What data and objectives shaped the learned representations?"
            },
            {
                "layer": "knowledge_graph",
                "role": "structured entity-relation memory",
                "governance_question": "What entities, relations, and provenance sources are represented?"
            },
            {
                "layer": "rules_constraints",
                "role": "semantic consistency and policy enforcement",
                "governance_question": "Which rules are authoritative and who reviews exceptions?"
            },
            {
                "layer": "retrieval",
                "role": "evidence grounding",
                "governance_question": "Are retrieved sources relevant, current, and correctly represented?"
            },
            {
                "layer": "human_review",
                "role": "oversight and contestability",
                "governance_question": "Who can inspect, challenge, revise, or override conclusions?"
            },
        ])

        hybrid_layers
        """),
        md("""
        ## Interpretation

        Hybrid AI should not be understood only as a technical architecture. It is also a governance architecture because it makes assumptions, evidence, constraints, and inference paths more visible.
        """),
    ],
)
