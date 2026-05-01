"""
AI in Education, Knowledge Work, and Learning Systems

Python workflow:
- Simulate AI-supported learning records.
- Evaluate learning gain, assisted performance, independent transfer,
  feedback quality, equity gaps, privacy risk, dependency risk, and governance risk.
- Produce governance-ready summaries.

Educational systems workflow only.
This code does not make student-specific educational decisions.
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


def clamp(values: np.ndarray | pd.Series, lower: float = 0.0, upper: float = 1.0):
    """Clamp values to a bounded interval."""
    return np.clip(values, lower, upper)


def simulate_learning_records(n: int = 4000) -> pd.DataFrame:
    """Create synthetic learning-system records for governance review."""
    course_type = rng.choice(
        ["writing", "mathematics", "science", "programming", "professional_learning"],
        size=n,
        p=[0.25, 0.20, 0.20, 0.20, 0.15],
    )

    access_context = rng.choice(
        ["high_access", "moderate_access", "limited_access"],
        size=n,
        p=[0.46, 0.38, 0.16],
    )

    language_context = rng.choice(
        ["dominant_instruction_language", "multilingual_or_language_support"],
        size=n,
        p=[0.78, 0.22],
    )

    accommodation_context = rng.choice(
        ["no_recorded_accommodation", "accessibility_support"],
        size=n,
        p=[0.86, 0.14],
    )

    baseline_knowledge = clamp(rng.normal(0.52, 0.17, n))
    effort = clamp(rng.normal(0.62, 0.18, n))
    ai_usage_intensity = clamp(rng.beta(a=2.2, b=2.5, size=n))
    teacher_integration_quality = clamp(rng.normal(0.68, 0.16, n))

    access_penalty = np.select(
        [
            access_context == "high_access",
            access_context == "moderate_access",
            access_context == "limited_access",
        ],
        [0.00, -0.04, -0.12],
        default=0.0,
    )

    language_support_effect = np.where(language_context == "multilingual_or_language_support", 0.04, 0.0)
    accessibility_effect = np.where(accommodation_context == "accessibility_support", 0.05, 0.0)

    learning_support_effect = (
        0.18 * ai_usage_intensity * teacher_integration_quality
        + 0.16 * effort
        + language_support_effect
        + accessibility_effect
        + access_penalty
    )

    dependency_risk = clamp(ai_usage_intensity * (1 - effort) * (1 - teacher_integration_quality + 0.25))

    post_learning_score = clamp(
        baseline_knowledge
        + learning_support_effect
        - 0.10 * dependency_risk
        + rng.normal(0, 0.07, n)
    )

    assisted_performance = clamp(
        post_learning_score
        + 0.16 * ai_usage_intensity
        + rng.normal(0, 0.05, n)
    )

    independent_transfer = clamp(
        post_learning_score
        + 0.08 * effort
        - 0.18 * dependency_risk
        + rng.normal(0, 0.06, n)
    )

    feedback_quality = clamp(
        0.35 * teacher_integration_quality
        + 0.25 * baseline_knowledge
        + 0.25 * effort
        + 0.15 * ai_usage_intensity
        + rng.normal(0, 0.08, n)
    )

    privacy_risk = clamp(
        0.12
        + 0.25 * ai_usage_intensity
        + 0.15 * (course_type == "professional_learning").astype(float)
        + 0.10 * (course_type == "writing").astype(float)
        + rng.normal(0, 0.05, n)
    )

    assessment_substitution_risk = clamp(
        0.40 * ai_usage_intensity
        + 0.35 * (1 - effort)
        + 0.20 * np.isin(course_type, ["writing", "programming"]).astype(float)
        - 0.20 * teacher_integration_quality
        + rng.normal(0, 0.05, n)
    )

    return pd.DataFrame(
        {
            "learner_record_id": [f"LEARN-{i:05d}" for i in range(n)],
            "course_type": course_type,
            "access_context": access_context,
            "language_context": language_context,
            "accommodation_context": accommodation_context,
            "baseline_knowledge": baseline_knowledge,
            "post_learning_score": post_learning_score,
            "assisted_performance": assisted_performance,
            "independent_transfer": independent_transfer,
            "effort": effort,
            "ai_usage_intensity": ai_usage_intensity,
            "teacher_integration_quality": teacher_integration_quality,
            "feedback_quality": feedback_quality,
            "dependency_risk": dependency_risk,
            "privacy_risk": privacy_risk,
            "assessment_substitution_risk": assessment_substitution_risk,
        }
    )


def evaluate_learning_system(records: pd.DataFrame) -> pd.DataFrame:
    """Add learning gain, transfer gap, and governance risk measures."""
    evaluated = records.copy()

    evaluated["learning_gain"] = evaluated["post_learning_score"] - evaluated["baseline_knowledge"]
    evaluated["assistance_gap"] = evaluated["assisted_performance"] - evaluated["independent_transfer"]

    evaluated["learning_system_governance_risk"] = clamp(
        0.24 * evaluated["assessment_substitution_risk"]
        + 0.22 * evaluated["privacy_risk"]
        + 0.20 * evaluated["dependency_risk"]
        + 0.16 * (1 - evaluated["feedback_quality"])
        + 0.10 * (evaluated["assistance_gap"] > 0.18).astype(float)
        + 0.08 * (evaluated["teacher_integration_quality"] < 0.50).astype(float)
    )

    evaluated["human_review_recommended"] = (
        (evaluated["learning_system_governance_risk"] > 0.42)
        | (evaluated["assessment_substitution_risk"] > 0.55)
        | (evaluated["privacy_risk"] > 0.48)
        | (evaluated["assistance_gap"] > 0.24)
        | (evaluated["feedback_quality"] < 0.35)
    )

    return evaluated


def summarize_by_group(records: pd.DataFrame) -> pd.DataFrame:
    """Summarize learning outcomes and risks by group/context."""
    group_columns = ["course_type", "access_context", "language_context", "accommodation_context"]
    rows = []

    overall_learning_gain = records["learning_gain"].mean()
    overall_transfer = records["independent_transfer"].mean()
    overall_risk = records["learning_system_governance_risk"].mean()

    for column in group_columns:
        for value, subset in records.groupby(column):
            rows.append(
                {
                    "group_type": column,
                    "group_value": value,
                    "records": len(subset),
                    "mean_learning_gain": subset["learning_gain"].mean(),
                    "mean_independent_transfer": subset["independent_transfer"].mean(),
                    "mean_assisted_performance": subset["assisted_performance"].mean(),
                    "mean_assistance_gap": subset["assistance_gap"].mean(),
                    "mean_feedback_quality": subset["feedback_quality"].mean(),
                    "mean_dependency_risk": subset["dependency_risk"].mean(),
                    "mean_privacy_risk": subset["privacy_risk"].mean(),
                    "mean_assessment_substitution_risk": subset["assessment_substitution_risk"].mean(),
                    "mean_governance_risk": subset["learning_system_governance_risk"].mean(),
                    "human_review_rate": subset["human_review_recommended"].mean(),
                    "learning_gain_gap_from_overall": subset["learning_gain"].mean() - overall_learning_gain,
                    "transfer_gap_from_overall": subset["independent_transfer"].mean() - overall_transfer,
                    "risk_gap_from_overall": subset["learning_system_governance_risk"].mean() - overall_risk,
                }
            )

    summary = pd.DataFrame(rows)

    summary["review_required"] = (
        (summary["records"] < 100)
        | (summary["learning_gain_gap_from_overall"].abs() > 0.06)
        | (summary["transfer_gap_from_overall"].abs() > 0.06)
        | (summary["risk_gap_from_overall"] > 0.08)
        | (summary["mean_assistance_gap"] > 0.18)
        | (summary["human_review_rate"] > 0.35)
    )

    return summary.sort_values(["review_required", "mean_governance_risk"], ascending=[False, False])


def main() -> None:
    """Run learning AI evaluation and governance review."""
    records = simulate_learning_records()
    evaluated = evaluate_learning_system(records)
    group_summary = summarize_by_group(evaluated)

    governance_summary = pd.DataFrame(
        [
            {
                "records_reviewed": len(evaluated),
                "mean_learning_gain": evaluated["learning_gain"].mean(),
                "mean_independent_transfer": evaluated["independent_transfer"].mean(),
                "mean_assisted_performance": evaluated["assisted_performance"].mean(),
                "mean_assistance_gap": evaluated["assistance_gap"].mean(),
                "mean_feedback_quality": evaluated["feedback_quality"].mean(),
                "mean_dependency_risk": evaluated["dependency_risk"].mean(),
                "mean_privacy_risk": evaluated["privacy_risk"].mean(),
                "mean_assessment_substitution_risk": evaluated["assessment_substitution_risk"].mean(),
                "mean_governance_risk": evaluated["learning_system_governance_risk"].mean(),
                "human_review_recommended_records": int(evaluated["human_review_recommended"].sum()),
                "groups_requiring_review": int(group_summary["review_required"].sum()),
            }
        ]
    )

    evaluated.to_csv(OUTPUT_DIR / "python_learning_ai_records.csv", index=False)
    group_summary.to_csv(OUTPUT_DIR / "python_learning_ai_group_review.csv", index=False)
    governance_summary.to_csv(OUTPUT_DIR / "python_learning_ai_governance_summary.csv", index=False)

    memo = f"""# AI Learning System Governance Memo

