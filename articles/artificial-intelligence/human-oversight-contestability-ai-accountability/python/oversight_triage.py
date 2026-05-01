"""
Oversight triage simulation for AI-assisted decisions.

This script creates synthetic cases and applies a transparent escalation rule.
It is intended for educational and governance-design purposes, not production use.
"""

from pathlib import Path
import numpy as np
import pandas as pd


def create_cases(n_cases: int = 1000, seed: int = 42) -> pd.DataFrame:
    """Create a synthetic AI-assisted decision dataset."""
    rng = np.random.default_rng(seed)

    cases = pd.DataFrame(
        {
            "case_id": np.arange(1, n_cases + 1),
            "uncertainty": rng.beta(2, 5, n_cases),
            "harm_probability": rng.beta(2, 8, n_cases),
            "harm_impact": rng.uniform(0.1, 1.0, n_cases),
            "rights_sensitive": rng.binomial(1, 0.20, n_cases),
            "vulnerable_context": rng.binomial(1, 0.15, n_cases),
        }
    )

    cases["expected_risk"] = cases["harm_probability"] * cases["harm_impact"]
    return cases


def apply_escalation_rule(
    cases: pd.DataFrame,
    risk_threshold: float = 0.18,
    uncertainty_threshold: float = 0.55,
) -> pd.DataFrame:
    """Apply a transparent governance escalation rule."""
    cases = cases.copy()

    cases["human_review_required"] = (
        (cases["expected_risk"] >= risk_threshold)
        | (cases["uncertainty"] >= uncertainty_threshold)
        | (cases["rights_sensitive"] == 1)
        | (cases["vulnerable_context"] == 1)
    )

    cases["route"] = np.where(
        cases["human_review_required"],
        "human_review",
        "standard_processing",
    )
    return cases


def summarize_routes(cases: pd.DataFrame) -> pd.DataFrame:
    """Summarize oversight routing behavior."""
    return (
        cases.groupby("route")
        .agg(
            cases=("case_id", "count"),
            mean_uncertainty=("uncertainty", "mean"),
            mean_expected_risk=("expected_risk", "mean"),
            rights_sensitive_share=("rights_sensitive", "mean"),
            vulnerable_context_share=("vulnerable_context", "mean"),
        )
        .reset_index()
    )


def main() -> None:
    """Run the oversight triage workflow."""
    article_dir = Path(__file__).resolve().parents[1]
    output_dir = article_dir / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    cases = create_cases()
    cases = apply_escalation_rule(cases)
    summary = summarize_routes(cases)

    cases.to_csv(output_dir / "oversight_triage_cases.csv", index=False)
    summary.to_csv(output_dir / "oversight_triage_summary.csv", index=False)

    print(summary)
    print(f"Overall review rate: {cases['human_review_required'].mean():.2%}")


if __name__ == "__main__":
    main()
