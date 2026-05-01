#!/usr/bin/env python3
"""
Create advanced Jupyter notebooks for:
AI Infrastructure: Data Pipelines, Compute, and Deployment Systems
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


pipeline_setup = """
import pandas as pd

pipeline_tasks = pd.DataFrame({
    "task": [
        "ingest_raw_data",
        "validate_schema",
        "transform_records",
        "build_features",
        "train_model",
        "evaluate_model",
        "register_model",
        "deploy_model",
        "monitor_predictions",
    ],
    "duration_minutes": [18, 7, 24, 16, 95, 20, 6, 12, 5],
    "failure_probability": [0.03, 0.02, 0.05, 0.04, 0.06, 0.03, 0.01, 0.02, 0.02],
    "governance_gate": [False, True, False, True, False, True, True, True, False],
})

pipeline_edges = pd.DataFrame({
    "source": [
        "ingest_raw_data",
        "validate_schema",
        "transform_records",
        "build_features",
        "train_model",
        "evaluate_model",
        "register_model",
        "deploy_model",
    ],
    "target": [
        "validate_schema",
        "transform_records",
        "build_features",
        "train_model",
        "evaluate_model",
        "register_model",
        "deploy_model",
        "monitor_predictions",
    ],
})
"""

write(
    NOTEBOOK_DIR / "01_pipeline_dags_data_validation_and_lineage_lab.ipynb",
    "Pipeline DAGs, Data Validation, and Lineage Lab",
    [
        md("""
        ## Purpose

        This lab models an AI pipeline as a directed acyclic graph with task durations, failure probabilities, and governance gates.
        """),
        code(pipeline_setup),
        code("""
pipeline_total_duration = pipeline_tasks["duration_minutes"].sum()

pipeline_reliability = 1.0
for p in pipeline_tasks["failure_probability"]:
    pipeline_reliability *= (1 - p)

governance_gate_count = pipeline_tasks["governance_gate"].sum()

summary = pd.DataFrame([
    {"metric": "pipeline_total_duration_minutes", "value": pipeline_total_duration},
    {"metric": "pipeline_reliability", "value": pipeline_reliability},
    {"metric": "governance_gate_count", "value": governance_gate_count},
])

pipeline_tasks, pipeline_edges, summary
        """),
        md("""
        ## Interpretation

        Production pipelines should be evaluated as dependency systems with failure probabilities and explicit governance checkpoints.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "02_compute_accelerators_distributed_training_and_utilization_lab.ipynb",
    "Compute Accelerators, Distributed Training, and Utilization Lab",
    [
        md("""
        ## Purpose

        This lab evaluates compute utilization across AI infrastructure resource pools.
        """),
        code("""
import pandas as pd

compute_cluster = pd.DataFrame({
    "resource": ["gpu_pool_a", "gpu_pool_b", "cpu_feature_workers", "model_serving_pool"],
    "available_units": [32, 16, 80, 12],
    "allocated_units": [26, 14, 52, 9],
    "utilization_target": [0.85, 0.85, 0.70, 0.75],
})

compute_cluster["utilization"] = compute_cluster["allocated_units"] / compute_cluster["available_units"]
compute_cluster["over_target"] = compute_cluster["utilization"] > compute_cluster["utilization_target"]
compute_cluster["available_headroom"] = 1 - compute_cluster["utilization"]

compute_cluster
        """),
        md("""
        ## Interpretation

        Compute infrastructure must balance high utilization against headroom for reliability, scaling, and workload variation.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "03_model_serving_latency_capacity_and_reliability_lab.ipynb",
    "Model Serving, Latency, Capacity, and Reliability Lab",
    [
        md("""
        ## Purpose

        This lab estimates serving replicas, total latency, and service-level feasibility.
        """),
        code("""
import math
import pandas as pd

serving = pd.DataFrame({
    "service": ["risk_model_api"],
    "required_qps": [1200],
    "throughput_per_replica": [150],
    "feature_latency_ms": [45],
    "model_latency_ms": [80],
    "network_latency_ms": [35],
    "postprocess_latency_ms": [20],
    "latency_budget_ms": [200],
})

serving["required_replicas"] = (
    serving["required_qps"] / serving["throughput_per_replica"]
).apply(math.ceil)

serving["total_latency_ms"] = (
    serving["feature_latency_ms"]
    + serving["model_latency_ms"]
    + serving["network_latency_ms"]
    + serving["postprocess_latency_ms"]
)

serving["meets_latency_budget"] = serving["total_latency_ms"] <= serving["latency_budget_ms"]

serving
        """),
        md("""
        ## Interpretation

        Serving readiness depends on end-to-end latency, replica planning, throughput, feature lookup, and rollback capacity.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "04_observability_mlops_governance_and_technical_debt_lab.ipynb",
    "Observability, MLOps Governance, and Technical Debt Lab",
    [
        md("""
        ## Purpose

        This lab scores AI infrastructure readiness and technical debt across operational components.
        """),
        code("""
import pandas as pd

components = pd.DataFrame({
    "component": [
        "data_pipeline",
        "feature_store",
        "training_cluster",
        "model_registry",
        "serving_layer",
        "observability",
        "security_controls",
        "governance_controls",
    ],
    "readiness_score": [0.82, 0.76, 0.78, 0.84, 0.80, 0.72, 0.74, 0.70],
    "technical_debt": [0.28, 0.34, 0.30, 0.20, 0.25, 0.42, 0.36, 0.40],
    "criticality": [0.95, 0.90, 0.92, 0.82, 0.94, 0.88, 0.90, 0.92],
})

components["weighted_risk"] = components["technical_debt"] * components["criticality"]

components["priority"] = pd.cut(
    components["weighted_risk"],
    bins=[0.0, 0.25, 0.35, 1.0],
    labels=["low", "medium", "high"],
    include_lowest=True,
)

components.sort_values("weighted_risk", ascending=False)
        """),
        md("""
        ## Interpretation

        Infrastructure governance should prioritize components where technical debt and criticality combine to create high operational risk.
        """),
    ],
)
