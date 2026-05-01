"""
Advanced AI Safety and System Reliability Lab

This module expands the article workflow with a more complete monitoring,
reliability, calibration, drift, incident-review, and governance evidence
pipeline for deployed AI systems.

The workflow uses synthetic data so it can run without external dependencies
beyond numpy, pandas, and matplotlib. Replace synthetic logs with production
inference logs when adapting this to a real system.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


ARTICLE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ARTICLE_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


@dataclass
class SafetyPolicy:
    """Operational thresholds for a deployed AI system."""

    decision_threshold: float = 0.70
    uncertainty_threshold: float = 0.30
    missed_failure_tolerance: float = 0.01
    drift_warning_threshold: float = 0.10
    drift_action_threshold: float = 0.25
    calibration_warning_threshold: float = 0.05
    calibration_action_threshold: float = 0.10


def sigmoid(z: np.ndarray) -> np.ndarray:
    """Numerically stable logistic transform for synthetic risk generation."""
    return 1 / (1 + np.exp(-z))


def simulate_inference_log(
    n: int,
    seed: int,
    shift: float = 0.0,
    adversarial_rate: float = 0.0,
    missingness_rate: float = 0.0,
) -> pd.DataFrame:
    """
    Simulate an AI decision-support inference log.

    Parameters
    ----------
    n:
        Number of inference records.
    seed:
        Random seed for reproducibility.
    shift:
        Simulated deployment distribution shift.
    adversarial_rate:
        Share of records with manipulated feature values.
    missingness_rate:
        Share of records with missing sensor values.

    Returns
    -------
    pd.DataFrame
        Synthetic inference log with features, predictions, uncertainty,
        outcomes, and subgroup labels.
    """
    rng = np.random.default_rng(seed)

    region = rng.choice(
        ["north", "south", "east", "west"],
        size=n,
        p=[0.25, 0.25, 0.25, 0.25],
    )

    asset_age = rng.normal(loc=10 + shift, scale=3.0, size=n).clip(0)
    sensor_load = rng.normal(loc=0.50 + 0.03 * shift, scale=0.15, size=n).clip(0, 1)
    maintenance_gap = rng.normal(loc=90 + 8 * shift, scale=30, size=n).clip(0)

    # Regional effect introduces subgroup structure.
    region_effect = pd.Series(region).map(
        {"north": 0.00, "south": 0.20, "east": -0.10, "west": 0.10}
    ).to_numpy()

    # Simulate adversarial or corrupted input records.
    adversarial_flag = rng.binomial(1, adversarial_rate, size=n).astype(bool)
    sensor_load[adversarial_flag] = np.clip(sensor_load[adversarial_flag] - 0.25, 0, 1)

    # Simulate missing sensor readings.
    missing_flag = rng.binomial(1, missingness_rate, size=n).astype(bool)
    sensor_load_with_missing = sensor_load.copy()
    sensor_load_with_missing[missing_flag] = np.nan

    # Operational pipeline imputes missing values to baseline mean.
    sensor_load_imputed = np.where(
        np.isnan(sensor_load_with_missing),
        np.nanmean(sensor_load_with_missing),
        sensor_load_with_missing,
    )

    latent_risk = (
        -3.2
        + 0.12 * asset_age
        + 2.5 * sensor_load
        + 0.014 * maintenance_gap
        + region_effect
        + rng.normal(0, 0.35, size=n)
    )

    true_probability = sigmoid(latent_risk)

    # Model score is imperfect because it sees imputed and possibly manipulated inputs.
    model_score = sigmoid(
        -3.0
        + 0.11 * asset_age
        + 2.25 * sensor_load_imputed
        + 0.013 * maintenance_gap
        + rng.normal(0, 0.25, size=n)
    )

    uncertainty = (
        0.08
        + 0.38 * np.exp(-((model_score - 0.50) ** 2) / 0.035)
        + 0.03 * abs(shift)
        + 0.08 * missing_flag
        + 0.06 * adversarial_flag
        + rng.normal(0, 0.02, size=n)
    ).clip(0, 1)

    observed_outcome = rng.binomial(1, true_probability)

    return pd.DataFrame(
        {
            "region": region,
            "asset_age": asset_age,
            "sensor_load": sensor_load_with_missing,
            "sensor_load_imputed": sensor_load_imputed,
            "maintenance_gap": maintenance_gap,
            "predicted_probability": model_score,
            "uncertainty": uncertainty,
            "observed_outcome": observed_outcome,
            "missing_sensor": missing_flag.astype(int),
            "adversarial_or_corrupted": adversarial_flag.astype(int),
        }
    )


def population_stability_index(
    expected: pd.Series,
    actual: pd.Series,
    bins: int = 10,
) -> float:
    """Calculate population stability index for distribution drift."""
    expected_clean = expected.dropna()
    actual_clean = actual.dropna()

    breakpoints = np.quantile(expected_clean, np.linspace(0, 1, bins + 1))
    breakpoints = np.unique(breakpoints)

    if len(breakpoints) < 3:
        return 0.0

    expected_counts, _ = np.histogram(expected_clean, bins=breakpoints)
    actual_counts, _ = np.histogram(actual_clean, bins=breakpoints)

    expected_share = expected_counts / max(expected_counts.sum(), 1)
    actual_share = actual_counts / max(actual_counts.sum(), 1)

    expected_share = np.where(expected_share == 0, 0.0001, expected_share)
    actual_share = np.where(actual_share == 0, 0.0001, actual_share)

    return float(np.sum((actual_share - expected_share) * np.log(actual_share / expected_share)))


def empirical_ks_statistic(expected: pd.Series, actual: pd.Series) -> float:
    """
    Calculate a simple empirical Kolmogorov-Smirnov style statistic
    without requiring scipy.
    """
    expected_values = np.sort(expected.dropna().to_numpy())
    actual_values = np.sort(actual.dropna().to_numpy())

    grid = np.sort(np.unique(np.concatenate([expected_values, actual_values])))

    expected_cdf = np.searchsorted(expected_values, grid, side="right") / len(expected_values)
    actual_cdf = np.searchsorted(actual_values, grid, side="right") / len(actual_values)

    return float(np.max(np.abs(expected_cdf - actual_cdf)))


def calibration_table(df: pd.DataFrame, bins: int = 10) -> pd.DataFrame:
    """Create a reliability calibration table."""
    temp = df.copy()
    temp["risk_band"] = pd.cut(
        temp["predicted_probability"],
        bins=np.linspace(0, 1, bins + 1),
        include_lowest=True,
    )

    table = temp.groupby("risk_band", observed=True).agg(
        count=("observed_outcome", "size"),
        predicted_mean=("predicted_probability", "mean"),
        observed_rate=("observed_outcome", "mean"),
    )

    table["absolute_gap"] = (table["predicted_mean"] - table["observed_rate"]).abs()
    table["weighted_gap"] = table["count"] / table["count"].sum() * table["absolute_gap"]

    return table.reset_index()


def expected_calibration_error(df: pd.DataFrame, bins: int = 10) -> float:
    """Calculate expected calibration error."""
    return float(calibration_table(df, bins=bins)["weighted_gap"].sum())


def brier_score(df: pd.DataFrame) -> float:
    """Calculate the Brier score for probabilistic predictions."""
    return float(
        np.mean((df["predicted_probability"] - df["observed_outcome"]) ** 2)
    )


def score_deployment(df: pd.DataFrame, policy: SafetyPolicy) -> pd.DataFrame:
    """Apply operational safety policy to deployment records."""
    scored = df.copy()

    scored["recommended_action"] = np.where(
        scored["predicted_probability"] >= policy.decision_threshold,
        "flag",
        "do_not_flag",
    )

    scored["review_required"] = scored["uncertainty"] > policy.uncertainty_threshold

    scored["missed_failure"] = (
        (scored["recommended_action"] == "do_not_flag")
        & (scored["observed_outcome"] == 1)
    )

    scored["automated_high_confidence"] = (
        (scored["review_required"] == False)
        & (scored["recommended_action"] == "flag")
    )

    return scored


def subgroup_safety_report(scored: pd.DataFrame) -> pd.DataFrame:
    """Calculate subgroup reliability and safety metrics."""
    report = scored.groupby("region").agg(
        records=("observed_outcome", "size"),
        event_rate=("observed_outcome", "mean"),
        mean_prediction=("predicted_probability", "mean"),
        mean_uncertainty=("uncertainty", "mean"),
        review_rate=("review_required", "mean"),
        missed_failure_rate=("missed_failure", "mean"),
        corrupted_share=("adversarial_or_corrupted", "mean"),
        missing_sensor_share=("missing_sensor", "mean"),
    )

    report["calibration_gap"] = report["mean_prediction"] - report["event_rate"]

    return report.reset_index()


def drift_report(
    baseline: pd.DataFrame,
    deployment: pd.DataFrame,
    features: Iterable[str],
    policy: SafetyPolicy,
) -> pd.DataFrame:
    """Create drift report for monitored features."""
    rows = []

    for feature in features:
        psi = population_stability_index(baseline[feature], deployment[feature])
        ks = empirical_ks_statistic(baseline[feature], deployment[feature])

        if psi >= policy.drift_action_threshold:
            status = "action"
        elif psi >= policy.drift_warning_threshold:
            status = "warning"
        else:
            status = "normal"

        rows.append(
            {
                "feature": feature,
                "baseline_mean": baseline[feature].mean(),
                "deployment_mean": deployment[feature].mean(),
                "baseline_sd": baseline[feature].std(),
                "deployment_sd": deployment[feature].std(),
                "population_stability_index": psi,
                "empirical_ks_statistic": ks,
                "drift_status": status,
            }
        )

    return pd.DataFrame(rows)


def threshold_sweep(
    deployment: pd.DataFrame,
    uncertainty_threshold: float = 0.30,
) -> pd.DataFrame:
    """
    Evaluate safety tradeoffs across possible decision thresholds.

    This helps governance teams understand the relationship among
    automation, review burden, false negatives, and missed failures.
    """
    rows = []

    for threshold in np.linspace(0.10, 0.90, 17):
        policy = SafetyPolicy(
            decision_threshold=float(threshold),
            uncertainty_threshold=uncertainty_threshold,
        )
        scored = score_deployment(deployment, policy)

        flagged = scored["recommended_action"] == "flag"
        missed_failure = scored["missed_failure"]
        review_required = scored["review_required"]

        rows.append(
            {
                "decision_threshold": float(threshold),
                "flag_rate": float(flagged.mean()),
                "review_rate": float(review_required.mean()),
                "missed_failure_rate": float(missed_failure.mean()),
                "observed_event_rate": float(scored["observed_outcome"].mean()),
                "mean_uncertainty": float(scored["uncertainty"].mean()),
            }
        )

    return pd.DataFrame(rows)


def reliability_survival_table(
    incident_times: np.ndarray,
    evaluation_horizon: int = 180,
) -> pd.DataFrame:
    """
    Estimate a simple survival-style reliability table.

    incident_times contains the simulated day on which each system instance
    experiences a safety incident. Values greater than the horizon are treated
    as not failed within the horizon.
    """
    days = np.arange(1, evaluation_horizon + 1)

    rows = []
    for day in days:
        reliability = np.mean(incident_times > day)
        cumulative_failure_probability = 1 - reliability
        rows.append(
            {
                "day": int(day),
                "reliability": float(reliability),
                "cumulative_failure_probability": float(cumulative_failure_probability),
            }
        )

    return pd.DataFrame(rows)


def simulate_incident_times(seed: int, n_systems: int = 1000) -> np.ndarray:
    """Simulate time-to-incident for reliability analysis."""
    rng = np.random.default_rng(seed)

    base_times = rng.weibull(a=1.8, size=n_systems) * 120
    rare_early_failures = rng.binomial(1, 0.05, size=n_systems).astype(bool)
    base_times[rare_early_failures] = rng.uniform(1, 20, rare_early_failures.sum())

    return base_times


def plot_threshold_sweep(sweep: pd.DataFrame, output_path: Path) -> None:
    """Plot safety tradeoffs across thresholds."""
    plt.figure(figsize=(8, 5))
    plt.plot(sweep["decision_threshold"], sweep["missed_failure_rate"], marker="o", label="Missed failure rate")
    plt.plot(sweep["decision_threshold"], sweep["review_rate"], marker="s", label="Review rate")
    plt.plot(sweep["decision_threshold"], sweep["flag_rate"], marker="^", label="Flag rate")
    plt.xlabel("Decision threshold")
    plt.ylabel("Rate")
    plt.title("AI safety threshold tradeoff review")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=160)
    plt.close()


def plot_reliability_curve(survival: pd.DataFrame, output_path: Path) -> None:
    """Plot reliability over time."""
    plt.figure(figsize=(8, 5))
    plt.plot(survival["day"], survival["reliability"])
    plt.xlabel("Day")
    plt.ylabel("Estimated reliability")
    plt.title("System reliability over time")
    plt.tight_layout()
    plt.savefig(output_path, dpi=160)
    plt.close()


def write_governance_memo(
    dashboard: pd.DataFrame,
    drift: pd.DataFrame,
    subgroup: pd.DataFrame,
    output_path: Path,
) -> None:
    """Create a governance-readable safety memo."""
    action_drift = drift.loc[drift["drift_status"] == "action", "feature"].tolist()
    warning_drift = drift.loc[drift["drift_status"] == "warning", "feature"].tolist()

    max_subgroup_missed = subgroup["missed_failure_rate"].max()
    worst_region = subgroup.sort_values("missed_failure_rate", ascending=False).iloc[0]["region"]

    memo = f"""# AI Safety and Reliability Governance Memo

