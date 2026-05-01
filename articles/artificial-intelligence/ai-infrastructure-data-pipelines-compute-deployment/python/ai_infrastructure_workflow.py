"""
AI Infrastructure: Data Pipelines, Compute, and Deployment Systems Mini-Workflow

This script demonstrates:
- pipeline DAG metadata
- compute utilization diagnostics
- serving-capacity estimation
- latency-budget analysis
- infrastructure readiness scoring

It is educational and uses synthetic data.
"""

from __future__ import annotations

from pathlib import Path

import math
import pandas as pd


OUTPUT_DIR = Path("../outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def build_pipeline_tasks() -> pd.DataFrame:
    """Create synthetic AI pipeline task metadata."""
    return pd.DataFrame(
        {
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
        }
    )


def build_pipeline_edges() -> pd.DataFrame:
    """Create synthetic DAG edges for the AI pipeline."""
    return pd.DataFrame(
        {
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
        }
    )


def build_compute_cluster() -> pd.DataFrame:
    """Create synthetic compute cluster utilization data."""
    compute_cluster = pd.DataFrame(
        {
            "resource": [
                "gpu_pool_a",
                "gpu_pool_b",
                "cpu_feature_workers",
                "model_serving_pool",
            ],
            "available_units": [32, 16, 80, 12],
            "allocated_units": [26, 14, 52, 9],
            "utilization_target": [0.85, 0.85, 0.70, 0.75],
        }
    )

    compute_cluster["utilization"] = (
        compute_cluster["allocated_units"] / compute_cluster["available_units"]
    )

    compute_cluster["over_target"] = (
        compute_cluster["utilization"] > compute_cluster["utilization_target"]
    )

    return compute_cluster


def build_serving_plan() -> pd.DataFrame:
    """Create synthetic serving-capacity and latency data."""
    serving = pd.DataFrame(
        {
            "service": ["risk_model_api"],
            "required_qps": [1200],
            "throughput_per_replica": [150],
            "feature_latency_ms": [45],
            "model_latency_ms": [80],
            "network_latency_ms": [35],
            "postprocess_latency_ms": [20],
            "latency_budget_ms": [200],
        }
    )

    serving["required_replicas"] = (
        serving["required_qps"] / serving["throughput_per_replica"]
    ).apply(math.ceil)

    serving["total_latency_ms"] = (
        serving["feature_latency_ms"]
        + serving["model_latency_ms"]
        + serving["network_latency_ms"]
        + serving["postprocess_latency_ms"]
    )

    serving["meets_latency_budget"] = (
        serving["total_latency_ms"] <= serving["latency_budget_ms"]
    )

    return serving


def build_readiness_scores() -> pd.DataFrame:
    """Create synthetic infrastructure readiness scores."""
    readiness = pd.DataFrame(
        [
            {"dimension": "data_pipeline", "score": 0.82},
            {"dimension": "compute_capacity", "score": 0.76},
            {"dimension": "storage_throughput", "score": 0.80},
            {"dimension": "serving_reliability", "score": 0.84},
            {"dimension": "observability", "score": 0.78},
            {"dimension": "security_controls", "score": 0.74},
            {"dimension": "governance_controls", "score": 0.72},
        ]
    )

    return readiness


def compute_pipeline_reliability(tasks: pd.DataFrame) -> float:
    """Compute simple pipeline reliability under independent failure assumption."""
    reliability = 1.0

    for p in tasks["failure_probability"]:
        reliability *= (1 - p)

    return reliability


def main() -> None:
    tasks = build_pipeline_tasks()
    edges = build_pipeline_edges()
    compute_cluster = build_compute_cluster()
    serving = build_serving_plan()
    readiness = build_readiness_scores()

    pipeline_reliability = compute_pipeline_reliability(tasks)
    infrastructure_readiness_score = readiness["score"].mean()

    summary = pd.DataFrame(
        [
            {"metric": "pipeline_total_duration_minutes", "value": tasks["duration_minutes"].sum()},
            {"metric": "pipeline_reliability", "value": pipeline_reliability},
            {"metric": "mean_compute_utilization", "value": compute_cluster["utilization"].mean()},
            {"metric": "serving_required_replicas", "value": serving["required_replicas"].iloc[0]},
            {"metric": "serving_total_latency_ms", "value": serving["total_latency_ms"].iloc[0]},
            {"metric": "infrastructure_readiness_score", "value": infrastructure_readiness_score},
        ]
    )

    tasks.to_csv(OUTPUT_DIR / "pipeline_tasks.csv", index=False)
    edges.to_csv(OUTPUT_DIR / "pipeline_edges.csv", index=False)
    compute_cluster.to_csv(OUTPUT_DIR / "compute_cluster_utilization.csv", index=False)
    serving.to_csv(OUTPUT_DIR / "serving_capacity_latency.csv", index=False)
    readiness.to_csv(OUTPUT_DIR / "infrastructure_readiness_scores.csv", index=False)
    summary.to_csv(OUTPUT_DIR / "infrastructure_summary.csv", index=False)

    print(tasks)
    print(edges)
    print(compute_cluster)
    print(serving)
    print(readiness)
    print(summary)


if __name__ == "__main__":
    main()
