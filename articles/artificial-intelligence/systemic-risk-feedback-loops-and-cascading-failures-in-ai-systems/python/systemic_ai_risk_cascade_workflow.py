"""
Systemic Risk, Feedback Loops, and Cascading Failures Mini-Workflow

This script demonstrates:
- synthetic dependency networks
- initial component failure
- threshold-based cascade propagation
- cascade-size measurement
- resilience improvement through buffers

It is educational and uses synthetic data.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


OUTPUT_DIR = Path("../outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

RANDOM_SEED = 42


def build_dependency_network(
    n_components: int = 18,
    connection_probability: float = 0.25,
) -> tuple[list[str], np.ndarray, np.ndarray]:
    """Create a synthetic weighted dependency network."""
    rng = np.random.default_rng(RANDOM_SEED)

    components = [f"component_{i:02d}" for i in range(1, n_components + 1)]

    dependency_matrix = rng.uniform(0, 0.35, size=(n_components, n_components))
    np.fill_diagonal(dependency_matrix, 0)

    mask = rng.binomial(
        1,
        connection_probability,
        size=(n_components, n_components),
    )

    dependency_matrix = dependency_matrix * mask

    thresholds = rng.uniform(0.25, 0.75, size=n_components)

    return components, dependency_matrix, thresholds


def simulate_cascade(
    dependency_matrix: np.ndarray,
    thresholds: np.ndarray,
    initial_failures: list[int],
    buffer_strength: float = 0.0,
    max_steps: int = 10,
) -> pd.DataFrame:
    """
    Simulate threshold-based failure propagation.

    A component fails when pressure from failed dependencies exceeds
    its threshold plus any buffer strength.
    """
    n = dependency_matrix.shape[0]

    state = np.ones(n, dtype=int)
    state[initial_failures] = 0

    rows: list[dict[str, float | int]] = []

    for step in range(max_steps + 1):
        failed = 1 - state
        pressure = dependency_matrix @ failed

        rows.append(
            {
                "step": step,
                "failed_count": int(np.sum(failed)),
                "failed_fraction": float(np.mean(failed)),
                "max_dependency_pressure": float(np.max(pressure)),
                "mean_dependency_pressure": float(np.mean(pressure)),
                "buffer_strength": buffer_strength,
            }
        )

        new_failures = (
            (pressure > (thresholds + buffer_strength))
            & (state == 1)
        )

        if not np.any(new_failures):
            break

        state[new_failures] = 0

    return pd.DataFrame(rows)


def run_scenarios() -> pd.DataFrame:
    """Run baseline and resilience-buffer cascade scenarios."""
    _, dependency_matrix, thresholds = build_dependency_network()

    scenario_frames = []

    for buffer_strength, scenario_name in [
        (0.00, "baseline"),
        (0.10, "small_buffer"),
        (0.20, "medium_buffer"),
        (0.35, "large_buffer"),
    ]:
        scenario = simulate_cascade(
            dependency_matrix=dependency_matrix,
            thresholds=thresholds,
            initial_failures=[0, 3],
            buffer_strength=buffer_strength,
        )

        scenario["scenario"] = scenario_name
        scenario_frames.append(scenario)

    return pd.concat(scenario_frames, ignore_index=True)


def main() -> None:
    results = run_scenarios()

    final_summary = (
        results
        .sort_values(["scenario", "step"])
        .groupby("scenario")
        .tail(1)
        .reset_index(drop=True)
    )

    results.to_csv(OUTPUT_DIR / "systemic_ai_cascade_simulation.csv", index=False)
    final_summary.to_csv(OUTPUT_DIR / "systemic_ai_cascade_summary.csv", index=False)

    print(results)
    print(final_summary)


if __name__ == "__main__":
    main()