## Executive Summary

This memo summarizes advanced monitoring results for the deployed AI system.

## Dashboard

- Missed failure rate: {dashboard.loc[0, "missed_failure_rate"]:.4f}
- Expected calibration error: {dashboard.loc[0, "expected_calibration_error"]:.4f}
- Brier score: {dashboard.loc[0, "brier_score"]:.4f}
- Human review rate: {dashboard.loc[0, "review_rate"]:.4f}
- Safety threshold violated: {dashboard.loc[0, "safety_threshold_violated"]}

## Drift Review

Features requiring action: {action_drift}
Features requiring warning review: {warning_drift}

## Subgroup Review

Highest subgroup missed-failure rate: {max_subgroup_missed:.4f}
Worst affected region in this simulation: {worst_region}

## Recommended Governance Actions

1. Review all features marked warning or action in the drift report.
2. Inspect high-uncertainty missed failures.
3. Reassess the decision threshold and uncertainty threshold.
4. Confirm whether affected subgroups require additional monitoring or remediation.
5. Document whether deployment should continue, be constrained, or be rolled back.
"""

    output_path.write_text(memo)


def main() -> None:
    """Run the advanced AI safety and reliability workflow."""
    policy = SafetyPolicy()

    baseline = simulate_inference_log(
        n=5000,
        seed=101,
        shift=0.0,
        adversarial_rate=0.00,
        missingness_rate=0.02,
    )

    deployment = simulate_inference_log(
        n=5000,
        seed=202,
        shift=2.0,
        adversarial_rate=0.04,
        missingness_rate=0.08,
    )

    scored = score_deployment(deployment, policy)

    monitored_features = [
        "asset_age",
        "sensor_load_imputed",
        "maintenance_gap",
        "predicted_probability",
        "uncertainty",
    ]

    drift = drift_report(baseline, scored, monitored_features, policy)
    calibration = calibration_table(scored)
    subgroup = subgroup_safety_report(scored)
    sweep = threshold_sweep(scored, uncertainty_threshold=policy.uncertainty_threshold)

    incident_times = simulate_incident_times(seed=303)
    survival = reliability_survival_table(incident_times, evaluation_horizon=180)

    dashboard = pd.DataFrame(
        [
            {
                "missed_failure_rate": float(scored["missed_failure"].mean()),
                "expected_calibration_error": expected_calibration_error(scored),
                "brier_score": brier_score(scored),
                "review_rate": float(scored["review_required"].mean()),
                "corrupted_share": float(scored["adversarial_or_corrupted"].mean()),
                "missing_sensor_share": float(scored["missing_sensor"].mean()),
                "safety_threshold_violated": bool(
                    scored["missed_failure"].mean() > policy.missed_failure_tolerance
                ),
            }
        ]
    )

    incident_review = scored.loc[scored["missed_failure"]].sort_values(
        by=["uncertainty", "predicted_probability"],
        ascending=[False, True],
    )

    baseline.to_csv(OUTPUT_DIR / "advanced_baseline_log.csv", index=False)
    scored.to_csv(OUTPUT_DIR / "advanced_deployment_scored.csv", index=False)
    dashboard.to_csv(OUTPUT_DIR / "advanced_safety_dashboard.csv", index=False)
    drift.to_csv(OUTPUT_DIR / "advanced_drift_report.csv", index=False)
    calibration.to_csv(OUTPUT_DIR / "advanced_calibration_table.csv", index=False)
    subgroup.to_csv(OUTPUT_DIR / "advanced_subgroup_safety_report.csv", index=False)
    sweep.to_csv(OUTPUT_DIR / "advanced_threshold_sweep.csv", index=False)
    survival.to_csv(OUTPUT_DIR / "advanced_reliability_survival_table.csv", index=False)
    incident_review.head(250).to_csv(OUTPUT_DIR / "advanced_incident_review.csv", index=False)

    plot_threshold_sweep(sweep, OUTPUT_DIR / "advanced_threshold_sweep.png")
    plot_reliability_curve(survival, OUTPUT_DIR / "advanced_reliability_curve.png")

    write_governance_memo(
        dashboard=dashboard,
        drift=drift,
        subgroup=subgroup,
        output_path=OUTPUT_DIR / "advanced_governance_memo.md",
    )

    print("Advanced AI safety and reliability workflow complete.")
    print(dashboard.T)


if __name__ == "__main__":
    main()
