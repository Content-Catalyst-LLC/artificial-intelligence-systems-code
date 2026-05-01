"""
Artificial Intelligence in Environmental Monitoring

Python workflow:
- synthetic environmental monitoring data
- sensor and satellite-style feature fusion
- environmental stress probability
- anomaly scoring
- human review routing
- governance summary generation
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


def create_environmental_monitoring_data(n_zones: int = 150) -> pd.DataFrame:
    """Create synthetic environmental monitoring data by monitoring zone."""
    zones = pd.DataFrame(
        {
            "zone_id": [f"Z{i:03d}" for i in range(n_zones)],
            "region_type": rng.choice(
                ["urban", "industrial", "agricultural", "forest", "coastal"],
                size=n_zones,
                p=[0.28, 0.16, 0.24, 0.20, 0.12],
            ),
            "pm25": rng.normal(14, 6, n_zones).clip(1),
            "ozone": rng.normal(52, 14, n_zones).clip(5),
            "water_turbidity": rng.normal(8, 4, n_zones).clip(0),
            "water_temperature": rng.normal(18, 5, n_zones).clip(0),
            "vegetation_index": rng.normal(0.55, 0.18, n_zones).clip(0, 1),
            "surface_temperature": rng.normal(24, 7, n_zones),
            "precipitation_anomaly": rng.normal(0, 1, n_zones),
            "sensor_health": rng.uniform(0.65, 1.00, n_zones),
            "population_exposure": rng.integers(100, 25000, n_zones),
            "environmental_justice_priority": rng.choice([0, 1], size=n_zones, p=[0.72, 0.28]),
        }
    )

    zones["industrial_or_urban"] = zones["region_type"].isin(["urban", "industrial"]).astype(int)
    zones["data_quality_risk"] = 1 - zones["sensor_health"]

    return zones


def estimate_environmental_stress(data: pd.DataFrame) -> pd.DataFrame:
    """Estimate environmental stress risk using transparent synthetic scoring."""
    scored = data.copy()

    scored["air_pollution_index"] = (
        0.55 * (scored["pm25"] / scored["pm25"].max())
        + 0.45 * (scored["ozone"] / scored["ozone"].max())
    )

    scored["water_stress_index"] = (
        0.60 * (scored["water_turbidity"] / scored["water_turbidity"].max())
        + 0.40 * (scored["water_temperature"] / scored["water_temperature"].max())
    )

    scored["vegetation_stress_index"] = 1 - scored["vegetation_index"]

    scored["climate_anomaly_index"] = (
        0.50
        * np.abs(scored["precipitation_anomaly"])
        / np.abs(scored["precipitation_anomaly"]).max()
        + 0.50
        * (scored["surface_temperature"] - scored["surface_temperature"].min())
        / (scored["surface_temperature"].max() - scored["surface_temperature"].min())
    )

    logit = (
        -2.8
        + 2.0 * scored["air_pollution_index"]
        + 1.6 * scored["water_stress_index"]
        + 1.4 * scored["vegetation_stress_index"]
        + 1.2 * scored["climate_anomaly_index"]
        + 0.6 * scored["industrial_or_urban"]
        + 0.8 * scored["data_quality_risk"]
    )

    scored["environmental_stress_probability"] = 1 / (1 + np.exp(-logit))

    scored["anomaly_score"] = (
        np.abs(scored["pm25"] - scored["pm25"].mean()) / scored["pm25"].std()
        + np.abs(scored["water_turbidity"] - scored["water_turbidity"].mean())
        / scored["water_turbidity"].std()
        + np.abs(scored["surface_temperature"] - scored["surface_temperature"].mean())
        / scored["surface_temperature"].std()
    ) / 3

    scored["human_review_required"] = (
        (scored["environmental_stress_probability"] > 0.60)
        | (scored["anomaly_score"] > 1.25)
        | (scored["data_quality_risk"] > 0.25)
        | (scored["environmental_justice_priority"] == 1)
    )

    scored["priority_score"] = (
        0.35 * scored["environmental_stress_probability"]
        + 0.20 * scored["anomaly_score"].clip(0, 2) / 2
        + 0.15 * scored["data_quality_risk"]
        + 0.15 * (scored["population_exposure"] / scored["population_exposure"].max())
        + 0.15 * scored["environmental_justice_priority"]
    )

    return scored.sort_values("priority_score", ascending=False)


def create_governance_summary(scored: pd.DataFrame) -> pd.DataFrame:
    """Create environmental monitoring governance summary."""
    return pd.DataFrame(
        [
            {
                "zones_reviewed": len(scored),
                "mean_stress_probability": scored["environmental_stress_probability"].mean(),
                "high_stress_zones": int((scored["environmental_stress_probability"] > 0.60).sum()),
                "human_review_required": int(scored["human_review_required"].sum()),
                "environmental_justice_priority_zones": int(scored["environmental_justice_priority"].sum()),
                "mean_data_quality_risk": scored["data_quality_risk"].mean(),
            }
        ]
    )


def main() -> None:
    """Run the environmental monitoring workflow."""
    data = create_environmental_monitoring_data()
    scored = estimate_environmental_stress(data)
    summary = create_governance_summary(scored)

    data.to_csv(OUTPUT_DIR / "python_environmental_monitoring_input.csv", index=False)
    scored.to_csv(OUTPUT_DIR / "python_environmental_stress_priority_table.csv", index=False)
    summary.to_csv(OUTPUT_DIR / "python_environmental_monitoring_governance_summary.csv", index=False)

    memo = f"""# Environmental Monitoring Governance Memo

Zones reviewed: {int(summary.loc[0, "zones_reviewed"])}
High-stress zones: {int(summary.loc[0, "high_stress_zones"])}
Human review required: {int(summary.loc[0, "human_review_required"])}
Environmental justice priority zones: {int(summary.loc[0, "environmental_justice_priority_zones"])}
Mean data quality risk: {summary.loc[0, "mean_data_quality_risk"]:.4f}

Recommended actions:
1. Review high-priority zones before automated escalation.
2. Inspect zones with high data-quality risk.
3. Validate anomaly alerts against sensor status and weather context.
4. Compare environmental justice priority zones against monitoring coverage.
5. Document uncertainty and human review decisions.
"""
    (OUTPUT_DIR / "python_environmental_governance_memo.md").write_text(memo)

    print(scored.head(10))
    print(summary.T)
    print(memo)


if __name__ == "__main__":
    main()
