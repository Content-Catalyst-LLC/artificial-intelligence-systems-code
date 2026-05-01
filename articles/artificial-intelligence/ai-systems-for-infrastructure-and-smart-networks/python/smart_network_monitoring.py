"""
AI Systems for Infrastructure and Smart Networks

Python workflow:
- synthetic infrastructure network generation
- sensor telemetry simulation
- network centrality scoring
- failure-risk estimation
- review routing
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


def create_synthetic_network(n_nodes: int = 80) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Create synthetic infrastructure nodes and edges."""
    nodes = pd.DataFrame(
        {
            "node_id": [f"N{i:03d}" for i in range(n_nodes)],
            "asset_type": rng.choice(
                ["pump", "valve", "substation", "junction", "sensor_hub"],
                size=n_nodes,
            ),
            "asset_age": rng.normal(22, 9, n_nodes).clip(1),
            "demand": rng.normal(100, 25, n_nodes).clip(10),
            "service_population": rng.integers(250, 6000, n_nodes),
            "sensor_health": rng.uniform(0.60, 1.00, n_nodes),
            "historical_failures": rng.poisson(1.3, n_nodes),
            "equity_priority": rng.choice([0, 1], size=n_nodes, p=[0.75, 0.25]),
            "climate_exposure": rng.uniform(0.00, 1.00, n_nodes),
        }
    )

    edges = []

    for i in range(n_nodes - 1):
        edges.append((f"N{i:03d}", f"N{i + 1:03d}", rng.uniform(0.5, 3.0)))

    for _ in range(n_nodes):
        a, b = rng.choice(n_nodes, size=2, replace=False)
        edges.append((f"N{a:03d}", f"N{b:03d}", rng.uniform(0.5, 3.0)))

    edge_df = pd.DataFrame(edges, columns=["source", "target", "capacity"]).drop_duplicates(
        subset=["source", "target"]
    )

    return nodes, edge_df


def degree_centrality(nodes: pd.DataFrame, edges: pd.DataFrame) -> pd.Series:
    """Calculate degree centrality without external graph libraries."""
    counts = pd.concat([edges["source"], edges["target"]]).value_counts()
    centrality = nodes["node_id"].map(counts).fillna(0)
    return centrality / max(float(centrality.max()), 1.0)


def simulate_telemetry(nodes: pd.DataFrame) -> pd.DataFrame:
    """Simulate smart infrastructure telemetry."""
    telemetry = nodes.copy()

    telemetry["pressure_drop"] = (
        rng.normal(0.10, 0.04, len(nodes))
        + 0.004 * telemetry["asset_age"]
        + 0.025 * telemetry["historical_failures"]
        + 0.04 * telemetry["climate_exposure"]
    ).clip(0, 1)

    telemetry["vibration_index"] = (
        rng.normal(0.20, 0.08, len(nodes))
        + 0.003 * telemetry["asset_age"]
        + 0.04 * telemetry["historical_failures"]
    ).clip(0, 1)

    telemetry["data_quality_risk"] = 1 - telemetry["sensor_health"]

    return telemetry


def estimate_failure_risk(nodes: pd.DataFrame, edges: pd.DataFrame) -> pd.DataFrame:
    """Estimate failure risk and maintenance priority for network assets."""
    scored = simulate_telemetry(nodes)
    scored["network_centrality"] = degree_centrality(scored, edges)

    logit = (
        -3.6
        + 0.045 * scored["asset_age"]
        + 1.9 * scored["pressure_drop"]
        + 1.4 * scored["vibration_index"]
        + 0.24 * scored["historical_failures"]
        + 1.1 * scored["network_centrality"]
        + 0.7 * scored["data_quality_risk"]
        + 0.6 * scored["climate_exposure"]
    )

    scored["failure_probability"] = 1 / (1 + np.exp(-logit))

    scored["criticality_score"] = (
        0.32 * scored["failure_probability"]
        + 0.22 * scored["network_centrality"]
        + 0.16 * (scored["service_population"] / scored["service_population"].max())
        + 0.10 * scored["data_quality_risk"]
        + 0.10 * scored["equity_priority"]
        + 0.10 * scored["climate_exposure"]
    )

    scored["review_required"] = (
        (scored["failure_probability"] > 0.55)
        | (scored["data_quality_risk"] > 0.25)
        | (scored["equity_priority"] == 1)
        | (scored["climate_exposure"] > 0.80)
    )

    return scored.sort_values("criticality_score", ascending=False)


def create_governance_summary(scored: pd.DataFrame) -> pd.DataFrame:
    """Create governance summary for smart infrastructure review."""
    return pd.DataFrame(
        [
            {
                "assets_reviewed": len(scored),
                "mean_failure_probability": scored["failure_probability"].mean(),
                "high_risk_assets": int((scored["failure_probability"] > 0.55).sum()),
                "human_review_required": int(scored["review_required"].sum()),
                "equity_priority_assets": int(scored["equity_priority"].sum()),
                "high_climate_exposure_assets": int((scored["climate_exposure"] > 0.80).sum()),
                "mean_data_quality_risk": scored["data_quality_risk"].mean(),
            }
        ]
    )


def main() -> None:
    """Run the smart infrastructure workflow."""
    nodes, edges = create_synthetic_network()
    scored = estimate_failure_risk(nodes, edges)
    summary = create_governance_summary(scored)

    nodes.to_csv(OUTPUT_DIR / "python_infrastructure_nodes.csv", index=False)
    edges.to_csv(OUTPUT_DIR / "python_infrastructure_edges.csv", index=False)
    scored.to_csv(OUTPUT_DIR / "python_smart_network_failure_risk.csv", index=False)
    summary.to_csv(OUTPUT_DIR / "python_smart_network_governance_summary.csv", index=False)

    memo = f"""# Smart Infrastructure Governance Memo

Assets reviewed: {int(summary.loc[0, "assets_reviewed"])}
High-risk assets: {int(summary.loc[0, "high_risk_assets"])}
Human review required: {int(summary.loc[0, "human_review_required"])}
Equity-priority assets: {int(summary.loc[0, "equity_priority_assets"])}
High climate-exposure assets: {int(summary.loc[0, "high_climate_exposure_assets"])}

Recommended actions:
1. Review high-criticality assets before automated maintenance prioritization.
2. Inspect assets with high data-quality risk before accepting model scores.
3. Evaluate whether historically under-served areas are receiving adequate attention.
4. Test model behavior under climate-stress and outage scenarios.
5. Document human decisions and overrides for governance review.
"""

    (OUTPUT_DIR / "python_smart_network_governance_memo.md").write_text(memo)

    print(scored.head(10))
    print(summary.T)
    print(memo)


if __name__ == "__main__":
    main()
