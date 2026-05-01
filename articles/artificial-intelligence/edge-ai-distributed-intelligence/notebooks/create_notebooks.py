#!/usr/bin/env python3
"""
Create advanced Jupyter notebooks for:
Edge AI and Distributed Intelligence
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


setup = """
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

nodes = pd.DataFrame({
    "node_id": [f"edge_node_{i:02d}" for i in range(1, 9)],
    "local_examples": rng.integers(250, 1800, size=8),
    "edge_inference_ms": rng.uniform(18, 70, size=8),
    "local_action_ms": rng.uniform(8, 25, size=8),
    "uplink_ms": rng.uniform(35, 90, size=8),
    "cloud_inference_ms": rng.uniform(25, 45, size=8),
    "downlink_ms": rng.uniform(30, 80, size=8),
    "raw_bandwidth_mb_s": rng.uniform(20, 150, size=8),
    "edge_output_mb_s": rng.uniform(1, 8, size=8),
    "node_trust": rng.uniform(0.70, 0.98, size=8),
    "governance_review_complete": rng.choice([0, 1], size=8, p=[0.25, 0.75]),
})
"""

write(
    NOTEBOOK_DIR / "01_edge_architectures_latency_bandwidth_and_resource_constraints_lab.ipynb",
    "Edge Architectures, Latency, Bandwidth, and Resource Constraints Lab",
    [
        md("""
        ## Purpose

        This lab compares edge and cloud latency while estimating bandwidth savings from local processing.
        """),
        code(setup),
        code("""
nodes["cloud_latency_ms"] = nodes["uplink_ms"] + nodes["cloud_inference_ms"] + nodes["downlink_ms"]
nodes["edge_latency_ms"] = nodes["edge_inference_ms"] + nodes["local_action_ms"]
nodes["latency_savings_ms"] = nodes["cloud_latency_ms"] - nodes["edge_latency_ms"]
nodes["bandwidth_savings"] = 1 - nodes["edge_output_mb_s"] / nodes["raw_bandwidth_mb_s"]

nodes[[
    "node_id",
    "edge_latency_ms",
    "cloud_latency_ms",
    "latency_savings_ms",
    "bandwidth_savings",
]]
        """),
        md("""
        ## Interpretation

        Edge inference can satisfy real-time constraints and reduce bandwidth when local outputs replace raw data transmission.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "02_federated_learning_fedavg_and_non_iid_client_diagnostics_lab.ipynb",
    "Federated Learning, FedAvg, and Non-IID Client Diagnostics Lab",
    [
        md("""
        ## Purpose

        This lab simulates one round of weighted federated averaging.
        """),
        code(setup),
        code("""
parameter_dimension = 5

client_updates = pd.DataFrame(
    rng.normal(0.0, 1.0, size=(len(nodes), parameter_dimension)),
    columns=[f"param_{j}" for j in range(parameter_dimension)],
)

client_updates["node_id"] = nodes["node_id"]
client_updates["local_examples"] = nodes["local_examples"]

weights = client_updates["local_examples"] / client_updates["local_examples"].sum()

global_update = {}

for column in [f"param_{j}" for j in range(parameter_dimension)]:
    global_update[column] = float((weights * client_updates[column]).sum())

global_update_table = pd.DataFrame([global_update])

client_updates, global_update_table
        """),
        md("""
        ## Interpretation

        FedAvg combines local model updates into a global update, often weighting clients by local data volume.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "03_resilience_node_failure_and_distributed_risk_lab.ipynb",
    "Resilience, Node Failure, and Distributed Risk Lab",
    [
        md("""
        ## Purpose

        This lab estimates node-level deployment feasibility and distributed risk.
        """),
        code(setup),
        code("""
nodes["compute_capacity"] = rng.uniform(0.45, 0.95, size=len(nodes))
nodes["model_compute_demand"] = rng.uniform(0.30, 0.90, size=len(nodes))
nodes["memory_capacity"] = rng.uniform(0.40, 0.95, size=len(nodes))
nodes["model_memory_demand"] = rng.uniform(0.25, 0.90, size=len(nodes))
nodes["energy_budget"] = rng.uniform(0.45, 0.95, size=len(nodes))
nodes["model_energy_demand"] = rng.uniform(0.25, 0.88, size=len(nodes))

nodes["compute_feasible"] = nodes["model_compute_demand"] <= nodes["compute_capacity"]
nodes["memory_feasible"] = nodes["model_memory_demand"] <= nodes["memory_capacity"]
nodes["energy_feasible"] = nodes["model_energy_demand"] <= nodes["energy_budget"]

nodes["edge_latency_ms"] = nodes["edge_inference_ms"] + nodes["local_action_ms"]
nodes["latency_feasible"] = nodes["edge_latency_ms"] <= 100

nodes["deployment_feasible"] = (
    nodes["compute_feasible"]
    & nodes["memory_feasible"]
    & nodes["energy_feasible"]
    & nodes["latency_feasible"]
)

nodes["distributed_risk"] = (
    0.35 * (1 - nodes["node_trust"])
    + 0.30 * (1 - nodes["governance_review_complete"])
    + 0.35 * (~nodes["deployment_feasible"]).astype(int)
)

nodes[["node_id", "deployment_feasible", "node_trust", "distributed_risk"]].sort_values(
    "distributed_risk",
    ascending=False,
)
        """),
        md("""
        ## Interpretation

        Distributed risk increases when node trust, deployment feasibility, or governance review coverage is weak.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "04_edge_governance_security_privacy_and_auditability_lab.ipynb",
    "Edge Governance, Security, Privacy, and Auditability Lab",
    [
        md("""
        ## Purpose

        This lab models governance coverage across distributed edge AI controls.
        """),
        code("""
import pandas as pd

controls = pd.DataFrame({
    "control": [
        "node_inventory",
        "signed_model_updates",
        "secure_aggregation",
        "data_rights_metadata",
        "latency_safety_review",
        "fallback_mode",
        "audit_logging",
        "incident_response",
    ],
    "coverage": [0.90, 0.72, 0.54, 0.64, 0.70, 0.76, 0.68, 0.58],
    "criticality": [0.80, 0.88, 0.82, 0.84, 0.90, 0.92, 0.86, 0.88],
})

controls["governance_gap"] = controls["criticality"] - controls["coverage"]
controls["needs_action"] = controls["governance_gap"] > 0.15

controls.sort_values("governance_gap", ascending=False)
        """),
        md("""
        ## Interpretation

        Edge AI governance must cover node inventory, update control, data rights, latency safety, fallback behavior, auditability, and incident response.
        """),
    ],
)
