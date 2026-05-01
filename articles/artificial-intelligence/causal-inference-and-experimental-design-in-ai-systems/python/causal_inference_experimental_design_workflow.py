"""
Causal Inference and Experimental Design in AI Systems Mini-Workflow

This script demonstrates:
- potential outcomes
- randomized treatment assignment
- observational confounding
- naive treatment-effect estimates
- stratified adjustment

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


def build_synthetic_causal_data(n: int = 5000) -> pd.DataFrame:
    """Create synthetic potential-outcomes data for causal inference examples."""
    users = pd.DataFrame(
        {
            "user_id": [f"user_{i:05d}" for i in range(1, n + 1)],
            "prior_activity": rng.normal(0, 1, size=n),
            "domain_expertise": rng.normal(0, 1, size=n),
        }
    )

    users["true_tau"] = (
        0.08
        + 0.04 * (users["prior_activity"] > 0)
        + 0.03 * (users["domain_expertise"] > 0)
    )

    users["y0"] = (
        0.30
        + 0.08 * users["prior_activity"]
        + 0.04 * users["domain_expertise"]
        + rng.normal(0, 0.05, size=n)
    )

    users["y1"] = users["y0"] + users["true_tau"]

    users["randomized_treatment"] = rng.binomial(1, 0.5, size=n)

    users["randomized_outcome"] = np.where(
        users["randomized_treatment"] == 1,
        users["y1"],
        users["y0"],
    )

    propensity = 1 / (1 + np.exp(-(-0.2 + 1.2 * users["prior_activity"])))
    users["propensity"] = propensity
    users["observed_treatment"] = rng.binomial(1, propensity)

    users["observed_outcome"] = np.where(
        users["observed_treatment"] == 1,
        users["y1"],
        users["y0"],
    )

    return users


def estimate_effects(users: pd.DataFrame) -> pd.DataFrame:
    """Estimate true, randomized, naive observational, and adjusted effects."""
    true_ate = users["true_tau"].mean()

    randomized_estimate = (
        users.loc[users["randomized_treatment"] == 1, "randomized_outcome"].mean()
        - users.loc[users["randomized_treatment"] == 0, "randomized_outcome"].mean()
    )

    naive_observational_estimate = (
        users.loc[users["observed_treatment"] == 1, "observed_outcome"].mean()
        - users.loc[users["observed_treatment"] == 0, "observed_outcome"].mean()
    )

    users = users.copy()
    users["activity_bin"] = pd.qcut(
        users["prior_activity"],
        q=5,
        labels=False,
        duplicates="drop",
    )

    stratum_effects = []

    for _, group in users.groupby("activity_bin"):
        treated = group[group["observed_treatment"] == 1]
        control = group[group["observed_treatment"] == 0]

        if len(treated) > 0 and len(control) > 0:
            effect = treated["observed_outcome"].mean() - control["observed_outcome"].mean()
            weight = len(group) / len(users)
            stratum_effects.append(weight * effect)

    stratified_adjusted_estimate = sum(stratum_effects)

    ipw_weights = (
        users["observed_treatment"] / users["propensity"]
        + (1 - users["observed_treatment"]) / (1 - users["propensity"])
    )

    treated_weighted_mean = np.average(
        users.loc[users["observed_treatment"] == 1, "observed_outcome"],
        weights=ipw_weights[users["observed_treatment"] == 1],
    )

    control_weighted_mean = np.average(
        users.loc[users["observed_treatment"] == 0, "observed_outcome"],
        weights=ipw_weights[users["observed_treatment"] == 0],
    )

    ipw_estimate = treated_weighted_mean - control_weighted_mean

    return pd.DataFrame(
        [
            {"estimate": "true_ate", "value": true_ate},
            {"estimate": "randomized_estimate", "value": randomized_estimate},
            {"estimate": "naive_observational_estimate", "value": naive_observational_estimate},
            {"estimate": "stratified_adjusted_estimate", "value": stratified_adjusted_estimate},
            {"estimate": "ipw_estimate", "value": ipw_estimate},
        ]
    )


def build_balance_table(users: pd.DataFrame) -> pd.DataFrame:
    """Summarize covariate balance by observational treatment group."""
    return (
        users
        .groupby("observed_treatment")
        .agg(
            users=("user_id", "count"),
            mean_prior_activity=("prior_activity", "mean"),
            mean_domain_expertise=("domain_expertise", "mean"),
            mean_propensity=("propensity", "mean"),
        )
        .reset_index()
    )


def main() -> None:
    users = build_synthetic_causal_data()
    estimates = estimate_effects(users)
    balance = build_balance_table(users)

    users.to_csv(OUTPUT_DIR / "causal_inference_synthetic_data.csv", index=False)
    estimates.to_csv(OUTPUT_DIR / "causal_inference_effect_estimates.csv", index=False)
    balance.to_csv(OUTPUT_DIR / "causal_inference_balance_table.csv", index=False)

    print(estimates)
    print(balance)


if __name__ == "__main__":
    main()
