"""
AI for Scientific Discovery and Computational Research

Python workflow:
- synthetic scientific candidate space
- surrogate modeling
- uncertainty proxy
- active learning candidate selection
- governance-ready discovery outputs
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ARTICLE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ARTICLE_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

RANDOM_SEED = 42
rng = np.random.default_rng(RANDOM_SEED)


def create_candidate_space(n: int = 1200) -> pd.DataFrame:
    """Create synthetic scientific candidates with hidden true properties."""
    x1 = rng.uniform(0, 1, n)
    x2 = rng.uniform(0, 1, n)
    x3 = rng.uniform(0, 1, n)
    x4 = rng.uniform(0, 1, n)

    true_property = (
        1.8 * np.sin(np.pi * x1)
        + 1.2 * np.cos(np.pi * x2)
        + 0.9 * x3 * x4
        - 0.4 * x2**2
        + rng.normal(0, 0.05, n)
    )

    synthesis_cost = 0.25 + 0.55 * x4 + 0.20 * rng.uniform(0, 1, n)
    safety_penalty = np.where(x2 > 0.85, 0.35, 0.00)

    return pd.DataFrame(
        {
            "candidate_id": [f"C{i:04d}" for i in range(n)],
            "feature_1": x1,
            "feature_2": x2,
            "feature_3": x3,
            "feature_4": x4,
            "true_property": true_property,
            "synthesis_cost": synthesis_cost,
            "safety_penalty": safety_penalty,
        }
    )


def design_matrix(df: pd.DataFrame) -> np.ndarray:
    """Create a polynomial design matrix for a simple surrogate model."""
    x1 = df["feature_1"].to_numpy()
    x2 = df["feature_2"].to_numpy()
    x3 = df["feature_3"].to_numpy()
    x4 = df["feature_4"].to_numpy()

    return np.column_stack(
        [
            np.ones(len(df)),
            x1,
            x2,
            x3,
            x4,
            x1**2,
            x2**2,
            x3**2,
            x4**2,
            x1 * x2,
            x3 * x4,
        ]
    )


def fit_ridge_surrogate(x: np.ndarray, y: np.ndarray, ridge: float = 0.01) -> np.ndarray:
    """Fit a ridge-regression surrogate using linear algebra."""
    identity = np.eye(x.shape[1])
    identity[0, 0] = 0.0
    return np.linalg.solve(x.T @ x + ridge * identity, x.T @ y)


def predict_surrogate(beta: np.ndarray, x: np.ndarray) -> np.ndarray:
    """Predict candidate properties from surrogate coefficients."""
    return x @ beta


def uncertainty_proxy(candidates: pd.DataFrame, observed: pd.DataFrame) -> np.ndarray:
    """Estimate uncertainty using distance to nearest observed candidate."""
    candidate_features = candidates[
        ["feature_1", "feature_2", "feature_3", "feature_4"]
    ].to_numpy()

    observed_features = observed[
        ["feature_1", "feature_2", "feature_3", "feature_4"]
    ].to_numpy()

    distances = []
    for row in candidate_features:
        d = np.sqrt(((observed_features - row) ** 2).sum(axis=1)).min()
        distances.append(d)

    distances = np.array(distances)
    return distances / max(distances.max(), 1e-8)


def run_active_learning_rounds(
    rounds: int = 5,
    initial_samples: int = 40,
    batch_size: int = 25,
) -> None:
    """Run active learning over a synthetic scientific candidate space."""
    candidates = create_candidate_space()

    observed_ids = set(
        rng.choice(candidates["candidate_id"], size=initial_samples, replace=False)
    )

    history = []

    for round_id in range(1, rounds + 1):
        observed = candidates[candidates["candidate_id"].isin(observed_ids)].copy()
        unobserved = candidates[~candidates["candidate_id"].isin(observed_ids)].copy()

        beta = fit_ridge_surrogate(
            design_matrix(observed),
            observed["true_property"].to_numpy(),
        )

        unobserved["predicted_property"] = predict_surrogate(
            beta,
            design_matrix(unobserved),
        )

        unobserved["uncertainty_proxy"] = uncertainty_proxy(unobserved, observed)

        unobserved["acquisition_score"] = (
            0.60 * unobserved["predicted_property"]
            + 0.30 * unobserved["uncertainty_proxy"]
            - 0.20 * unobserved["synthesis_cost"]
            - 0.40 * unobserved["safety_penalty"]
        )

        selected = unobserved.sort_values(
            "acquisition_score",
            ascending=False,
        ).head(batch_size)

        observed_ids.update(selected["candidate_id"])

        history.append(
            {
                "round": round_id,
                "observed_candidates": len(observed_ids),
                "best_observed_property": candidates[
                    candidates["candidate_id"].isin(observed_ids)
                ]["true_property"].max(),
                "mean_selected_true_property": selected["true_property"].mean(),
                "mean_selected_cost": selected["synthesis_cost"].mean(),
                "mean_selected_safety_penalty": selected["safety_penalty"].mean(),
            }
        )

        selected.to_csv(
            OUTPUT_DIR / f"python_selected_candidates_round_{round_id}.csv",
            index=False,
        )

    final_observed = candidates[candidates["candidate_id"].isin(observed_ids)].copy()
    history_df = pd.DataFrame(history)

    candidates.to_csv(OUTPUT_DIR / "python_candidate_space.csv", index=False)
    final_observed.to_csv(OUTPUT_DIR / "python_observed_candidates.csv", index=False)
    history_df.to_csv(OUTPUT_DIR / "python_active_learning_history.csv", index=False)

    memo = f"""# Scientific Discovery Active Learning Memo

Rounds completed: {rounds}
Initial samples: {initial_samples}
Batch size: {batch_size}
Total observed candidates: {len(final_observed)}
Best observed property: {final_observed["true_property"].max():.4f}

Interpretation:
- The surrogate model accelerates search through a large candidate space.
- The acquisition function balances predicted property, uncertainty, cost, and safety.
- Selected candidates still require simulation or experimental validation.
- The workflow should be versioned with data, code, seed, and model assumptions.
"""

    (OUTPUT_DIR / "python_active_learning_governance_memo.md").write_text(memo)

    print(history_df)
    print(memo)


if __name__ == "__main__":
    run_active_learning_rounds()
