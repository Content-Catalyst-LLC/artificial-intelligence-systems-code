"""
AI History Paradigm Shares

This educational example creates synthetic paradigm-share curves for AI history.
It is not a bibliometric measurement. It is a reproducible conceptual model
showing how symbolic AI, statistical learning, deep learning, and systems-scale
AI can overlap over time.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


OUTPUT_DIR = Path("../outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def logistic(year: np.ndarray, midpoint: float, steepness: float) -> np.ndarray:
    """Return a logistic transition curve."""
    return 1.0 / (1.0 + np.exp(-steepness * (year - midpoint)))


def main() -> None:
    years = np.arange(1950, 2027)

    symbolic_score = 1.4 * (1.0 - logistic(years, midpoint=1990, steepness=0.08))
    statistical_score = logistic(years, midpoint=1995, steepness=0.08) * (
        1.0 - 0.35 * logistic(years, midpoint=2015, steepness=0.15)
    )
    deep_learning_score = logistic(years, midpoint=2012, steepness=0.20)
    systems_scale_score = logistic(years, midpoint=2020, steepness=0.35)

    scores = np.vstack(
        [
            symbolic_score,
            statistical_score,
            deep_learning_score,
            systems_scale_score,
        ]
    ).T

    shares = scores / scores.sum(axis=1, keepdims=True)

    timeline = pd.DataFrame(
        {
            "year": years,
            "symbolic_ai": shares[:, 0],
            "statistical_learning": shares[:, 1],
            "deep_learning": shares[:, 2],
            "systems_scale_ai": shares[:, 3],
        }
    )

    events = pd.DataFrame(
        [
            {
                "year": 1950,
                "event": "Turing's machine intelligence framing",
                "paradigm": "computation",
            },
            {
                "year": 1956,
                "event": "Dartmouth workshop and naming of AI",
                "paradigm": "symbolic_ai",
            },
            {
                "year": 1980,
                "event": "Expert systems expansion",
                "paradigm": "symbolic_ai",
            },
            {
                "year": 1990,
                "event": "Statistical learning becomes increasingly central",
                "paradigm": "statistical_learning",
            },
            {
                "year": 2012,
                "event": "Deep learning breakthrough era accelerates",
                "paradigm": "deep_learning",
            },
            {
                "year": 2017,
                "event": "Transformer architecture reshapes sequence modeling",
                "paradigm": "deep_learning",
            },
            {
                "year": 2022,
                "event": "Generative AI enters broad public use",
                "paradigm": "systems_scale_ai",
            },
        ]
    )

    timeline.to_csv(OUTPUT_DIR / "ai_history_paradigm_shares.csv", index=False)
    events.to_csv(OUTPUT_DIR / "ai_history_events.csv", index=False)

    print(timeline.tail())
    print(events)


if __name__ == "__main__":
    main()
