"""
Model Monitoring, Drift, and AI Observability

Python workflow:
- Simulate production monitoring batches.
- Compute feature drift, prediction drift, performance, latency, and incident signals.
- Score AI observability risk.
- Produce governance-ready summaries.
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


def population_stability_index(reference: np.ndarray, current: np.ndarray, bins: int = 10) -> float:
    """Compute a simple population stability index for one numeric feature."""
    quantiles = np.linspace(0, 1, bins + 1)
    edges = np.quantile(reference, quantiles)
    edges = np.unique(edges)

    if len(edges) < 3:
        return 0.0

    reference_counts, _ = np.histogram(reference, bins=edges)
    current_counts, _ = np.histogram(current, bins=edges)

    reference_prop = np.maximum(reference_counts / max(reference_counts.sum(), 1), 1e-6)
    current_prop = np.maximum(current_counts / max(current_counts.sum(), 1), 1e-6)

    return float(np.sum((reference_prop - current_prop) * np.log(reference_prop / current_prop)))


def simulate_reference_data(n: int = 5000) -> pd.DataFrame:
    """Create synthetic reference data."""
    feature_a = rng.normal(loc=0.0, scale=1.0, size=n)
    feature_b = rng.gamma(shape=2.0, scale=1.0, size=n)
    feature_c = rng.normal(loc=3.0, scale=0.8, size=n)

    logit = 0.7 * feature_a - 0.4 * feature_b + 0.5 * feature_c - 1.2
    probability = 1 / (1 + np.exp(-logit))
    label = rng.binomial(1, probability)

    return pd.DataFrame(
        {
            "feature_a": feature_a,
            "feature_b": feature_b,
            "feature_c": feature_c,
            "prediction_score": probability,
            "label": label,
        }
    )


def simulate_production_batches(reference: pd.DataFrame, batches: int = 24, batch_size: int = 600) -> pd.DataFrame:
    """Create synthetic production monitoring records for multiple batches."""
    rows = []

    for batch in range(1, batches + 1):
        drift_pressure = max(0, batch - 8) / batches

        feature_a = rng.normal(loc=0.0 + 0.9 * drift_pressure, scale=1.0, size=batch_size)
        feature_b = rng.gamma(shape=2.0 + 1.2 * drift_pressure, scale=1.0, size=batch_size)
        feature_c = rng.normal(loc=3.0 - 0.6 * drift_pressure, scale=0.8, size=batch_size)

        logit = 0.7 * feature_a - 0.4 * feature_b + 0.5 * feature_c - 1.2
        probability = 1 / (1 + np.exp(-logit))

        concept_shift = 0.45 if batch >= 14 else 0.0
        true_probability = 1 / (1 + np.exp(-(logit - concept_shift * feature_a + 0.35 * concept_shift)))
        label = rng.binomial(1, true_probability)

        predicted_label = (probability >= 0.5).astype(int)
        accuracy = float((predicted_label == label).mean())
        positive_rate = float(predicted_label.mean())
        mean_prediction = float(probability.mean())
        latency_ms = float(rng.gamma(shape=2.5, scale=120.0) + 12 * batch)
        missing_rate = float(np.clip(rng.normal(loc=0.01 + 0.02 * drift_pressure, scale=0.01), 0, 0.2))
        incident_count = int(rng.poisson(lam=0.2 + 1.8 * max(0, drift_pressure - 0.3)))

        psi_a = population_stability_index(reference["feature_a"].to_numpy(), feature_a)
        psi_b = population_stability_index(reference["feature_b"].to_numpy(), feature_b)
        psi_c = population_stability_index(reference["feature_c"].to_numpy(), feature_c)
        prediction_psi = population_stability_index(reference["prediction_score"].to_numpy(), probability)

        rows.append(
            {
                "batch": batch,
                "psi_feature_a": psi_a,
                "psi_feature_b": psi_b,
                "psi_feature_c": psi_c,
                "prediction_psi": prediction_psi,
                "max_feature_psi": max(psi_a, psi_b, psi_c),
                "accuracy": accuracy,
                "positive_rate": positive_rate,
                "mean_prediction": mean_prediction,
                "latency_ms": latency_ms,
                "missing_rate": missing_rate,
                "incident_count": incident_count,
                "label_available": int(batch >= 4),
            }
        )

    return pd.DataFrame(rows)


def score_observability_risk(records: pd.DataFrame) -> pd.DataFrame:
    """Score production batches for monitoring and governance risk."""
    scored = records.copy()

    scored["performance_degradation"] = np.clip(0.88 - scored["accuracy"], 0, 1)
    scored["drift_signal"] = np.clip(
        0.45 * scored["max_feature_psi"]
        + 0.35 * scored["prediction_psi"]
        + 0.20 * scored["missing_rate"] * 5,
        0,
        1.5,
    )
    scored["operational_signal"] = np.clip(
        (scored["latency_ms"] / 1200)
        + (scored["incident_count"] / 8),
        0,
        1.5,
    )

    scored["observability_risk"] = (
        0.35 * scored["drift_signal"]
        + 0.30 * scored["performance_degradation"]
        + 0.20 * scored["operational_signal"]
        + 0.15 * np.clip(scored["missing_rate"] * 5, 0, 1)
    )

    scored["alert_level"] = np.select(
        [
            scored["observability_risk"] > 0.60,
            scored["observability_risk"] > 0.40,
            scored["observability_risk"] > 0.25,
        ],
        [
            "incident_review",
            "action_required",
            "warning",
        ],
        default="normal",
    )

    scored["review_required"] = (
        (scored["alert_level"].isin(["action_required", "incident_review"]))
        | (scored["max_feature_psi"] > 0.25)
        | (scored["prediction_psi"] > 0.25)
        | (scored["accuracy"] < 0.78)
        | (scored["incident_count"] >= 2)
    )

    scored["recommended_action"] = np.select(
        [
            scored["alert_level"].eq("incident_review"),
            scored["max_feature_psi"] > 0.35,
            scored["accuracy"] < 0.78,
            scored["prediction_psi"] > 0.25,
            scored["incident_count"] >= 2,
        ],
        [
            "pause_or_rollback_and_open_incident",
            "investigate_data_pipeline_and_feature_drift",
            "review_performance_and_retraining_candidate",
            "review_thresholds_and_prediction_distribution",
            "open_operational_incident_review",
        ],
        default="continue_monitoring",
    )

    return scored


def main() -> None:
    """Run model monitoring, drift, and observability review."""
    reference = simulate_reference_data()
    production = simulate_production_batches(reference)
    scored = score_observability_risk(production)

    governance_summary = pd.DataFrame(
        [
            {
                "batches_reviewed": len(scored),
                "review_required": int(scored["review_required"].sum()),
                "incident_review_batches": int(scored["alert_level"].eq("incident_review").sum()),
                "max_feature_psi_observed": scored["max_feature_psi"].max(),
                "max_prediction_psi_observed": scored["prediction_psi"].max(),
                "minimum_accuracy_observed": scored["accuracy"].min(),
                "mean_latency_ms": scored["latency_ms"].mean(),
                "total_incidents": int(scored["incident_count"].sum()),
                "mean_observability_risk": scored["observability_risk"].mean(),
            }
        ]
    )

    reference.to_csv(OUTPUT_DIR / "python_reference_data.csv", index=False)
    production.to_csv(OUTPUT_DIR / "python_production_monitoring_records.csv", index=False)
    scored.to_csv(OUTPUT_DIR / "python_observability_risk_scores.csv", index=False)
    governance_summary.to_csv(OUTPUT_DIR / "python_observability_governance_summary.csv", index=False)

    memo = f"""# Model Monitoring, Drift, and AI Observability Memo

Batches reviewed: {int(governance_summary.loc[0, "batches_reviewed"])}
Review required: {int(governance_summary.loc[0, "review_required"])}
Incident-review batches: {int(governance_summary.loc[0, "incident_review_batches"])}
Maximum feature PSI observed: {governance_summary.loc[0, "max_feature_psi_observed"]:.4f}
Maximum prediction PSI observed: {governance_summary.loc[0, "max_prediction_psi_observed"]:.4f}
Minimum accuracy observed: {governance_summary.loc[0, "minimum_accuracy_observed"]:.4f}
Mean latency ms: {governance_summary.loc[0, "mean_latency_ms"]:.2f}
Total incidents: {int(governance_summary.loc[0, "total_incidents"])}
Mean observability risk: {governance_summary.loc[0, "mean_observability_risk"]:.4f}

Interpretation:
- Drift should be interpreted alongside performance, latency, incidents, and missingness.
- Production monitoring should distinguish warning signals from incident-level signals.
- Retraining should be governed, not automatic.
- Rollback readiness and incident response are part of model observability.
"""

    (OUTPUT_DIR / "python_observability_governance_memo.md").write_text(memo)

    print(governance_summary.T)
    print(scored)
    print(memo)


if __name__ == "__main__":
    main()
