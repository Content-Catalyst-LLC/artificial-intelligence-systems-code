"""
Probabilistic Machine Learning and Bayesian AI Systems

Python workflow:
- asset-level binary risk simulation
- Beta-Bernoulli Bayesian updating
- posterior mean risk and credible interval approximation
- calibration review
- expected-loss decision support
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


def simulate_assets(n_assets: int = 200) -> pd.DataFrame:
    """Create synthetic asset observations with latent binary risk."""
    asset_ids = [f"ASSET-{i:03d}" for i in range(n_assets)]

    age_index = rng.uniform(0.0, 1.0, n_assets)
    exposure_index = rng.uniform(0.0, 1.0, n_assets)
    maintenance_quality = rng.uniform(0.0, 1.0, n_assets)

    latent_logit = (
        -3.0
        + 1.7 * age_index
        + 1.4 * exposure_index
        - 1.2 * maintenance_quality
        + rng.normal(0, 0.35, n_assets)
    )

    true_risk = 1 / (1 + np.exp(-latent_logit))
    inspection_count = rng.integers(5, 60, n_assets)
    observed_events = rng.binomial(inspection_count, true_risk)

    return pd.DataFrame(
        {
            "asset_id": asset_ids,
            "age_index": age_index,
            "exposure_index": exposure_index,
            "maintenance_quality": maintenance_quality,
            "inspection_count": inspection_count,
            "observed_events": observed_events,
            "true_risk": true_risk,
        }
    )


def beta_posterior_update(records: pd.DataFrame, alpha_prior: float = 2.0, beta_prior: float = 18.0) -> pd.DataFrame:
    """Update a Beta prior with binomial observations."""
    updated = records.copy()

    updated["alpha_prior"] = alpha_prior
    updated["beta_prior"] = beta_prior

    updated["alpha_posterior"] = updated["alpha_prior"] + updated["observed_events"]
    updated["beta_posterior"] = (
        updated["beta_prior"]
        + updated["inspection_count"]
        - updated["observed_events"]
    )

    updated["posterior_mean_risk"] = (
        updated["alpha_posterior"]
        / (updated["alpha_posterior"] + updated["beta_posterior"])
    )

    updated["posterior_variance"] = (
        updated["alpha_posterior"]
        * updated["beta_posterior"]
        / (
            (updated["alpha_posterior"] + updated["beta_posterior"]) ** 2
            * (updated["alpha_posterior"] + updated["beta_posterior"] + 1)
        )
    )

    updated["posterior_sd"] = np.sqrt(updated["posterior_variance"])

    updated["risk_ci_lower"] = np.clip(
        updated["posterior_mean_risk"] - 1.96 * updated["posterior_sd"],
        0,
        1,
    )

    updated["risk_ci_upper"] = np.clip(
        updated["posterior_mean_risk"] + 1.96 * updated["posterior_sd"],
        0,
        1,
    )

    updated["uncertainty_width"] = updated["risk_ci_upper"] - updated["risk_ci_lower"]

    updated["review_required"] = (
        (updated["posterior_mean_risk"] > 0.20)
        | (updated["uncertainty_width"] > 0.25)
        | (
            (updated["posterior_mean_risk"] > 0.12)
            & (updated["inspection_count"] < 15)
        )
    )

    return updated.sort_values(
        ["review_required", "posterior_mean_risk", "uncertainty_width"],
        ascending=[False, False, False],
    )


def calibration_review(updated: pd.DataFrame, n_bins: int = 6) -> pd.DataFrame:
    """Evaluate calibration of posterior mean risk against observed rates."""
    calibration = updated.copy()

    calibration["observed_rate"] = (
        calibration["observed_events"] / calibration["inspection_count"]
    )

    calibration["risk_bin"] = pd.cut(
        calibration["posterior_mean_risk"],
        bins=np.linspace(0, 1, n_bins + 1),
        include_lowest=True,
    )

    summary = (
        calibration.groupby("risk_bin", observed=False)
        .agg(
            assets=("asset_id", "count"),
            mean_predicted_risk=("posterior_mean_risk", "mean"),
            mean_observed_rate=("observed_rate", "mean"),
            mean_uncertainty_width=("uncertainty_width", "mean"),
            review_rate=("review_required", "mean"),
        )
        .reset_index()
    )

    summary["absolute_calibration_error"] = (
        summary["mean_predicted_risk"] - summary["mean_observed_rate"]
    ).abs()

    return summary


def expected_loss_priority(updated: pd.DataFrame) -> pd.DataFrame:
    """Create a decision-support ranking using expected loss."""
    ranked = updated.copy()

    cost_false_negative = 100.0
    cost_inspection = 8.0

    ranked["expected_loss_no_inspection"] = (
        ranked["posterior_mean_risk"] * cost_false_negative
    )

    ranked["expected_loss_inspection"] = cost_inspection

    ranked["expected_loss_reduction"] = (
        ranked["expected_loss_no_inspection"]
        - ranked["expected_loss_inspection"]
    )

    ranked["decision_recommendation"] = np.where(
        ranked["expected_loss_reduction"] > 0,
        "prioritize_inspection",
        "routine_monitoring",
    )

    return ranked.sort_values("expected_loss_reduction", ascending=False)


def main() -> None:
    """Run Bayesian risk updating and calibration review."""
    assets = simulate_assets()
    updated = beta_posterior_update(assets)
    calibration = calibration_review(updated)
    decisions = expected_loss_priority(updated)

    governance_summary = pd.DataFrame(
        [
            {
                "assets_reviewed": len(updated),
                "review_required": int(updated["review_required"].sum()),
                "mean_posterior_risk": updated["posterior_mean_risk"].mean(),
                "mean_uncertainty_width": updated["uncertainty_width"].mean(),
                "mean_calibration_error": calibration["absolute_calibration_error"].mean(),
                "inspection_priority_count": int(
                    decisions["decision_recommendation"].eq("prioritize_inspection").sum()
                ),
            }
        ]
    )

    assets.to_csv(OUTPUT_DIR / "python_asset_observations.csv", index=False)
    updated.to_csv(OUTPUT_DIR / "python_bayesian_risk_updates.csv", index=False)
    calibration.to_csv(OUTPUT_DIR / "python_calibration_review.csv", index=False)
    decisions.to_csv(OUTPUT_DIR / "python_expected_loss_priority.csv", index=False)
    governance_summary.to_csv(OUTPUT_DIR / "python_bayesian_governance_summary.csv", index=False)

    memo = f"""# Bayesian AI Systems Governance Memo

Assets reviewed: {int(governance_summary.loc[0, "assets_reviewed"])}
Review required: {int(governance_summary.loc[0, "review_required"])}
Mean posterior risk: {governance_summary.loc[0, "mean_posterior_risk"]:.4f}
Mean uncertainty width: {governance_summary.loc[0, "mean_uncertainty_width"]:.4f}
Mean calibration error: {governance_summary.loc[0, "mean_calibration_error"]:.4f}
Inspection priority count: {int(governance_summary.loc[0, "inspection_priority_count"])}

Interpretation:
- Bayesian risk estimates should include uncertainty intervals, not only point estimates.
- High uncertainty can justify review even when estimated risk is moderate.
- Calibration should be monitored because probabilities support decisions.
- Expected-loss rules make decision thresholds explicit and reviewable.
"""

    (OUTPUT_DIR / "python_bayesian_governance_memo.md").write_text(memo)

    print(governance_summary.T)
    print(calibration)
    print(decisions.head(10))
    print(memo)


if __name__ == "__main__":
    main()
