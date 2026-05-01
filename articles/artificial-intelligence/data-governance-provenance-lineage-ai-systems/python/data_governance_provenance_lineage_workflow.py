"""
Data Governance, Provenance, and Lineage in AI Systems Mini-Workflow

This script demonstrates:
- provenance entities, activities, and agents
- lineage relations
- dependency tracing
- impact analysis
- governance-ready metadata tables

It is educational and uses synthetic data.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


OUTPUT_DIR = Path("../outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def build_entities() -> pd.DataFrame:
    """Create synthetic AI system entities."""
    return pd.DataFrame(
        [
            {"entity_id": "D_source_A", "entity_type": "source_dataset", "name": "Source Dataset A", "version": "2026-01"},
            {"entity_id": "D_source_B", "entity_type": "source_dataset", "name": "Source Dataset B", "version": "2026-01"},
            {"entity_id": "D_joined_1", "entity_type": "derived_dataset", "name": "Joined Training Dataset", "version": "v1"},
            {"entity_id": "F_features_2", "entity_type": "feature_table", "name": "Feature Table", "version": "v2"},
            {"entity_id": "M_model_3", "entity_type": "model", "name": "Risk Model", "version": "v3"},
            {"entity_id": "R_eval_3", "entity_type": "evaluation_report", "name": "Evaluation Report", "version": "v3"},
            {"entity_id": "D_deploy_log_3", "entity_type": "deployment_log", "name": "Deployment Log", "version": "v3"},
        ]
    )


def build_activities() -> pd.DataFrame:
    """Create synthetic pipeline activities."""
    return pd.DataFrame(
        [
            {"activity_id": "A_ingest", "activity_type": "ingestion", "name": "Ingest Source Data"},
            {"activity_id": "A_join", "activity_type": "join", "name": "Join Source Datasets"},
            {"activity_id": "A_feature", "activity_type": "feature_engineering", "name": "Build Feature Table"},
            {"activity_id": "A_train", "activity_type": "model_training", "name": "Train Model"},
            {"activity_id": "A_eval", "activity_type": "evaluation", "name": "Evaluate Model"},
            {"activity_id": "A_deploy", "activity_type": "deployment", "name": "Deploy Model"},
        ]
    )


def build_agents() -> pd.DataFrame:
    """Create synthetic responsible agents."""
    return pd.DataFrame(
        [
            {"agent_id": "G_data_team", "agent_type": "team", "name": "Data Engineering"},
            {"agent_id": "G_ml_team", "agent_type": "team", "name": "Machine Learning"},
            {"agent_id": "G_governance", "agent_type": "team", "name": "AI Governance"},
            {"agent_id": "G_platform", "agent_type": "service", "name": "MLOps Platform"},
        ]
    )


def build_relations() -> pd.DataFrame:
    """Create provenance and lineage relations."""
    return pd.DataFrame(
        [
            {"source": "D_source_A", "relation": "used_by", "target": "A_join"},
            {"source": "D_source_B", "relation": "used_by", "target": "A_join"},
            {"source": "A_join", "relation": "generated", "target": "D_joined_1"},
            {"source": "D_joined_1", "relation": "used_by", "target": "A_feature"},
            {"source": "A_feature", "relation": "generated", "target": "F_features_2"},
            {"source": "F_features_2", "relation": "used_by", "target": "A_train"},
            {"source": "A_train", "relation": "generated", "target": "M_model_3"},
            {"source": "M_model_3", "relation": "used_by", "target": "A_eval"},
            {"source": "A_eval", "relation": "generated", "target": "R_eval_3"},
            {"source": "M_model_3", "relation": "used_by", "target": "A_deploy"},
            {"source": "A_deploy", "relation": "generated", "target": "D_deploy_log_3"},
            {"source": "G_data_team", "relation": "responsible_for", "target": "A_join"},
            {"source": "G_ml_team", "relation": "responsible_for", "target": "A_train"},
            {"source": "G_governance", "relation": "reviewed", "target": "R_eval_3"},
            {"source": "G_platform", "relation": "executed", "target": "A_deploy"},
        ]
    )


def build_quality_checks() -> pd.DataFrame:
    """Create synthetic quality and governance checks."""
    return pd.DataFrame(
        [
            {"entity_id": "D_source_A", "quality_metric": "completeness", "value": 0.96, "status": "pass"},
            {"entity_id": "D_source_B", "quality_metric": "completeness", "value": 0.88, "status": "warning"},
            {"entity_id": "D_joined_1", "quality_metric": "schema_validity", "value": 0.99, "status": "pass"},
            {"entity_id": "F_features_2", "quality_metric": "missing_rate", "value": 0.07, "status": "warning"},
            {"entity_id": "M_model_3", "quality_metric": "external_validation_ready", "value": 1.00, "status": "pass"},
            {"entity_id": "R_eval_3", "quality_metric": "governance_review_complete", "value": 1.00, "status": "pass"},
        ]
    )


def downstream_dependencies(start_entity: str, relation_table: pd.DataFrame) -> set[str]:
    """
    Find downstream nodes reachable from a starting entity.

    This is a simple graph traversal for educational lineage analysis.
    """
    visited: set[str] = set()
    frontier: list[str] = [start_entity]

    while frontier:
        current = frontier.pop()

        if current in visited:
            continue

        visited.add(current)

        children = relation_table.loc[
            relation_table["source"] == current,
            "target"
        ].tolist()

        frontier.extend(children)

    visited.remove(start_entity)
    return visited


def main() -> None:
    entities = build_entities()
    activities = build_activities()
    agents = build_agents()
    relations = build_relations()
    quality_checks = build_quality_checks()

    impacted_by_source_b = downstream_dependencies("D_source_B", relations)

    impact_table = pd.DataFrame(
        [
            {
                "source_entity": "D_source_B",
                "impacted_nodes": ", ".join(sorted(impacted_by_source_b)),
                "impacted_model_present": "M_model_3" in impacted_by_source_b,
                "impacted_deployment_log_present": "D_deploy_log_3" in impacted_by_source_b,
            }
        ]
    )

    entities.to_csv(OUTPUT_DIR / "provenance_entities.csv", index=False)
    activities.to_csv(OUTPUT_DIR / "provenance_activities.csv", index=False)
    agents.to_csv(OUTPUT_DIR / "provenance_agents.csv", index=False)
    relations.to_csv(OUTPUT_DIR / "provenance_relations.csv", index=False)
    quality_checks.to_csv(OUTPUT_DIR / "quality_checks.csv", index=False)
    impact_table.to_csv(OUTPUT_DIR / "lineage_impact_analysis.csv", index=False)

    print("Entities")
    print(entities)

    print("\nRelations")
    print(relations)

    print("\nQuality Checks")
    print(quality_checks)

    print("\nImpact Analysis")
    print(impact_table)


if __name__ == "__main__":
    main()
