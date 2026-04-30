#!/usr/bin/env python3
"""
Create advanced Jupyter notebooks for:
Systemic Risk, Feedback Loops, and Cascading Failures in AI Systems
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


write(
    NOTEBOOK_DIR / "01_dependency_networks_and_cascade_propagation_lab.ipynb",
    "Dependency Networks and Cascade Propagation Lab",
    [
        md("""
        ## Purpose

        This lab simulates how local failures propagate through an AI-system dependency network.
        """),
        code("""
        import numpy as np
        import pandas as pd

        rng = np.random.default_rng(42)

        n = 18
        A = rng.uniform(0, 0.35, size=(n, n))
        np.fill_diagonal(A, 0)

        mask = rng.binomial(1, 0.25, size=(n, n))
        A = A * mask

        thresholds = rng.uniform(0.25, 0.75, size=n)

        def simulate_cascade(initial_failures, buffer_strength=0.0, max_steps=10):
            state = np.ones(n, dtype=int)
            state[initial_failures] = 0

            rows = []

            for step in range(max_steps + 1):
                failed = 1 - state
                pressure = A @ failed

                rows.append({
                    "step": step,
                    "failed_count": int(np.sum(failed)),
                    "failed_fraction": float(np.mean(failed)),
                    "max_pressure": float(np.max(pressure)),
                    "mean_pressure": float(np.mean(pressure)),
                })

                new_failures = (pressure > thresholds + buffer_strength) & (state == 1)

                if not np.any(new_failures):
                    break

                state[new_failures] = 0

            return pd.DataFrame(rows)

        baseline = simulate_cascade([0, 3], buffer_strength=0.0)
        buffered = simulate_cascade([0, 3], buffer_strength=0.20)

        baseline["scenario"] = "baseline"
        buffered["scenario"] = "buffered"

        pd.concat([baseline, buffered], ignore_index=True)
        """),
        md("""
        ## Interpretation

        Buffers and thresholds can determine whether a local failure remains contained or becomes a cascade.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "02_feedback_loops_and_self_reinforcing_dynamics_lab.ipynb",
    "Feedback Loops and Self-Reinforcing Dynamics Lab",
    [
        md("""
        ## Purpose

        This lab simulates stabilizing and destabilizing feedback in AI-mediated systems.
        """),
        code("""
        import numpy as np
        import pandas as pd

        def simulate_feedback(x0=1.0, gain=0.10, steps=30):
            x = x0
            rows = []

            for t in range(steps + 1):
                rows.append({"time": t, "state": x, "gain": gain})
                action = gain * x
                x = x + action

            return pd.DataFrame(rows)

        stabilizing = simulate_feedback(x0=1.0, gain=-0.05)
        destabilizing = simulate_feedback(x0=1.0, gain=0.08)

        stabilizing["loop_type"] = "stabilizing"
        destabilizing["loop_type"] = "destabilizing"

        pd.concat([stabilizing, destabilizing], ignore_index=True)
        """),
        md("""
        ## Interpretation

        Positive feedback can amplify deviation, while negative feedback can stabilize system behavior.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "03_concentration_common_dependency_and_platform_fragility_lab.ipynb",
    "Concentration, Common Dependency, and Platform Fragility Lab",
    [
        md("""
        ## Purpose

        This lab calculates concentration risk using dependency shares.
        """),
        code("""
        import pandas as pd

        providers = pd.DataFrame([
            {"provider": "ProviderA", "dependency_share": 0.48},
            {"provider": "ProviderB", "dependency_share": 0.22},
            {"provider": "ProviderC", "dependency_share": 0.14},
            {"provider": "ProviderD", "dependency_share": 0.10},
            {"provider": "Other", "dependency_share": 0.06},
        ])

        providers["squared_share"] = providers["dependency_share"] ** 2

        concentration_score = providers["squared_share"].sum()

        providers, concentration_score
        """),
        md("""
        ## Interpretation

        Provider concentration increases common-mode risk when many systems depend on the same upstream platform.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "04_systemic_ai_governance_incidents_and_runtime_resilience_lab.ipynb",
    "Systemic AI Governance, Incidents, and Runtime Resilience Lab",
    [
        md("""
        ## Purpose

        This lab frames systemic AI risk as governance evidence: dependencies, feedback loops, incidents, and controls.
        """),
        code("""
        import pandas as pd

        governance_review = pd.DataFrame([
            {
                "review_area": "dependency_mapping",
                "question": "Are upstream and downstream dependencies documented?",
                "status": "partial",
                "owner": "Architecture",
            },
            {
                "review_area": "feedback_loops",
                "question": "Are self-reinforcing AI feedback loops monitored?",
                "status": "missing",
                "owner": "ML Governance",
            },
            {
                "review_area": "cascade_scenarios",
                "question": "Have local-failure cascade scenarios been simulated?",
                "status": "partial",
                "owner": "Risk",
            },
            {
                "review_area": "fallback",
                "question": "Are fallback and rollback pathways tested?",
                "status": "partial",
                "owner": "Operations",
            },
            {
                "review_area": "incident_reporting",
                "question": "Are propagation incidents reported and reviewed?",
                "status": "complete",
                "owner": "Security / Governance",
            },
        ])

        governance_review.groupby("status").size().reset_index(name="count")
        """),
        md("""
        ## Interpretation

        Systemic AI governance requires evidence about dependency maps, feedback loops, cascade scenarios, fallback capacity, and incidents.
        """),
    ],
)
