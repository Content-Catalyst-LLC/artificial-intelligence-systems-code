"""
The Future of Artificial Intelligence Systems Mini-Workflow

This script demonstrates:
- simplified scaling-law simulation
- compute/capability tradeoff modeling
- AI system-fitness scoring
- governance-capacity comparison
- future scenario ranking

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


def build_system_options() -> pd.DataFrame:
    """Create synthetic future AI system options."""
    systems = pd.DataFrame(
        {
            "system": [
                "centralized_frontier",
                "compute_optimal_specialist",
                "distributed_edge_network",
                "hybrid_governed_platform",
                "undergoverned_agentic_stack",
            ],
            "scale_index": [0.95, 0.72, 0.58, 0.78, 0.88],
            "capability": [0.95, 0.83, 0.74, 0.88, 0.91],
            "efficiency": [0.42, 0.86, 0.78, 0.74, 0.45],
            "governance_capacity": [0.62, 0.78, 0.70, 0.90, 0.38],
            "trust": [0.58, 0.80, 0.72, 0.86, 0.42],
            "systemic_risk": [0.72, 0.38, 0.44, 0.32, 0.86],
            "cost": [0.90, 0.48, 0.55, 0.62, 0.76],
        }
    )

    systems["responsible_scaling_gap"] = (
        systems["capability"] - systems["governance_capacity"]
    )

    systems["system_fitness"] = (
        0.30 * systems["capability"]
        + 0.18 * systems["efficiency"]
        + 0.22 * systems["governance_capacity"]
        + 0.18 * systems["trust"]
        - 0.20 * systems["systemic_risk"]
        - 0.12 * systems["cost"]
    )

    systems["governance_warning"] = systems["responsible_scaling_gap"] > 0.15

    return systems


def build_scaling_curve(n_points: int = 100) -> pd.DataFrame:
    """Create a simplified scaling-law curve."""
    scale = np.linspace(1, 100, n_points)
    loss_floor = 1.2
    x0 = 35
    alpha = 0.32

    return pd.DataFrame(
        {
            "scale": scale,
            "loss": loss_floor + (x0 / scale) ** alpha,
        }
    )


def build_future_scenarios() -> pd.DataFrame:
    """Create synthetic AI futures scenarios."""
    scenarios = pd.DataFrame(
        {
            "scenario": [
                "centralized_frontier_dominance",
                "distributed_intelligence_networks",
                "hybrid_public_private_infrastructure",
                "regulated_high_risk_ai",
                "governance_lag_and_systemic_fragility",
            ],
            "capability": [0.95, 0.74, 0.86, 0.80, 0.88],
            "infrastructure": [0.88, 0.70, 0.82, 0.75, 0.66],
            "governance": [0.55, 0.68, 0.84, 0.90, 0.35],
            "resilience": [0.52, 0.78, 0.80, 0.74, 0.40],
            "legitimacy": [0.50, 0.72, 0.82, 0.86, 0.34],
            "systemic_risk": [0.78, 0.46, 0.38, 0.42, 0.90],
        }
    )

    scenarios["scenario_score"] = (
        0.22 * scenarios["capability"]
        + 0.18 * scenarios["infrastructure"]
        + 0.22 * scenarios["governance"]
        + 0.18 * scenarios["resilience"]
        + 0.15 * scenarios["legitimacy"]
        - 0.20 * scenarios["systemic_risk"]
    )

    scenarios["governance_gap"] = scenarios["capability"] - scenarios["governance"]

    scenarios["risk_warning"] = (
        (scenarios["governance_gap"] > 0.20)
        | (scenarios["systemic_risk"] > 0.70)
    )

    return scenarios


def summarize_constraints(scenarios: pd.DataFrame) -> pd.DataFrame:
    """Summarize scenario-level AI futures constraints."""
    return pd.DataFrame(
        [
            {"metric": "mean_capability", "value": scenarios["capability"].mean()},
            {"metric": "mean_governance", "value": scenarios["governance"].mean()},
            {"metric": "mean_resilience", "value": scenarios["resilience"].mean()},
            {"metric": "mean_systemic_risk", "value": scenarios["systemic_risk"].mean()},
            {"metric": "share_with_risk_warning", "value": scenarios["risk_warning"].mean()},
        ]
    )


def main() -> None:
    systems = build_system_options()
    scaling_curve = build_scaling_curve()
    scenarios = build_future_scenarios()
    constraint_summary = summarize_constraints(scenarios)

    systems_ranked = systems.sort_values("system_fitness", ascending=False)
    scenarios_ranked = scenarios.sort_values("scenario_score", ascending=False)

    systems.to_csv(OUTPUT_DIR / "future_ai_system_options.csv", index=False)
    systems_ranked.to_csv(OUTPUT_DIR / "future_ai_system_options_ranked.csv", index=False)
    scaling_curve.to_csv(OUTPUT_DIR / "future_ai_scaling_curve.csv", index=False)
    scenarios.to_csv(OUTPUT_DIR / "future_ai_scenarios.csv", index=False)
    scenarios_ranked.to_csv(OUTPUT_DIR / "future_ai_scenarios_ranked.csv", index=False)
    constraint_summary.to_csv(OUTPUT_DIR / "future_ai_constraint_summary.csv", index=False)

    print(systems_ranked)
    print(scenarios_ranked)
    print(constraint_summary)


if __name__ == "__main__":
    main()
