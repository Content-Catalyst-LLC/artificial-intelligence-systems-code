"""
Human-AI Interaction and Interface Design Mini-Workflow

This script demonstrates:
- synthetic model outputs
- interface clarity and explanation quality
- simulated user decisions
- overreliance and underreliance diagnostics
- grouped interaction summaries

It is educational and uses synthetic data.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


OUTPUT_DIR = Path("../outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

RANDOM_SEED = 42


def build_interaction_data(n: int = 1800) -> pd.DataFrame:
    """Create synthetic human-AI interaction data."""
    rng = np.random.default_rng(RANDOM_SEED)

    data = pd.DataFrame(
        {
            "case_id": [f"HIAI-{i:04d}" for i in range(1, n + 1)],
            "model_confidence": rng.beta(5, 2, size=n),
            "explanation_quality": rng.beta(4, 3, size=n),
            "uncertainty_clarity": rng.beta(3.5, 3, size=n),
            "time_pressure": rng.choice(
                ["low", "medium", "high"],
                size=n,
                p=[0.35, 0.40, 0.25],
            ),
            "user_expertise": rng.choice(
                ["novice", "intermediate", "expert"],
                size=n,
                p=[0.30, 0.45, 0.25],
            ),
            "risk_level": rng.choice(
                ["low", "medium", "high"],
                size=n,
                p=[0.45, 0.35, 0.20],
            ),
        }
    )

    data["model_correct"] = rng.binomial(
        1,
        p=np.clip(0.20 + 0.75 * data["model_confidence"], 0, 1),
        size=n,
    )

    return data


def simulate_user_behavior(data: pd.DataFrame) -> pd.DataFrame:
    """Simulate user acceptance, escalation, and reliance diagnostics."""
    rng = np.random.default_rng(RANDOM_SEED)
    frame = data.copy()

    expertise_adjustment = frame["user_expertise"].map(
        {"novice": 0.10, "intermediate": 0.03, "expert": -0.04}
    )

    pressure_adjustment = frame["time_pressure"].map(
        {"low": -0.04, "medium": 0.03, "high": 0.12}
    )

    risk_adjustment = frame["risk_level"].map(
        {"low": 0.06, "medium": 0.00, "high": -0.10}
    )

    reliance_probability = (
        0.10
        + 0.48 * frame["model_confidence"]
        + 0.16 * frame["explanation_quality"]
        + 0.12 * frame["uncertainty_clarity"]
        + expertise_adjustment
        + pressure_adjustment
        + risk_adjustment
    )

    frame["user_accepted_ai"] = rng.binomial(
        1,
        p=np.clip(reliance_probability, 0.02, 0.98),
        size=len(frame),
    )

    escalation_probability = (
        0.05
        + 0.20 * (frame["risk_level"] == "high").astype(int)
        + 0.15 * (frame["uncertainty_clarity"] < 0.40).astype(int)
        + 0.10 * (frame["explanation_quality"] < 0.40).astype(int)
    )

    frame["user_escalated"] = rng.binomial(
        1,
        p=np.clip(escalation_probability, 0.01, 0.80),
        size=len(frame),
    )

    frame["overreliance"] = (
        (frame["user_accepted_ai"] == 1) & (frame["model_correct"] == 0)
    ).astype(int)

    frame["underreliance"] = (
        (frame["user_accepted_ai"] == 0) & (frame["model_correct"] == 1)
    ).astype(int)

    frame["reliance_gap"] = np.abs(
        frame["user_accepted_ai"] - frame["model_correct"]
    )

    return frame


def summarize_interactions(frame: pd.DataFrame) -> pd.DataFrame:
    """Summarize interaction diagnostics."""
    return (
        frame
        .groupby(["user_expertise", "risk_level", "time_pressure"])
        .agg(
            cases=("case_id", "count"),
            accuracy=("model_correct", "mean"),
            acceptance_rate=("user_accepted_ai", "mean"),
            escalation_rate=("user_escalated", "mean"),
            overreliance_rate=("overreliance", "mean"),
            underreliance_rate=("underreliance", "mean"),
            mean_reliance_gap=("reliance_gap", "mean"),
            mean_explanation_quality=("explanation_quality", "mean"),
            mean_uncertainty_clarity=("uncertainty_clarity", "mean"),
        )
        .reset_index()
    )


def main() -> None:
    data = build_interaction_data()
    scored = simulate_user_behavior(data)
    summary = summarize_interactions(scored)

    scored.to_csv(OUTPUT_DIR / "human_ai_interaction_synthetic_dataset.csv", index=False)
    summary.to_csv(OUTPUT_DIR / "human_ai_interaction_diagnostics.csv", index=False)

    print(summary.sort_values("mean_reliance_gap", ascending=False).head(10))
    print(scored.head())


if __name__ == "__main__":
    main()
