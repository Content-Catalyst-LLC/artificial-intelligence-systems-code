"""
Large Language Models and Foundation Model Systems

Python workflow:
- LLM application evaluation simulation
- quality, grounding, factuality, safety, security, cost, and latency scoring
- governance risk routing
- summary tables and governance memo
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


def simulate_llm_evaluations(n: int = 220) -> pd.DataFrame:
    """Create synthetic evaluation records for LLM system responses."""
    use_cases = [
        "knowledge_search",
        "document_summary",
        "code_assistance",
        "policy_explanation",
        "research_synthesis",
        "customer_support",
        "decision_support",
    ]

    risk_levels = ["low", "medium", "high"]

    rows = []

    for i in range(n):
        use_case = rng.choice(use_cases)
        risk_level = rng.choice(risk_levels, p=[0.50, 0.35, 0.15])

        rows.append(
            {
                "eval_id": f"LLM-EVAL-{i:03d}",
                "use_case": use_case,
                "risk_level": risk_level,
                "task_quality": float(rng.uniform(0.55, 0.98)),
                "grounding_score": float(rng.uniform(0.35, 0.98)),
                "factuality_score": float(rng.uniform(0.45, 0.99)),
                "citation_fidelity": float(rng.uniform(0.35, 0.98)),
                "safety_score": float(rng.uniform(0.55, 1.00)),
                "prompt_injection_resistance": float(rng.uniform(0.40, 0.98)),
                "privacy_control_score": float(rng.uniform(0.55, 1.00)),
                "retrieved_sources": int(rng.integers(0, 8)),
                "tool_calls": int(rng.integers(0, 5)),
                "input_tokens": int(rng.integers(400, 9000)),
                "output_tokens": int(rng.integers(100, 1800)),
                "latency_seconds": float(rng.gamma(shape=2.5, scale=1.2)),
            }
        )

    return pd.DataFrame(rows)


def score_llm_system(records: pd.DataFrame) -> pd.DataFrame:
    """Score LLM evaluation records for quality and governance risk."""
    scored = records.copy()

    scored["total_tokens"] = scored["input_tokens"] + scored["output_tokens"]

    scored["quality_score"] = (
        0.25 * scored["task_quality"]
        + 0.25 * scored["grounding_score"]
        + 0.25 * scored["factuality_score"]
        + 0.25 * scored["citation_fidelity"]
    )

    scored["security_and_safety_score"] = (
        0.40 * scored["safety_score"]
        + 0.30 * scored["prompt_injection_resistance"]
        + 0.30 * scored["privacy_control_score"]
    )

    scored["operational_cost_index"] = np.clip(
        (scored["total_tokens"] / 10000)
        + (scored["latency_seconds"] / 20)
        + (scored["tool_calls"] / 10),
        0,
        1.5,
    )

    risk_weight = scored["risk_level"].map(
        {
            "low": 0.10,
            "medium": 0.25,
            "high": 0.45,
        }
    )

    scored["llm_system_risk"] = (
        0.25 * (1 - scored["quality_score"])
        + 0.25 * (1 - scored["security_and_safety_score"])
        + 0.20 * (1 - scored["grounding_score"])
        + 0.15 * scored["operational_cost_index"]
        + 0.15 * risk_weight
    )

    scored["review_required"] = (
        (scored["llm_system_risk"] > 0.40)
        | (scored["risk_level"].eq("high"))
        | (scored["grounding_score"] < 0.60)
        | (scored["factuality_score"] < 0.65)
        | (scored["prompt_injection_resistance"] < 0.60)
        | (scored["privacy_control_score"] < 0.70)
    )

    scored["deployment_recommendation"] = np.select(
        [
            scored["llm_system_risk"] > 0.55,
            scored["review_required"],
            scored["quality_score"] > 0.82,
        ],
        [
            "pause_for_system_risk_review",
            "approve_only_after_human_review",
            "candidate_for_controlled_deployment",
        ],
        default="continue_evaluation",
    )

    return scored.sort_values("llm_system_risk", ascending=False)


def summarize_by_use_case(scored: pd.DataFrame) -> pd.DataFrame:
    """Summarize quality and risk by use case."""
    return (
        scored.groupby("use_case")
        .agg(
            evaluations=("eval_id", "count"),
            mean_quality_score=("quality_score", "mean"),
            mean_grounding_score=("grounding_score", "mean"),
            mean_factuality_score=("factuality_score", "mean"),
            mean_security_and_safety=("security_and_safety_score", "mean"),
            mean_llm_system_risk=("llm_system_risk", "mean"),
            review_rate=("review_required", "mean"),
            mean_total_tokens=("total_tokens", "mean"),
            mean_latency_seconds=("latency_seconds", "mean"),
        )
        .reset_index()
        .sort_values("mean_llm_system_risk", ascending=False)
    )


def main() -> None:
    """Run LLM system evaluation and governance review."""
    records = simulate_llm_evaluations()
    scored = score_llm_system(records)
    use_case_summary = summarize_by_use_case(scored)

    governance_summary = pd.DataFrame(
        [
            {
                "evaluations_reviewed": len(scored),
                "review_required": int(scored["review_required"].sum()),
                "high_risk_cases": int(scored["risk_level"].eq("high").sum()),
                "mean_quality_score": scored["quality_score"].mean(),
                "mean_grounding_score": scored["grounding_score"].mean(),
                "mean_system_risk": scored["llm_system_risk"].mean(),
                "mean_total_tokens": scored["total_tokens"].mean(),
                "mean_latency_seconds": scored["latency_seconds"].mean(),
            }
        ]
    )

    records.to_csv(OUTPUT_DIR / "python_llm_evaluation_records.csv", index=False)
    scored.to_csv(OUTPUT_DIR / "python_llm_system_risk_scores.csv", index=False)
    use_case_summary.to_csv(OUTPUT_DIR / "python_llm_use_case_summary.csv", index=False)
    governance_summary.to_csv(OUTPUT_DIR / "python_llm_governance_summary.csv", index=False)

    memo = f"""# LLM Foundation Model System Governance Memo

Evaluations reviewed: {int(governance_summary.loc[0, "evaluations_reviewed"])}
Review required: {int(governance_summary.loc[0, "review_required"])}
High-risk cases: {int(governance_summary.loc[0, "high_risk_cases"])}
Mean quality score: {governance_summary.loc[0, "mean_quality_score"]:.4f}
Mean grounding score: {governance_summary.loc[0, "mean_grounding_score"]:.4f}
Mean system risk: {governance_summary.loc[0, "mean_system_risk"]:.4f}
Mean total tokens: {governance_summary.loc[0, "mean_total_tokens"]:.2f}
Mean latency seconds: {governance_summary.loc[0, "mean_latency_seconds"]:.2f}

Interpretation:
- LLM systems should be evaluated by use case, not only by general benchmarks.
- Grounding, factuality, citation fidelity, safety, and security should be reviewed together.
- High-risk use cases require human review and explicit deployment boundaries.
- Token cost, latency, retrieval quality, and tool behavior are system-level governance concerns.
"""

    (OUTPUT_DIR / "python_llm_governance_memo.md").write_text(memo)

    print(governance_summary.T)
    print(use_case_summary)
    print(scored.head(10))
    print(memo)


if __name__ == "__main__":
    main()
