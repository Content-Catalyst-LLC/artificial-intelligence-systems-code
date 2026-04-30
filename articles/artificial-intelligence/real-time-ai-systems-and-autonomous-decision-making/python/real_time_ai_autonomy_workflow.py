"""
Real-Time AI Systems and Autonomous Decision-Making Mini-Workflow

This script demonstrates:
- synthetic real-time AI task data
- component latency simulation
- deadline-miss diagnostics
- utilization scoring
- safety fallback flags

It is educational and uses synthetic data.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


OUTPUT_DIR = Path("../outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

RANDOM_SEED = 42
rng = np.random.default_rng(RANDOM_SEED)


def build_task_data(n: int = 1500) -> pd.DataFrame:
    """Create synthetic real-time AI task data."""
    tasks = pd.DataFrame(
        {
            "task_id": [f"rtai-{i:04d}" for i in range(1, n + 1)],
            "task_type": rng.choice(
                ["perception", "tracking", "planning", "control", "safety_monitor"],
                size=n,
                p=[0.32, 0.20, 0.18, 0.20, 0.10],
            ),
            "deadline_ms": rng.choice(
                [20, 40, 80, 120],
                size=n,
                p=[0.20, 0.35, 0.30, 0.15],
            ),
            "risk_level": rng.choice(
                ["low", "medium", "high"],
                size=n,
                p=[0.45, 0.35, 0.20],
            ),
        }
    )

    latency_profiles = {
        "perception": (18, 8),
        "tracking": (10, 4),
        "planning": (35, 15),
        "control": (8, 3),
        "safety_monitor": (12, 5),
    }

    sense_latency = rng.normal(loc=5, scale=1.5, size=n)
    pre_latency = rng.normal(loc=6, scale=2.0, size=n)

    infer_latency = np.array(
        [
            rng.normal(
                loc=latency_profiles[task_type][0],
                scale=latency_profiles[task_type][1],
            )
            for task_type in tasks["task_type"]
        ]
    )

    act_latency = rng.normal(loc=4, scale=1.0, size=n)

    tasks["latency_ms"] = np.maximum(
        1,
        sense_latency + pre_latency + infer_latency + act_latency,
    )

    return tasks


def score_real_time_feasibility(tasks: pd.DataFrame) -> pd.DataFrame:
    """Compute deadline misses, latency margins, and fallback flags."""
    scored = tasks.copy()

    scored["deadline_miss"] = scored["latency_ms"] > scored["deadline_ms"]
    scored["latency_margin_ms"] = scored["deadline_ms"] - scored["latency_ms"]

    scored["fallback_required"] = (
        scored["deadline_miss"]
        | (
            (scored["risk_level"] == "high")
            & (scored["latency_margin_ms"] < 10)
        )
    )

    scored["timing_risk_score"] = np.clip(
        1 - (scored["latency_margin_ms"] / scored["deadline_ms"]),
        0,
        2,
    )

    return scored


def summarize(scored: pd.DataFrame) -> pd.DataFrame:
    """Summarize latency and risk diagnostics by task type and risk level."""
    return (
        scored
        .groupby(["task_type", "risk_level"])
        .agg(
            tasks=("task_id", "count"),
            mean_latency_ms=("latency_ms", "mean"),
            p95_latency_ms=("latency_ms", lambda x: np.percentile(x, 95)),
            mean_deadline_ms=("deadline_ms", "mean"),
            deadline_miss_rate=("deadline_miss", "mean"),
            fallback_rate=("fallback_required", "mean"),
            mean_latency_margin_ms=("latency_margin_ms", "mean"),
            mean_timing_risk_score=("timing_risk_score", "mean"),
        )
        .reset_index()
    )


def main() -> None:
    tasks = build_task_data()
    scored = score_real_time_feasibility(tasks)
    summary = summarize(scored)

    scored.to_csv(OUTPUT_DIR / "real_time_ai_latency_results.csv", index=False)
    summary.to_csv(OUTPUT_DIR / "real_time_ai_latency_summary.csv", index=False)

    print(summary.sort_values("deadline_miss_rate", ascending=False).head(10))
    print(scored.head())


if __name__ == "__main__":
    main()
