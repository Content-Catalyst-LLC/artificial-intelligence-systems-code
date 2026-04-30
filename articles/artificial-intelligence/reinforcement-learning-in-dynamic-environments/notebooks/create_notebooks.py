#!/usr/bin/env python3
"""
Create advanced Jupyter notebooks for:
Reinforcement Learning in Dynamic Environments
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


gridworld_setup = """
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

grid_size = 5
n_states = grid_size * grid_size
n_actions = 4

actions = {0: "up", 1: "down", 2: "left", 3: "right"}

goal_state = 24
hazard_state = 12

def state_to_position(state):
    return divmod(state, grid_size)

def position_to_state(row, col):
    return row * grid_size + col

def step_environment(state, action, episode):
    row, col = state_to_position(state)

    if action == 0:
        row = max(0, row - 1)
    elif action == 1:
        row = min(grid_size - 1, row + 1)
    elif action == 2:
        col = max(0, col - 1)
    elif action == 3:
        col = min(grid_size - 1, col + 1)

    next_state = position_to_state(row, col)
    goal_reward = 10.0 if episode < 400 else 6.0

    if next_state == goal_state:
        return next_state, goal_reward, True
    if next_state == hazard_state:
        return next_state, -8.0, False
    return next_state, -0.1, False
"""

write(
    NOTEBOOK_DIR / "01_q_learning_gridworld_dynamic_environment_lab.ipynb",
    "Q-Learning Gridworld Dynamic Environment Lab",
    [
        md("""
        ## Purpose

        This lab introduces Q-learning in a small dynamic grid environment.
        """),
        code(gridworld_setup),
        code("""
alpha = 0.15
gamma = 0.95
epsilon = 0.20
episodes = 800
max_steps = 80

Q = np.zeros((n_states, n_actions))
rows = []

for episode in range(episodes):
    state = 0
    total_reward = 0.0
    done = False

    for step_index in range(max_steps):
        if rng.random() < epsilon:
            action = int(rng.integers(n_actions))
        else:
            action = int(np.argmax(Q[state]))

        next_state, reward, done = step_environment(state, action, episode)

        td_target = reward + gamma * np.max(Q[next_state])
        td_error = td_target - Q[state, action]
        Q[state, action] += alpha * td_error

        total_reward += reward
        state = next_state

        if done:
            break

    rows.append({
        "episode": episode,
        "total_reward": total_reward,
        "reached_goal": done,
        "phase": "early_reward" if episode < 400 else "shifted_reward",
    })

results = pd.DataFrame(rows)
results.groupby("phase").agg(
    mean_reward=("total_reward", "mean"),
    goal_rate=("reached_goal", "mean"),
)
        """),
        md("""
        ## Interpretation

        The reward shift tests whether the learned policy remains effective when the environment changes.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "02_exploration_exploitation_and_policy_evaluation_lab.ipynb",
    "Exploration, Exploitation, and Policy Evaluation Lab",
    [
        md("""
        ## Purpose

        This lab compares exploration schedules and policy outcomes.
        """),
        code("""
import numpy as np
import pandas as pd

episodes = 600

schedules = pd.DataFrame({
    "episode": np.arange(1, episodes + 1)
})

schedules["constant_epsilon"] = 0.20
schedules["decaying_epsilon"] = np.maximum(0.05, 0.35 * np.exp(-schedules["episode"] / 180))
schedules["low_epsilon"] = 0.05

# Synthetic reward curves to illustrate evaluation concepts.
rng = np.random.default_rng(42)

for schedule in ["constant_epsilon", "decaying_epsilon", "low_epsilon"]:
    schedules[f"reward_{schedule}"] = (
        5.0
        + 5.0 * (1 - schedules[schedule])
        + rng.normal(0, 0.6, size=episodes)
    )

summary = pd.DataFrame({
    "schedule": ["constant_epsilon", "decaying_epsilon", "low_epsilon"],
    "mean_reward": [
        schedules["reward_constant_epsilon"].mean(),
        schedules["reward_decaying_epsilon"].mean(),
        schedules["reward_low_epsilon"].mean(),
    ],
    "mean_exploration_rate": [
        schedules["constant_epsilon"].mean(),
        schedules["decaying_epsilon"].mean(),
        schedules["low_epsilon"].mean(),
    ],
})

summary
        """),
        md("""
        ## Interpretation

        Exploration policies should be evaluated not only by reward, but also by safety, adaptation, and learning value.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "03_nonstationary_rewards_partial_observability_and_adaptation_lab.ipynb",
    "Nonstationary Rewards, Partial Observability, and Adaptation Lab",
    [
        md("""
        ## Purpose

        This lab simulates non-stationary reward conditions and partial observability.
        """),
        code("""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
episodes = 700

data = pd.DataFrame({
    "episode": np.arange(episodes),
})

data["environment_phase"] = np.where(data["episode"] < 350, "stable", "shifted")
data["observation_noise"] = np.where(data["environment_phase"] == "stable", 0.10, 0.25)
data["reward_signal"] = np.where(data["environment_phase"] == "stable", 8.0, 5.8)
data["observed_reward"] = data["reward_signal"] + rng.normal(0, data["observation_noise"], size=episodes)
data["adaptation_alert"] = data["observed_reward"].rolling(30, min_periods=5).mean() < 6.4

data.groupby("environment_phase").agg(
    mean_observed_reward=("observed_reward", "mean"),
    mean_observation_noise=("observation_noise", "mean"),
    alert_rate=("adaptation_alert", "mean"),
).reset_index()
        """),
        md("""
        ## Interpretation

        Non-stationary environments require monitoring signals that detect when policy assumptions may no longer hold.
        """),
    ],
)

write(
    NOTEBOOK_DIR / "04_safe_rl_constraints_governance_and_monitoring_lab.ipynb",
    "Safe RL Constraints, Governance, and Monitoring Lab",
    [
        md("""
        ## Purpose

        This lab frames RL deployment as a governance problem with rewards, constraints, fallback, and monitoring.
        """),
        code("""
import pandas as pd

rl_governance = pd.DataFrame([
    {
        "area": "reward_function",
        "question": "Does the reward function match the intended system objective?",
        "status": "partial",
        "owner": "ML + Domain Team",
    },
    {
        "area": "exploration_safety",
        "question": "Is exploration constrained in high-risk states?",
        "status": "missing",
        "owner": "Safety Review",
    },
    {
        "area": "constraint_monitoring",
        "question": "Are constraint violations logged and reviewed?",
        "status": "partial",
        "owner": "MLOps",
    },
    {
        "area": "fallback_policy",
        "question": "Is there a safe fallback policy?",
        "status": "partial",
        "owner": "Operations",
    },
    {
        "area": "human_override",
        "question": "Can humans pause or override the RL system?",
        "status": "complete",
        "owner": "Product / Governance",
    },
])

rl_governance.groupby("status").size().reset_index(name="count")
        """),
        md("""
        ## Interpretation

        RL governance requires explicit review of reward specification, exploration risk, constraints, fallback policy, and human override.
        """),
    ],
)
