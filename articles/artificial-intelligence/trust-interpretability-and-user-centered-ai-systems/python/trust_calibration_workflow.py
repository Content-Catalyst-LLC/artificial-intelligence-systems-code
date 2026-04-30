"""
Trust, Interpretability, and User-Centered AI Mini-Workflow

This script demonstrates:
- model confidence and correctness
- explanation quality
- simulated user reliance
- reliance gap diagnostics
- grouped trust calibration summaries

It is educational and uses synthetic data.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


OUTPUT_DIR = Path("../outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

RANDOM_SEED = 42


def build_user_ai_dataset(n: int = 1500) -> pd.DataFrame:
    """Create synthetic user-AI interaction records."""
    rng = np.random.default_rng(RANDOM_SEED)

    data = pd.DataFrame(
        {
            "case_id": [f"C-{i:04d}" for i in range(1, n + 1)],
            "model_confidence": rng.beta(5, 2, size=n),
            "explanation_quality": rng.beta(4, 3, size=n),
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

    expertise_adjustment = data["user_expertise"].map(
        {
            "novice": 0.12,
            "intermediate": 0.04,
            "expert": -0.04,
        }
    )

    risk_adjustment = data["risk_level"].map(
        {
            "low": 0.08,
            "medium": 0.00,
            "high": -0.10,
        }
    )

    reliance_probability = (
        0.15
        + 0.50 * data["model_confidence"]
        + 0.20 * data["explanation_quality"]
        + expertise_adjustment
        + risk_adjustment
    )

    data["user_relied_on_ai"] = rng.binomial(
        1,
        p=np.clip(reliance_probability, 0.02, 0.98),
        size=n,
    )

    return data


def add_diagnostics(data: pd.DataFrame) -> pd.DataFrame:
    """Add overreliance, underreliance, and reliance gap diagnostics."""
    scored = data.copy()

    scored["warranted_reliance"] = scored["model_correct"]

    scored["overreliance"] = (
        (scored["user_relied_on_ai"] == 1)
        & (scored["model_correct"] == 0)
    ).astype(int)

    scored["underreliance"] = (
        (scored["user_relied_on_ai"] == 0)
        & (scored["model_correct"] == 1)
    ).astype(int)

    scored["reliance_gap"] = np.abs(
        scored["user_relied_on_ai"] - scored["warranted_reliance"]
    )

    return scored


def summarize_reliance(scored: pd.DataFrame) -> pd.DataFrame:
    """Summarize trust calibration by expertise and risk level."""
    return (
        scored
        .groupby(["user_expertise", "risk_level"])
        .agg(
            cases=("case_id", "count"),
            mean_model_confidence=("model_confidence", "mean"),
            mean_explanation_quality=("explanation_quality", "mean"),
            model_accuracy=("model_correct", "mean"),
            user_reliance_rate=("user_relied_on_ai", "mean"),
            overreliance_rate=("overreliance", "mean"),
            underreliance_rate=("underreliance", "mean"),
            mean_reliance_gap=("reliance_gap", "mean"),
        )
        .reset_index()
    )


def main() -> None:
    data = build_user_ai_dataset()
    scored = add_diagnostics(data)
    summary = summarize_reliance(scored)

    scored.to_csv(OUTPUT_DIR / "user_ai_interaction_synthetic_dataset.csv", index=False)
    summary.to_csv(OUTPUT_DIR / "trust_calibration_summary.csv", index=False)

    print(summary.sort_values("mean_reliance_gap", ascending=False))
    print(scored.head())


if __name__ == "__main__":
    main()
