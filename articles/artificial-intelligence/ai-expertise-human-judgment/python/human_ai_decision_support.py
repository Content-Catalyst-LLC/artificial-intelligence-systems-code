"""
Human-AI decision support simulation.

This script creates synthetic cases and compares AI-only, expert-only,
and combined human-AI decision scores. It also estimates warranted AI
reliance, observed AI reliance, automation-bias flags, expert-AI
disagreement, and high-complexity review requirements.

The workflow is intended for educational and governance-design purposes,
not production use.
"""

from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd


def create_cases(n_cases: int = 1000, seed: int = 42) -> pd.DataFrame:
    """Create a synthetic human-AI decision dataset."""
    rng = np.random.default_rng(seed)

    cases = pd.DataFrame(
        {
            "case_id": np.arange(1, n_cases + 1),
            "true_risk": rng.beta(2, 5, n_cases),
            "context_complexity": rng.uniform(0, 1, n_cases),
            "expertise_level": rng.uniform(0.2, 1.0, n_cases),
        }
    )

    cases["ai_score"] = np.clip(
        cases["true_risk"] + rng.normal(0, 0.09, n_cases),
        0,
        1,
    )

    cases["expert_score"] = np.clip(
        cases["true_risk"] + rng.normal(0, 0.11, n_cases),
        0,
        1,
    )

    # Warranted reliance declines when context is complex and when expert
    # capability is high enough to provide meaningful independent judgment.
    cases["warranted_ai_reliance"] = np.clip(
        0.70
        - 0.40 * cases["context_complexity"]
        - 0.15 * cases["expertise_level"],
        0,
        1,
    )

    # Observed reliance includes a positive bias term to simulate possible
    # automation bias in real workflows.
    cases["observed_ai_reliance"] = np.clip(
        cases["warranted_ai_reliance"] + rng.normal(0.10, 0.08, n_cases),
        0,
        1,
    )

    cases["combined_score"] = (
        cases["observed_ai_reliance"] * cases["ai_score"]
        + (1 - cases["observed_ai_reliance"]) * cases["expert_score"]
    )

    cases["automation_bias_flag"] = (
        cases["observed_ai_reliance"]
        > cases["warranted_ai_reliance"] + 0.15
    )

    cases["expert_ai_disagreement"] = abs(
        cases["expert_score"] - cases["ai_score"]
    )

    cases["high_complexity_review_required"] = (
        (cases["context_complexity"] > 0.70)
        | (cases["expert_ai_disagreement"] > 0.30)
        | (cases["automation_bias_flag"])
    )

    cases["complexity_band"] = pd.cut(
        cases["context_complexity"],
        bins=[0, 0.33, 0.66, 1.0],
        labels=["low", "medium", "high"],
        include_lowest=True,
    )

    return cases


def summarize_decision_quality(cases: pd.DataFrame) -> pd.DataFrame:
    """Summarize AI, expert, and combined decision quality."""
    return pd.DataFrame(
        {
            "mean_ai_score_error": [
                np.mean(abs(cases["ai_score"] - cases["true_risk"]))
            ],
            "mean_expert_score_error": [
                np.mean(abs(cases["expert_score"] - cases["true_risk"]))
            ],
            "mean_combined_score_error": [
                np.mean(abs(cases["combined_score"] - cases["true_risk"]))
            ],
            "automation_bias_rate": [
                cases["automation_bias_flag"].mean()
            ],
            "mean_expert_ai_disagreement": [
                cases["expert_ai_disagreement"].mean()
            ],
            "review_required_rate": [
                cases["high_complexity_review_required"].mean()
            ],
        }
    )


def summarize_by_complexity(cases: pd.DataFrame) -> pd.DataFrame:
    """Summarize reliance and disagreement by context complexity."""
    return (
        cases.groupby("complexity_band", observed=True)
        .agg(
            cases=("case_id", "count"),
            mean_observed_ai_reliance=("observed_ai_reliance", "mean"),
            mean_warranted_ai_reliance=("warranted_ai_reliance", "mean"),
            automation_bias_rate=("automation_bias_flag", "mean"),
            mean_disagreement=("expert_ai_disagreement", "mean"),
            review_required_rate=("high_complexity_review_required", "mean"),
        )
        .reset_index()
    )


def main() -> None:
    """Run the human-AI decision support workflow."""
    article_dir = Path(__file__).resolve().parents[1]
    output_dir = article_dir / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    cases = create_cases()
    summary = summarize_decision_quality(cases)
    complexity_summary = summarize_by_complexity(cases)

    cases.to_csv(output_dir / "human_ai_decision_cases.csv", index=False)
    summary.to_csv(output_dir / "human_ai_decision_summary.csv", index=False)
    complexity_summary.to_csv(
        output_dir / "human_ai_complexity_summary.csv",
        index=False,
    )

    print("\nDecision quality summary")
    print(summary.to_string(index=False))

    print("\nComplexity-band governance summary")
    print(complexity_summary.to_string(index=False))


if __name__ == "__main__":
    main()
