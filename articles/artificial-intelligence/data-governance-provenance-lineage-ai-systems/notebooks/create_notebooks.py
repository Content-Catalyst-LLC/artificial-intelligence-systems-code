#!/usr/bin/env python3
"""
Create advanced Jupyter notebooks for:
Data Governance, Provenance, and Lineage in AI Systems
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


provenance_setup = """
import pandas as pd

entities = pd.DataFrame([
    {"entity_id": "D_source_A", "entity_type": "source_dataset", "version": "2026-01"},
    {"entity_id": "D_source_B", "entity_type": "source_dataset", "version": "2026-01"},
    {"entity_id": "D_joined_1", "entity_type": "derived_dataset", "version": "v1"},
    {"entity_id": "F_features_2", "entity_type": "feature_table", "version": "v2"},
    {"entity_id": "M_model_3", "entity_type": "model", "version": "v3"},
    {"entity_id": "R_eval_3", "entity_type": "evaluation_report", "version": "v3"},
])

activities = pd.DataFrame([
    {"activity_id": "A_join", "activity_type": "join"},
    {"activity_id": "A_feature", "activity_type": "feature_engineering"},
    {"activity_id": "A_train", "activity_type": "model_training"},
    {"activity_id": "A_eval", "activity_type": "evaluation"},
])

agents = pd.DataFrame([
    {"agent_id": "G_data_team", "agent_type": "team"},
    {"agent_id": "G_ml_team", "agent_type": "team"},
    {"agent_id": "G_governance", "agent_type": "team"},
])

relations = pd.DataFrame([
    {"source": "D_source_A", "relation": "used_by", "target": "A_join"},
    {"source": "D_source_B", "relation": "used_by", "target": "A_join"},
    {"source": "A_join", "relation": "generated", "target": "D_joined_1"},
    {"source": "D_joined_1", "relation": "used_by", "target": "A_feature"},
    {"source": "A_feature", "relation": "generated", "target": "F_features_2"},
    {"source": "F_features_2", "relation": "used_by", "target": "A_train"},
    {"source": "A_train", "relation": "generated", "target": "M_model_3"},
    {"source": "M_model_3", "relation": "used_by", "target": "A_eval"},
    {"source": "A_eval", "relation": "generated", "target": "R_eval_3"},
])

entities, activities, agents, relations.head()
"""

write(
    NOTEBOOK_DIR / "01_provenance_entities_activities_agents_and_relations_lab.ipynb",
    "Provenance Entities, Activities, Agents, and Relations Lab",
    [
        md("""
        ## Purpose

        This lab introduces W3C PROV-inspired entities, activities, agents, and provenance relations.
        """),
        code(provenance_setup),
        code("""
summary = pd.DataFrame([
    {"table": "entities", "records": len(entities)},
    {"table": "activities", "records": len(activities)},
    {"table": "agents", "records": len(agents)},
    {"table": "relations", "records": len(relations)},
])

summary
        """),
        md("""
        ## Interpretation

        Provenance metadata makes AI artifacts traceable across data, transformations, models, evaluation, and responsible agents.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "02_lineage_graphs_dependency_tracing_and_impact_analysis_lab.ipynb",
    "Lineage Graphs, Dependency Tracing, and Impact Analysis Lab",
    [
        md("""
        ## Purpose

        This lab traces downstream dependencies from a source dataset to affected artifacts.
        """),
        code(provenance_setup),
        code("""
def downstream_dependencies(start_entity: str, relation_table: pd.DataFrame) -> set[str]:
    visited = set()
    frontier = [start_entity]

    while frontier:
        current = frontier.pop()

        if current in visited:
            continue

        visited.add(current)

        children = relation_table.loc[relation_table["source"] == current, "target"].tolist()
        frontier.extend(children)

    visited.remove(start_entity)
    return visited

impacted_by_source_b = downstream_dependencies("D_source_B", relations)

impact_table = pd.DataFrame([{
    "source_entity": "D_source_B",
    "impacted_nodes": ", ".join(sorted(impacted_by_source_b)),
    "model_impacted": "M_model_3" in impacted_by_source_b,
    "evaluation_impacted": "R_eval_3" in impacted_by_source_b,
}])

impact_table
        """),
        md("""
        ## Interpretation

        Impact analysis identifies which downstream artifacts must be reviewed when a source dataset changes or contains defects.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "03_dataset_documentation_fair_data_and_reproducibility_lab.ipynb",
    "Dataset Documentation, FAIR Data, and Reproducibility Lab",
    [
        md("""
        ## Purpose

        This lab models documentation and reproducibility readiness for AI data artifacts.
        """),
        code("""
import pandas as pd

documentation = pd.DataFrame([
    {
        "artifact": "D_source_A",
        "datasheet_complete": True,
        "rights_review_complete": True,
        "quality_review_complete": True,
        "fair_findable": True,
        "fair_accessible": True,
        "fair_interoperable": False,
        "fair_reusable": True,
    },
    {
        "artifact": "D_source_B",
        "datasheet_complete": False,
        "rights_review_complete": True,
        "quality_review_complete": False,
        "fair_findable": True,
        "fair_accessible": False,
        "fair_interoperable": False,
        "fair_reusable": False,
    },
    {
        "artifact": "M_model_3",
        "datasheet_complete": True,
        "rights_review_complete": True,
        "quality_review_complete": True,
        "fair_findable": True,
        "fair_accessible": True,
        "fair_interoperable": True,
        "fair_reusable": True,
    },
])

readiness_summary = documentation.drop(columns=["artifact"]).mean().reset_index()
readiness_summary.columns = ["criterion", "completion_rate"]

readiness_summary
        """),
        md("""
        ## Interpretation

        FAIR and documentation readiness can be summarized as governance metadata across datasets, models, and evaluation artifacts.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "04_mlops_governance_access_control_and_audit_readiness_lab.ipynb",
    "MLOps Governance, Access Control, and Audit Readiness Lab",
    [
        md("""
        ## Purpose

        This lab frames MLOps metadata as audit-readiness infrastructure.
        """),
        code("""
import pandas as pd

access_controls = pd.DataFrame([
    {"artifact": "D_source_A", "role": "data_engineer", "permission": "read_write", "approved": True},
    {"artifact": "D_source_B", "role": "ml_engineer", "permission": "read", "approved": True},
    {"artifact": "F_features_2", "role": "ml_engineer", "permission": "read_write", "approved": True},
    {"artifact": "M_model_3", "role": "ml_engineer", "permission": "deploy", "approved": True},
    {"artifact": "R_eval_3", "role": "governance_reviewer", "permission": "review", "approved": True},
])

audit_readiness = pd.DataFrame([
    {"area": "provenance_capture", "status": "complete", "owner": "Data Platform"},
    {"area": "lineage_queries", "status": "partial", "owner": "MLOps"},
    {"area": "quality_checks", "status": "partial", "owner": "Data Steward"},
    {"area": "rights_metadata", "status": "complete", "owner": "Governance"},
    {"area": "reproducibility", "status": "partial", "owner": "ML Engineering"},
])

audit_readiness.groupby("status").size().reset_index(name="count")
        """),
        md("""
        ## Interpretation

        Audit readiness depends on provenance capture, lineage queryability, quality controls, rights metadata, and reproducibility evidence.
        """),
    ],
)
