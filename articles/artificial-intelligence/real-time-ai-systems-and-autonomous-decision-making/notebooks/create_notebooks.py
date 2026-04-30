#!/usr/bin/env python3
"""
Create advanced Jupyter notebooks for:
Real-Time AI Systems and Autonomous Decision-Making
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


latency_setup = """
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

n = 1500

tasks = pd.DataFrame({
    "task_id": [f"rtai-{i:04d}" for i in range(1, n + 1)],
    "task_type": rng.choice(
        ["perception", "tracking", "planning", "control", "safety_monitor"],
        size=n,
        p=[0.32, 0.20, 0.18, 0.20, 0.10],
    ),
    "deadline_ms": rng.choice([20, 40, 80, 120], size=n, p=[0.20, 0.35, 0.30, 0.15]),
    "risk_level": rng.choice(["low", "medium", "high"], size=n, p=[0.45, 0.35, 0.20]),
})

latency_profiles = {
    "perception": (18, 8),
    "tracking": (10, 4),
    "planning": (35, 15),
    "control": (8, 3),
    "safety_monitor": (12, 5),
}

sense_latency = rng.normal(loc=5, scale=1.5, size=n)
pre_latency = rng.normal(loc=6, scale=2.0, size=n)

infer_latency = np.array([
    rng.normal(
        loc=latency_profiles[task_type][0],
        scale=latency_profiles[task_type][1],
    )
    for task_type in tasks["task_type"]
])

act_latency = rng.normal(loc=4, scale=1.0, size=n)

tasks["latency_ms"] = np.maximum(
    1,
    sense_latency + pre_latency + infer_latency + act_latency,
)

tasks["deadline_miss"] = tasks["latency_ms"] > tasks["deadline_ms"]
tasks["latency_margin_ms"] = tasks["deadline_ms"] - tasks["latency_ms"]

tasks.head()
"""

write(
    NOTEBOOK_DIR / "01_latency_deadlines_and_deadline_miss_diagnostics_lab.ipynb",
    "Latency, Deadlines, and Deadline-Miss Diagnostics Lab",
    [
        md("""
        ## Purpose

        This lab evaluates end-to-end latency, deadline misses, and latency margins for real-time AI tasks.
        """),
        code(latency_setup),
        code("""
summary = (
    tasks
    .groupby("task_type")
    .agg(
        tasks=("task_id", "count"),
        mean_latency_ms=("latency_ms", "mean"),
        p95_latency_ms=("latency_ms", lambda x: np.percentile(x, 95)),
        p99_latency_ms=("latency_ms", lambda x: np.percentile(x, 99)),
        deadline_miss_rate=("deadline_miss", "mean"),
        mean_latency_margin_ms=("latency_margin_ms", "mean"),
    )
    .reset_index()
)

summary.sort_values("deadline_miss_rate", ascending=False)
        """),
        md("""
        ## Interpretation

        Real-time AI should be evaluated with p95, p99, deadline misses, and latency margins, not average inference time alone.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "02_schedulability_utilization_and_task_priority_lab.ipynb",
    "Schedulability, Utilization, and Task Priority Lab",
    [
        md("""
        ## Purpose

        This lab introduces task utilization and simple schedulability diagnostics.
        """),
        code("""
import pandas as pd

task_set = pd.DataFrame([
    {"task": "sensor_read", "execution_ms": 2.0, "period_ms": 10.0, "deadline_ms": 10.0, "priority": 1},
    {"task": "perception_model", "execution_ms": 18.0, "period_ms": 40.0, "deadline_ms": 40.0, "priority": 3},
    {"task": "tracking_filter", "execution_ms": 6.0, "period_ms": 20.0, "deadline_ms": 20.0, "priority": 2},
    {"task": "planner", "execution_ms": 24.0, "period_ms": 80.0, "deadline_ms": 80.0, "priority": 4},
    {"task": "safety_monitor", "execution_ms": 4.0, "period_ms": 20.0, "deadline_ms": 20.0, "priority": 1},
    {"task": "actuator_command", "execution_ms": 2.0, "period_ms": 10.0, "deadline_ms": 10.0, "priority": 1},
])

task_set["utilization"] = task_set["execution_ms"] / task_set["period_ms"]

total_utilization = task_set["utilization"].sum()

task_set, total_utilization
        """),
        md("""
        ## Interpretation

        Utilization is not a full schedulability proof, but it is a useful first diagnostic for real-time workload pressure.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "03_runtime_assurance_fallback_and_safety_gating_lab.ipynb",
    "Runtime Assurance, Fallback, and Safety Gating Lab",
    [
        md("""
        ## Purpose

        This lab simulates safety-gated autonomous action based on risk and timing.
        """),
        code("""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
n = 1000

events = pd.DataFrame({
    "event_id": range(n),
    "risk_score": rng.beta(2.5, 4.0, size=n),
    "latency_ms": rng.normal(45, 18, size=n),
    "deadline_ms": rng.choice([40, 80, 120], size=n, p=[0.40, 0.45, 0.15]),
})

events["deadline_miss"] = events["latency_ms"] > events["deadline_ms"]
events["fallback_used"] = (events["risk_score"] > 0.65) | events["deadline_miss"]
events["action_mode"] = np.where(events["fallback_used"], "safe_fallback", "ai_action")

events.groupby("action_mode").agg(
    events=("event_id", "count"),
    mean_risk=("risk_score", "mean"),
    mean_latency=("latency_ms", "mean"),
    deadline_miss_rate=("deadline_miss", "mean"),
).reset_index()
        """),
        md("""
        ## Interpretation

        Runtime assurance treats fallback behavior as a designed safety function, not as an emergency afterthought.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "04_edge_inference_autonomy_governance_and_monitoring_lab.ipynb",
    "Edge Inference, Autonomy Governance, and Monitoring Lab",
    [
        md("""
        ## Purpose

        This lab frames real-time AI deployment as a governance and monitoring problem.
        """),
        code("""
import pandas as pd

deployment_review = pd.DataFrame([
    {
        "area": "latency_budget",
        "question": "Is end-to-end latency measured against operational deadlines?",
        "status": "partial",
        "owner": "Systems Engineering",
    },
    {
        "area": "edge_inference",
        "question": "Is edge inference required to meet deadline and resilience needs?",
        "status": "complete",
        "owner": "Infrastructure",
    },
    {
        "area": "safety_monitor",
        "question": "Is the safety monitor scheduled with sufficient priority?",
        "status": "partial",
        "owner": "Safety",
    },
    {
        "area": "fallback",
        "question": "Is fallback behavior tested under overload and deadline misses?",
        "status": "partial",
        "owner": "Operations",
    },
    {
        "area": "human_override",
        "question": "Can human supervisors pause or override autonomy?",
        "status": "complete",
        "owner": "Governance",
    },
])

deployment_review.groupby("status").size().reset_index(name="count")
        """),
        md("""
        ## Interpretation

        Real-time AI governance requires evidence about timing, fallback, edge deployment, safety monitors, and human override.
        """),
    ],
)
