"""
Edge AI and Distributed Intelligence Mini-Workflow

This script demonstrates:
- edge-node resource profiles
- cloud versus edge latency analysis
- bandwidth savings from local processing
- federated averaging
- node-level governance diagnostics

It is educational and uses synthetic data.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


OUTPUT_DIR = Path("../outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(42)


def build_edge_nodes(n_nodes: int = 8) -> pd.DataFrame:
    """Create synthetic edge-node profiles."""
    nodes = pd.DataFrame(
        {
            "node_id": [f"edge_node_{i:02d}" for i in range(1, n_nodes + 1)],
            "local_examples": rng.integers(250, 1800, size=n_nodes),
            "edge_inference_ms": rng.uniform(18, 70, size=n_nodes),
            "local_action_ms": rng.uniform(8, 25, size=n_nodes),
            "uplink_ms": rng.uniform(35, 90, size=n_nodes),
            "cloud_inference_ms": rng.uniform(25, 45, size=n_nodes),
            "downlink_ms": rng.uniform(30, 80, size=n_nodes),
            "raw_bandwidth_mb_s": rng.uniform(20, 150, size=n_nodes),
            "edge_output_mb_s": rng.uniform(1, 8, size=n_nodes),
            "compute_capacity": rng.uniform(0.45, 0.95, size=n_nodes),
            "model_compute_demand": rng.uniform(0.30, 0.90, size=n_nodes),
            "memory_capacity": rng.uniform(0.40, 0.95, size=n_nodes),
            "model_memory_demand": rng.uniform(0.25, 0.90, size=n_nodes),
            "energy_budget": rng.uniform(0.45, 0.95, size=n_nodes),
            "model_energy_demand": rng.uniform(0.25, 0.88, size=n_nodes),
            "node_trust": rng.uniform(0.70, 0.98, size=n_nodes),
            "governance_review_complete": rng.choice([0, 1], size=n_nodes, p=[0.25, 0.75]),
        }
    )

    nodes["cloud_latency_ms"] = (
        nodes["uplink_ms"]
        + nodes["cloud_inference_ms"]
        + nodes["downlink_ms"]
    )

    nodes["edge_latency_ms"] = (
        nodes["edge_inference_ms"]
        + nodes["local_action_ms"]
    )

    nodes["latency_savings_ms"] = (
        nodes["cloud_latency_ms"]
        - nodes["edge_latency_ms"]
    )

    nodes["bandwidth_savings"] = (
        1 - nodes["edge_output_mb_s"] / nodes["raw_bandwidth_mb_s"]
    )

    nodes["compute_feasible"] = (
        nodes["model_compute_demand"] <= nodes["compute_capacity"]
    )

    nodes["memory_feasible"] = (
        nodes["model_memory_demand"] <= nodes["memory_capacity"]
    )

    nodes["energy_feasible"] = (
        nodes["model_energy_demand"] <= nodes["energy_budget"]
    )

    nodes["edge_meets_budget"] = nodes["edge_latency_ms"] <= 100
    nodes["cloud_meets_budget"] = nodes["cloud_latency_ms"] <= 100

    nodes["deployment_feasible"] = (
        nodes["compute_feasible"]
        & nodes["memory_feasible"]
        & nodes["energy_feasible"]
        & nodes["edge_meets_budget"]
    )

    nodes["resource_margin"] = (
        0.34 * (nodes["compute_capacity"] - nodes["model_compute_demand"])
        + 0.33 * (nodes["memory_capacity"] - nodes["model_memory_demand"])
        + 0.33 * (nodes["energy_budget"] - nodes["model_energy_demand"])
    )

    nodes["distributed_risk"] = (
        0.35 * (1 - nodes["node_trust"])
        + 0.30 * (1 - nodes["governance_review_complete"])
        + 0.20 * (~nodes["deployment_feasible"]).astype(int)
        + 0.15 * np.maximum(0, -nodes["resource_margin"])
    )

    return nodes


def federated_average(nodes: pd.DataFrame, parameter_dimension: int = 5) -> pd.DataFrame:
    """Simulate one round of federated averaging."""
    client_updates = pd.DataFrame(
        rng.normal(loc=0.0, scale=1.0, size=(len(nodes), parameter_dimension)),
        columns=[f"param_{j}" for j in range(parameter_dimension)],
    )

    client_updates["node_id"] = nodes["node_id"].to_numpy()
    client_updates["local_examples"] = nodes["local_examples"].to_numpy()

    total_examples = client_updates["local_examples"].sum()
    weights = client_updates["local_examples"] / total_examples

    global_update = {}

    for column in [f"param_{j}" for j in range(parameter_dimension)]:
        global_update[column] = float((weights * client_updates[column]).sum())

    return pd.DataFrame([global_update])


def summarize(nodes: pd.DataFrame) -> pd.DataFrame:
    """Create edge AI and governance summary metrics."""
    return pd.DataFrame(
        [
            {"metric": "share_edge_meets_latency_budget", "value": nodes["edge_meets_budget"].mean()},
            {"metric": "share_cloud_meets_latency_budget", "value": nodes["cloud_meets_budget"].mean()},
            {"metric": "mean_bandwidth_savings", "value": nodes["bandwidth_savings"].mean()},
            {"metric": "share_deployment_feasible", "value": nodes["deployment_feasible"].mean()},
            {"metric": "mean_node_trust", "value": nodes["node_trust"].mean()},
            {"metric": "mean_distributed_risk", "value": nodes["distributed_risk"].mean()},
            {"metric": "share_governance_review_complete", "value": nodes["governance_review_complete"].mean()},
        ]
    )


def main() -> None:
    nodes = build_edge_nodes()
    global_update = federated_average(nodes)
    summary = summarize(nodes)

    nodes.to_csv(OUTPUT_DIR / "edge_ai_nodes.csv", index=False)
    global_update.to_csv(OUTPUT_DIR / "federated_average_global_update.csv", index=False)
    summary.to_csv(OUTPUT_DIR / "edge_ai_summary.csv", index=False)

    print(nodes[
        [
            "node_id",
            "edge_latency_ms",
            "cloud_latency_ms",
            "latency_savings_ms",
            "bandwidth_savings",
            "deployment_feasible",
            "distributed_risk",
        ]
    ])

    print(global_update)
    print(summary)


if __name__ == "__main__":
    main()
