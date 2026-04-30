"""
Reinforcement Learning in Dynamic Environments Mini-Workflow

This script demonstrates:
- a simple grid environment
- Q-learning
- epsilon-greedy exploration
- dynamic reward shift
- policy extraction

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

GRID_SIZE = 5
N_STATES = GRID_SIZE * GRID_SIZE
N_ACTIONS = 4

ACTIONS = {
    0: "up",
    1: "down",
    2: "left",
    3: "right",
}

GOAL_STATE = 24
HAZARD_STATE = 12


def state_to_position(state: int) -> tuple[int, int]:
    """Convert integer state to grid row and column."""
    return divmod(state, GRID_SIZE)


def position_to_state(row: int, col: int) -> int:
    """Convert grid row and column to integer state."""
    return row * GRID_SIZE + col


def step_environment(state: int, action: int, episode: int) -> tuple[int, float, bool]:
    """
    Environment transition.

    The goal reward changes after episode 400 to simulate a dynamic environment.
    """
    row, col = state_to_position(state)

    if action == 0:
        row = max(0, row - 1)
    elif action == 1:
        row = min(GRID_SIZE - 1, row + 1)
    elif action == 2:
        col = max(0, col - 1)
    elif action == 3:
        col = min(GRID_SIZE - 1, col + 1)

    next_state = position_to_state(row, col)

    goal_reward = 10.0 if episode < 400 else 6.0

    if next_state == GOAL_STATE:
        return next_state, goal_reward, True

    if next_state == HAZARD_STATE:
        return next_state, -8.0, False

    return next_state, -0.1, False


def run_q_learning(
    episodes: int = 800,
    max_steps: int = 80,
    alpha: float = 0.15,
    gamma: float = 0.95,
    epsilon: float = 0.20,
) -> tuple[pd.DataFrame, pd.DataFrame, np.ndarray]:
    """Run Q-learning in a small dynamic grid environment."""
    q_table = np.zeros((N_STATES, N_ACTIONS))
    episode_rows: list[dict[str, float | int | bool | str]] = []

    for episode in range(episodes):
        state = 0
        total_reward = 0.0
        done = False
        steps = 0
        hazard_visits = 0

        for _ in range(max_steps):
            if rng.random() < epsilon:
                action = int(rng.integers(N_ACTIONS))
            else:
                action = int(np.argmax(q_table[state]))

            next_state, reward, done = step_environment(state, action, episode)

            if next_state == HAZARD_STATE:
                hazard_visits += 1

            td_target = reward + gamma * np.max(q_table[next_state])
            td_error = td_target - q_table[state, action]
            q_table[state, action] += alpha * td_error

            total_reward += reward
            state = next_state
            steps += 1

            if done:
                break

        episode_rows.append(
            {
                "episode": episode,
                "total_reward": total_reward,
                "steps": steps,
                "reached_goal": done,
                "hazard_visits": hazard_visits,
                "phase": "early_reward" if episode < 400 else "shifted_reward",
            }
        )

    results = pd.DataFrame(episode_rows)

    policy = pd.DataFrame(
        {
            "state": range(N_STATES),
            "best_action": [
                ACTIONS[int(np.argmax(q_table[state]))]
                for state in range(N_STATES)
            ],
            "best_value": [
                float(np.max(q_table[state]))
                for state in range(N_STATES)
            ],
        }
    )

    return results, policy, q_table


def summarize_results(results: pd.DataFrame) -> pd.DataFrame:
    """Summarize episode-level RL diagnostics."""
    return (
        results
        .groupby("phase")
        .agg(
            episodes=("episode", "count"),
            mean_reward=("total_reward", "mean"),
            mean_steps=("steps", "mean"),
            goal_rate=("reached_goal", "mean"),
            mean_hazard_visits=("hazard_visits", "mean"),
        )
        .reset_index()
    )


def main() -> None:
    results, policy, _ = run_q_learning()
    summary = summarize_results(results)

    results.to_csv(OUTPUT_DIR / "rl_dynamic_environment_episode_results.csv", index=False)
    policy.to_csv(OUTPUT_DIR / "rl_dynamic_environment_policy.csv", index=False)
    summary.to_csv(OUTPUT_DIR / "rl_dynamic_environment_summary.csv", index=False)

    print(summary)
    print(policy.head(10))


if __name__ == "__main__":
    main()
