"""
Retrieval-Augmented Generation and AI Knowledge Systems

Python workflow:
- RAG evaluation simulation
- retrieval quality scoring
- answer grounding and citation fidelity scoring
- security and access-control review
- governance risk routing
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


def simulate_rag_evaluations(n: int = 240) -> pd.DataFrame:
    """Create synthetic RAG evaluation records."""
    query_types = [
        "direct_fact",
        "multi_hop_question",
        "policy_lookup",
        "technical_support",
        "research_synthesis",
        "compliance_question",
        "unknown_answer",
    ]

    source_types = [
        "official_policy",
        "technical_manual",
        "peer_reviewed_paper",
        "internal_note",
        "support_article",
        "archived_document",
    ]

    rows = []

    for i in range(n):
        query_type = rng.choice(query_types)
        source_type = rng.choice(source_types)

        retrieved_k = int(rng.integers(3, 12))
        relevant_retrieved = int(rng.integers(0, retrieved_k + 1))
        supporting_sources = int(rng.integers(0, min(relevant_retrieved, 5) + 1))

        source_authority = rng.uniform(0.35, 1.0)
        freshness_score = rng.uniform(0.25, 1.0)

        if source_type == "official_policy":
            source_authority = max(source_authority, 0.80)
        elif source_type == "archived_document":
            freshness_score = min(freshness_score, 0.45)

        if query_type == "unknown_answer":
            abstained = int(rng.choice([0, 1], p=[0.35, 0.65]))
            unsupported_answer_risk = 1 - abstained
        else:
            abstained = int(rng.choice([0, 1], p=[0.90, 0.10]))
            unsupported_answer_risk = rng.uniform(0.0, 0.35)

        rows.append(
            {
                "eval_id": f"RAG-EVAL-{i:03d}",
                "query_type": query_type,
                "source_type": source_type,
                "retrieved_k": retrieved_k,
                "relevant_retrieved": relevant_retrieved,
                "supporting_sources": supporting_sources,
                "retrieval_recall": relevant_retrieved / retrieved_k,
                "source_authority": float(source_authority),
                "freshness_score": float(freshness_score),
                "grounding_score": float(rng.uniform(0.35, 1.0)),
                "citation_fidelity": float(rng.uniform(0.30, 1.0)),
                "answer_quality": float(rng.uniform(0.45, 1.0)),
                "prompt_injection_resistance": float(rng.uniform(0.45, 1.0)),
                "access_control_score": float(rng.uniform(0.60, 1.0)),
                "abstained": abstained,
                "unsupported_answer_risk": float(unsupported_answer_risk),
                "latency_seconds": float(rng.gamma(shape=2.3, scale=1.1)),
                "total_tokens": int(rng.integers(1200, 12000)),
            }
        )

    return pd.DataFrame(rows)


def score_rag_system(records: pd.DataFrame) -> pd.DataFrame:
    """Score RAG evaluation records for quality and governance risk."""
    scored = records.copy()

    scored["retrieval_quality_score"] = (
        0.45 * scored["retrieval_recall"]
        + 0.25 * np.minimum(scored["supporting_sources"] / 3, 1)
        + 0.15 * scored["source_authority"]
        + 0.15 * scored["freshness_score"]
    )

    scored["answer_grounding_score"] = (
        0.35 * scored["grounding_score"]
        + 0.30 * scored["citation_fidelity"]
        + 0.20 * scored["answer_quality"]
        + 0.15 * np.minimum(scored["supporting_sources"] / 3, 1)
    )

    scored["security_score"] = (
        0.55 * scored["prompt_injection_resistance"]
        + 0.45 * scored["access_control_score"]
    )

    scored["operational_cost_index"] = np.clip(
        (scored["latency_seconds"] / 10) + (scored["total_tokens"] / 15000),
        0,
        1.5,
    )

    scored["rag_system_risk"] = (
        0.25 * (1 - scored["retrieval_quality_score"])
        + 0.25 * (1 - scored["answer_grounding_score"])
        + 0.20 * (1 - scored["security_score"])
        + 0.15 * scored["unsupported_answer_risk"]
        + 0.15 * scored["operational_cost_index"]
    )

    scored["review_required"] = (
        (scored["rag_system_risk"] > 0.42)
        | (scored["grounding_score"] < 0.60)
        | (scored["citation_fidelity"] < 0.60)
        | (scored["source_authority"] < 0.55)
        | (scored["freshness_score"] < 0.45)
        | (scored["prompt_injection_resistance"] < 0.60)
        | (scored["access_control_score"] < 0.75)
        | ((scored["query_type"] == "unknown_answer") & (scored["abstained"] == 0))
    )

    scored["deployment_recommendation"] = np.select(
        [
            scored["rag_system_risk"] > 0.58,
            scored["review_required"],
            scored["answer_grounding_score"] > 0.82,
        ],
        [
            "pause_for_knowledge_system_review",
            "approve_only_after_source_and_grounding_review",
            "candidate_for_controlled_deployment",
        ],
        default="continue_evaluation",
    )

    return scored.sort_values("rag_system_risk", ascending=False)


def summarize_by_query_type(scored: pd.DataFrame) -> pd.DataFrame:
    """Summarize RAG quality and risk by query type."""
    return (
        scored.groupby("query_type")
        .agg(
            evaluations=("eval_id", "count"),
            mean_retrieval_quality=("retrieval_quality_score", "mean"),
            mean_answer_grounding=("answer_grounding_score", "mean"),
            mean_security_score=("security_score", "mean"),
            mean_rag_system_risk=("rag_system_risk", "mean"),
            review_rate=("review_required", "mean"),
            abstention_rate=("abstained", "mean"),
            mean_latency_seconds=("latency_seconds", "mean"),
            mean_total_tokens=("total_tokens", "mean"),
        )
        .reset_index()
        .sort_values("mean_rag_system_risk", ascending=False)
    )


def main() -> None:
    """Run RAG evaluation and governance review."""
    records = simulate_rag_evaluations()
    scored = score_rag_system(records)
    query_summary = summarize_by_query_type(scored)

    governance_summary = pd.DataFrame(
        [
            {
                "evaluations_reviewed": len(scored),
                "review_required": int(scored["review_required"].sum()),
                "unknown_answer_cases": int(scored["query_type"].eq("unknown_answer").sum()),
                "failed_abstention_cases": int(
                    ((scored["query_type"] == "unknown_answer") & (scored["abstained"] == 0)).sum()
                ),
                "mean_retrieval_quality": scored["retrieval_quality_score"].mean(),
                "mean_answer_grounding": scored["answer_grounding_score"].mean(),
                "mean_security_score": scored["security_score"].mean(),
                "mean_rag_system_risk": scored["rag_system_risk"].mean(),
            }
        ]
    )

    records.to_csv(OUTPUT_DIR / "python_rag_evaluation_records.csv", index=False)
    scored.to_csv(OUTPUT_DIR / "python_rag_system_risk_scores.csv", index=False)
    query_summary.to_csv(OUTPUT_DIR / "python_rag_query_type_summary.csv", index=False)
    governance_summary.to_csv(OUTPUT_DIR / "python_rag_governance_summary.csv", index=False)

    memo = f"""# RAG Knowledge System Governance Memo

Evaluations reviewed: {int(governance_summary.loc[0, "evaluations_reviewed"])}
Review required: {int(governance_summary.loc[0, "review_required"])}
Unknown-answer cases: {int(governance_summary.loc[0, "unknown_answer_cases"])}
Failed abstention cases: {int(governance_summary.loc[0, "failed_abstention_cases"])}
Mean retrieval quality: {governance_summary.loc[0, "mean_retrieval_quality"]:.4f}
Mean answer grounding: {governance_summary.loc[0, "mean_answer_grounding"]:.4f}
Mean security score: {governance_summary.loc[0, "mean_security_score"]:.4f}
Mean RAG system risk: {governance_summary.loc[0, "mean_rag_system_risk"]:.4f}

Interpretation:
- RAG systems should be evaluated at both retrieval and generation layers.
- Citation fidelity and claim support require separate review.
- Unknown-answer cases should test whether the system abstains when evidence is absent.
- Access control, prompt-injection resistance, source authority, and freshness are governance controls.
"""

    (OUTPUT_DIR / "python_rag_governance_memo.md").write_text(memo)

    print(governance_summary.T)
    print(query_summary)
    print(scored.head(10))
    print(memo)


if __name__ == "__main__":
    main()
