"""
Explainable AI and Model Interpretability

Python workflow for:
- synthetic risk data generation
- black-box model training
- permutation importance
- local surrogate explanations
- counterfactual search
- explanation stability testing
- governance-ready output artifacts
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

try:
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import accuracy_score
    from sklearn.model_selection import train_test_split
except ImportError as exc:
    raise SystemExit(
        "This workflow requires scikit-learn. Install with: pip install scikit-learn pandas numpy"
    ) from exc


ARTICLE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ARTICLE_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

RANDOM_SEED = 42
rng = np.random.default_rng(RANDOM_SEED)


@dataclass
class ExplanationResult:
    case_index: int
    prediction_probability: float
    local_coefficients: pd.Series
    counterfactual: pd.Series
    counterfactual_probability: float
    explanation_stability: float


def make_synthetic_risk_data(n: int = 3000) -> pd.DataFrame:
    """Create synthetic data for an interpretable risk-prediction example."""
    asset_age = rng.normal(10, 3, n).clip(0)
    sensor_load = rng.normal(0.5, 0.15, n).clip(0, 1)
    maintenance_gap = rng.normal(90, 30, n).clip(0)
    weather_stress = rng.normal(0.4, 0.2, n).clip(0, 1)
    inspection_score = rng.normal(0.7, 0.15, n).clip(0, 1)

    logit = (
        -3.0
        + 0.10 * asset_age
        + 2.2 * sensor_load
        + 0.012 * maintenance_gap
        + 1.3 * weather_stress
        - 1.6 * inspection_score
        + rng.normal(0, 0.25, n)
    )

    probability = 1 / (1 + np.exp(-logit))
    outcome = rng.binomial(1, probability)

    return pd.DataFrame(
        {
            "asset_age": asset_age,
            "sensor_load": sensor_load,
            "maintenance_gap": maintenance_gap,
            "weather_stress": weather_stress,
            "inspection_score": inspection_score,
            "outcome": outcome,
        }
    )


def permutation_importance(
    model: RandomForestClassifier,
    x_valid: pd.DataFrame,
    y_valid: pd.Series,
) -> pd.Series:
    """Calculate dependency-light permutation importance."""
    baseline = accuracy_score(y_valid, model.predict(x_valid))
    scores = {}

    for column in x_valid.columns:
        x_permuted = x_valid.copy()
        x_permuted[column] = rng.permutation(x_permuted[column].to_numpy())
        permuted_score = accuracy_score(y_valid, model.predict(x_permuted))
        scores[column] = baseline - permuted_score

    return pd.Series(scores).sort_values(ascending=False)


def local_surrogate_explanation(
    model: RandomForestClassifier,
    x_train: pd.DataFrame,
    case: pd.Series,
    samples: int = 500,
    noise_scale: float = 0.10,
) -> pd.Series:
    """Fit a simple LIME-like local linear surrogate around one case."""
    feature_std = x_train.std().replace(0, 1)
    perturbations = []

    for _ in range(samples):
        noise = rng.normal(0, noise_scale, size=len(case)) * feature_std.to_numpy()
        perturbations.append(case.to_numpy() + noise)

    local_x = pd.DataFrame(perturbations, columns=x_train.columns)
    local_y = model.predict_proba(local_x)[:, 1]

    surrogate = LinearRegression()
    surrogate.fit(local_x, local_y)

    return pd.Series(surrogate.coef_, index=x_train.columns).sort_values(
        key=np.abs,
        ascending=False,
    )


def find_counterfactual(
    model: RandomForestClassifier,
    case: pd.Series,
    target_threshold: float = 0.50,
    max_steps: int = 60,
) -> tuple[pd.Series, float]:
    """Search for a simple counterfactual by changing actionable risk features."""
    candidate = case.copy()

    for _ in range(max_steps):
        probability = model.predict_proba(candidate.to_frame().T)[0, 1]

        if probability < target_threshold:
            return candidate, float(probability)

        candidate["maintenance_gap"] = max(candidate["maintenance_gap"] - 4, 0)
        candidate["sensor_load"] = max(candidate["sensor_load"] - 0.015, 0)
        candidate["weather_stress"] = max(candidate["weather_stress"] - 0.012, 0)

    probability = model.predict_proba(candidate.to_frame().T)[0, 1]
    return candidate, float(probability)


def explanation_stability(
    model: RandomForestClassifier,
    x_train: pd.DataFrame,
    case: pd.Series,
    repeats: int = 12,
) -> float:
    """Estimate stability of local surrogate explanations."""
    explanations = []

    for _ in range(repeats):
        coefficients = local_surrogate_explanation(model, x_train, case, samples=300)
        explanations.append(coefficients.reindex(x_train.columns).to_numpy())

    matrix = np.vstack(explanations)
    mean_vector = matrix.mean(axis=0)
    distances = np.linalg.norm(matrix - mean_vector, axis=1)

    return float(1 / (1 + distances.mean()))


def main() -> None:
    """Run the explainability workflow."""
    data = make_synthetic_risk_data()
    data.to_csv(OUTPUT_DIR / "synthetic_explainability_data.csv", index=False)

    x = data.drop(columns=["outcome"])
    y = data["outcome"]

    x_train, x_valid, y_train, y_valid = train_test_split(
        x,
        y,
        test_size=0.30,
        random_state=RANDOM_SEED,
        stratify=y,
    )

    model = RandomForestClassifier(
        n_estimators=250,
        max_depth=6,
        random_state=RANDOM_SEED,
    )
    model.fit(x_train, y_train)

    validation_accuracy = accuracy_score(y_valid, model.predict(x_valid))

    global_importance = permutation_importance(model, x_valid, y_valid)
    global_importance.to_csv(OUTPUT_DIR / "python_global_permutation_importance.csv")

    case_index = 10
    case = x_valid.iloc[case_index]
    probability = float(model.predict_proba(case.to_frame().T)[0, 1])

    local_coefficients = local_surrogate_explanation(model, x_train, case)
    counterfactual, cf_probability = find_counterfactual(model, case)
    stability = explanation_stability(model, x_train, case)

    local_coefficients.to_csv(OUTPUT_DIR / "python_local_surrogate_coefficients.csv")
    counterfactual.to_csv(OUTPUT_DIR / "python_counterfactual_case.csv")

    audit = pd.DataFrame(
        [
            {
                "case_index": case_index,
                "prediction_probability": probability,
                "counterfactual_probability": cf_probability,
                "explanation_stability": stability,
                "validation_accuracy": validation_accuracy,
                "method": "local_surrogate_plus_counterfactual",
            }
        ]
    )

    audit.to_csv(OUTPUT_DIR / "python_explanation_audit_summary.csv", index=False)

    memo = f"""# Explainability Audit Memo

Validation accuracy: {validation_accuracy:.4f}
Prediction probability for reviewed case: {probability:.4f}
Counterfactual probability: {cf_probability:.4f}
Explanation stability score: {stability:.4f}

Interpretation:
- Global permutation importance identifies broad model sensitivity.
- Local surrogate coefficients explain one prediction neighborhood.
- Counterfactual search identifies a plausible path to a different model output.
- Stability score should be monitored before explanations are used for governance.
"""
    (OUTPUT_DIR / "python_explanation_audit_memo.md").write_text(memo)

    print(memo)


if __name__ == "__main__":
    main()