Records reviewed: {int(governance_summary.loc[0, "records_reviewed"])}
Mean learning gain: {governance_summary.loc[0, "mean_learning_gain"]:.4f}
Mean independent transfer: {governance_summary.loc[0, "mean_independent_transfer"]:.4f}
Mean assisted performance: {governance_summary.loc[0, "mean_assisted_performance"]:.4f}
Mean assistance gap: {governance_summary.loc[0, "mean_assistance_gap"]:.4f}
Mean feedback quality: {governance_summary.loc[0, "mean_feedback_quality"]:.4f}
Mean dependency risk: {governance_summary.loc[0, "mean_dependency_risk"]:.4f}
Mean privacy risk: {governance_summary.loc[0, "mean_privacy_risk"]:.4f}
Mean assessment substitution risk: {governance_summary.loc[0, "mean_assessment_substitution_risk"]:.4f}
Mean governance risk: {governance_summary.loc[0, "mean_governance_risk"]:.4f}
Human-review recommended records: {int(governance_summary.loc[0, "human_review_recommended_records"])}
Groups requiring review: {int(governance_summary.loc[0, "groups_requiring_review"])}

Interpretation:
- AI-supported learning should be evaluated by learning gain and independent transfer, not output quality alone.
- A large assistance gap can indicate dependence on AI-assisted performance rather than durable learning.
- Feedback quality, privacy risk, assessment substitution risk, and equity gaps should be monitored.
- Review should focus on contexts where AI use weakens evidence of learning or creates unequal benefit.
"""

    (OUTPUT_DIR / "python_learning_ai_governance_memo.md").write_text(memo)

    print(governance_summary.T)
    print(group_summary.head(20))
    print(memo)


if __name__ == "__main__":
    main()
