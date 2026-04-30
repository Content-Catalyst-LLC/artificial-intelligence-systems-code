"""
Knowledge Representation and Symbolic AI Mini-Workflow

This script demonstrates:
- symbolic facts
- semantic triples
- rule-based inference
- inferred conclusions
- audit-friendly inference traces

It is educational and does not use private data.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


OUTPUT_DIR = Path("../outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def build_facts() -> pd.DataFrame:
    """Create a synthetic symbolic fact table."""
    return pd.DataFrame(
        [
            {"subject": "ModelA", "predicate": "type", "object": "HighImpactSystem"},
            {"subject": "DatasetB", "predicate": "type", "object": "SensitiveDataset"},
            {"subject": "ModelA", "predicate": "trainedOn", "object": "DatasetB"},
            {"subject": "ModelC", "predicate": "type", "object": "LowImpactSystem"},
            {"subject": "DatasetD", "predicate": "type", "object": "PublicDataset"},
            {"subject": "ModelC", "predicate": "trainedOn", "object": "DatasetD"},
            {"subject": "ModelE", "predicate": "type", "object": "HighImpactSystem"},
            {"subject": "DatasetF", "predicate": "type", "object": "SensitiveDataset"},
            {"subject": "ModelE", "predicate": "trainedOn", "object": "DatasetF"},
        ]
    )


def has_fact(facts: pd.DataFrame, subject: str, predicate: str, object_value: str) -> bool:
    """Check whether a fact exists in the symbolic fact table."""
    match = facts[
        (facts["subject"] == subject)
        & (facts["predicate"] == predicate)
        & (facts["object"] == object_value)
    ]
    return len(match) > 0


def objects_for(facts: pd.DataFrame, subject: str, predicate: str) -> list[str]:
    """Return all objects connected to subject by predicate."""
    return facts[
        (facts["subject"] == subject)
        & (facts["predicate"] == predicate)
    ]["object"].tolist()


def infer_governance_requirements(facts: pd.DataFrame) -> pd.DataFrame:
    """Infer governance requirements from symbolic facts."""
    inference_traces = []

    models = facts[facts["predicate"] == "trainedOn"]["subject"].unique()

    for model in models:
        datasets = objects_for(facts, model, "trainedOn")

        for dataset in datasets:
            if (
                has_fact(facts, model, "type", "HighImpactSystem")
                and has_fact(facts, dataset, "type", "SensitiveDataset")
            ):
                inference_traces.append(
                    {
                        "inferred_subject": model,
                        "inferred_predicate": "requires",
                        "inferred_object": "FairnessReview",
                        "rule_applied": "high_impact_sensitive_data_requires_fairness_review",
                        "supporting_facts": (
                            f"{model} type HighImpactSystem; "
                            f"{model} trainedOn {dataset}; "
                            f"{dataset} type SensitiveDataset"
                        ),
                    }
                )

    return pd.DataFrame(inference_traces)


def expand_knowledge_graph(facts: pd.DataFrame, inferences: pd.DataFrame) -> pd.DataFrame:
    """Combine base facts and inferred facts."""
    if inferences.empty:
        return facts.copy()

    inferred_triples = inferences.rename(
        columns={
            "inferred_subject": "subject",
            "inferred_predicate": "predicate",
            "inferred_object": "object",
        }
    )[["subject", "predicate", "object"]]

    return pd.concat([facts, inferred_triples], ignore_index=True)


def main() -> None:
    facts = build_facts()
    inferences = infer_governance_requirements(facts)
    expanded_graph = expand_knowledge_graph(facts, inferences)

    facts.to_csv(OUTPUT_DIR / "symbolic_facts.csv", index=False)
    inferences.to_csv(OUTPUT_DIR / "symbolic_inference_traces.csv", index=False)
    expanded_graph.to_csv(OUTPUT_DIR / "expanded_symbolic_knowledge_graph.csv", index=False)

    print("Facts:")
    print(facts)

    print("\nInferences:")
    print(inferences)

    print("\nExpanded knowledge graph:")
    print(expanded_graph)


if __name__ == "__main__":
    main()
