"""
Artificial Intelligence in Decision Support Systems

Python workflow:
- synthetic decision options
- expected utility scoring
- robust utility scoring
- capacity-constrained selection
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


def create_decision_options(n: int = 150) -> pd.DataFrame:
    """Create synthetic decision options for resource allocation."""
    options = pd.DataFrame(
        {
            "option_id": [f"A{i:03d}" for i in range(n)],
            "predicted_risk": rng.beta(2.5, 4.0, n),
            "benefit_if_successful": rng.normal(100, 25, n).clip(10),
            "cost": rng.normal(35, 10, n).clip(5),
            "uncertainty": rng.uniform(0.05, 0.45, n),
            "service_population": rng.integers(100, 10000, n),
            "equity_priority": rng.choice([0, 1], size=n, p=[0.75, 0.25]),
            "capacity_required": rng.integers(1, 6, n),
        }
    )

    return options


def evaluate_options(options: pd.DataFrame, total_capacity: int = 140) -> pd.DataFrame:
    """Estimate decision utility and select actions under capacity."""
    scored = options.copy()

    scored["expected_benefit"] = (
        scored["predicted_risk"] * scored["benefit_if_successful"]
    )

    scored["population_weight"] = (
        scored["service_population"] / scored["service_population"].max()
    )

    scored["expected_utility"] = (
        scored["expected_benefit"]
        - scored["cost"]
        + 15 * scored["population_weight"]
        + 10 * scored["equity_priority"]
        - 8 * scored["uncertainty"]
    )

    scored["robust_utility"] = (
        scored["expected_utility"]
        - 20 * scored["uncertainty"]
    )

    scored["human_review_required"] = (
        (scored["uncertainty"] > 0.30)
        | (scored["equity_priority"] == 1)
        | (scored["predicted_risk"] > 0.70)
    )

    scored = scored.sort_values("robust_utility", ascending=False).reset_index(drop=True)

    selected = []
    used_capacity = 0

    for _, row in scored.iterrows():
        if used_capacity + row["capacity_required"] <= total_capacity:
            selected.append(True)
            used_capacity += row["capacity_required"]
        else:
            selected.append(False)

    scored["selected_under_capacity"] = selected

    return scored


def create_governance_summary(scored: pd.DataFrame) -> pd.DataFrame:
    """Create governance summary for decision support review."""
    selected = scored[scored["selected_under_capacity"]]

    return pd.DataFrame(
        [
            {
                "options_reviewed": len(scored),
                "options_selected": int(scored["selected_under_capacity"].sum()),
                "mean_selected_risk": selected["predicted_risk"].mean(),
                "mean_selected_uncertainty": selected["uncertainty"].mean(),
                "selected_equity_priority_options": int(selected["equity_priority"].sum()),
                "human_review_required": int(scored["human_review_required"].sum()),
                "total_expected_utility": selected["expected_utility"].sum(),
                "total_robust_utility": selected["robust_utility"].sum(),
            }
        ]
    )


def main() -> None:
    """Run the AI decision support workflow."""
    options = create_decision_options()
    scored = evaluate_options(options)
    summary = create_governance_summary(scored)

    options.to_csv(OUTPUT_DIR / "python_decision_options.csv", index=False)
    scored.to_csv(OUTPUT_DIR / "python_decision_support_scored_options.csv", index=False)
    summary.to_csv(OUTPUT_DIR / "python_decision_support_governance_summary.csv", index=False)

    memo = f"""# Decision Support Governance Memo

Options reviewed: {int(summary.loc[0, "options_reviewed"])}
Options selected: {int(summary.loc[0, "options_selected"])}
Human review required: {int(summary.loc[0, "human_review_required"])}
Selected equity-priority options: {int(summary.loc[0, "selected_equity_priority_options"])}
Total expected utility: {summary.loc[0, "total_expected_utility"]:.2f}
Total robust utility: {summary.loc[0, "total_robust_utility"]:.2f}

Interpretation:
- Selected actions maximize robust utility under a capacity constraint.
- High-uncertainty and equity-priority decisions require human review.
- The system separates prediction, utility, constraints, and governance.
"""

    (OUTPUT_DIR / "python_decision_support_governance_memo.md").write_text(memo)

    print(scored.head(10))
    print(summary.T)
    print(memo)


if __name__ == "__main__":
    main()
