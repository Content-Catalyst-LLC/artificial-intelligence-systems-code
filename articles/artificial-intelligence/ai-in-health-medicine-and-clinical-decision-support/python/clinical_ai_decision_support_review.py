"""
AI in Health, Medicine, and Clinical Decision Support

Python workflow:
- Simulate clinical decision support prediction logs.
- Evaluate performance, calibration, subgroup differences, alert burden,
  clinical utility, and governance risk.
- Produce governance-ready outputs for clinical AI review.

Educational systems workflow only.
Not medical advice, not regulatory advice, and not a substitute for local
clinical validation, privacy, safety, or compliance review.
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


def sigmoid(values: np.ndarray) -> np.ndarray:
    """Compute logistic sigmoid."""
    return 1 / (1 + np.exp(-values))


def simulate_clinical_predictions(n: int = 5000) -> pd.DataFrame:
    """Create synthetic clinical prediction records for governance review."""
    site = rng.choice(["hospital_a", "hospital_b", "hospital_c"], size=n, p=[0.50, 0.32, 0.18])
    unit = rng.choice(["ward", "icu", "ed"], size=n, p=[0.58, 0.22, 0.20])
    age_band = rng.choice(["18_44", "45_64", "65_84", "85_plus"], size=n, p=[0.22, 0.34, 0.34, 0.10])
    language_group = rng.choice(["english", "non_english"], size=n, p=[0.82, 0.18])

    vital_score = rng.normal(0, 1, n)
    lab_score = rng.normal(0, 1, n)
    comorbidity_score = rng.gamma(shape=2.0, scale=0.6, size=n)
    missingness_score = rng.beta(a=1.2, b=6.0, size=n)

    unit_shift = np.select([unit == "ward", unit == "icu", unit == "ed"], [0.0, 0.9, 0.35], default=0.0)
    age_shift = np.select(
        [age_band == "18_44", age_band == "45_64", age_band == "65_84", age_band == "85_plus"],
        [-0.35, 0.0, 0.45, 0.75],
        default=0.0,
    )
    language_shift = np.where(language_group == "non_english", 0.18, 0.0)
    site_shift = np.select([site == "hospital_a", site == "hospital_b", site == "hospital_c"], [0.0, 0.15, -0.10], default=0.0)

    true_logit = (
        0.90 * vital_score
        + 0.65 * lab_score
        + 0.55 * comorbidity_score
        + unit_shift
        + age_shift
        + language_shift
        + site_shift
        - 2.45
    )

    true_probability = sigmoid(true_logit)
    outcome = rng.binomial(1, true_probability)

    model_logit = (
        0.82 * vital_score
        + 0.58 * lab_score
        + 0.48 * comorbidity_score
        + 0.72 * unit_shift
        + 0.35 * age_shift
        + 0.03 * language_shift
        + 0.05 * site_shift
        - 2.10
        + rng.normal(0, 0.45, n)
    )

    predicted_probability = sigmoid(model_logit)

    return pd.DataFrame(
        {
            "case_id": [f"CLIN-{i:05d}" for i in range(n)],
            "site": site,
            "unit": unit,
            "age_band": age_band,
            "language_group": language_group,
            "vital_score": vital_score,
            "lab_score": lab_score,
            "comorbidity_score": comorbidity_score,
            "missingness_score": missingness_score,
            "true_probability": true_probability,
            "predicted_probability": predicted_probability,
            "outcome": outcome,
        }
    )


def binary_metrics(records: pd.DataFrame, threshold: float = 0.25) -> dict[str, float]:
    """Compute threshold-based clinical decision support metrics."""
    y = records["outcome"].to_numpy()
    p = records["predicted_probability"].to_numpy()
    alerts = p >= threshold

    tp = int(np.sum((alerts == 1) & (y == 1)))
    fp = int(np.sum((alerts == 1) & (y == 0)))
    tn = int(np.sum((alerts == 0) & (y == 0)))
    fn = int(np.sum((alerts == 0) & (y == 1)))

    sensitivity = tp / max(tp + fn, 1)
    specificity = tn / max(tn + fp, 1)
    ppv = tp / max(tp + fp, 1)
    npv = tn / max(tn + fn, 1)
    alert_rate = float(np.mean(alerts))
    brier = float(np.mean((p - y) ** 2))

    utility = (
        2.0 * tp
        - 0.25 * fp
        - 4.0 * fn
        - 0.05 * np.sum(alerts)
    ) / len(records)

    return {
        "cases": len(records),
        "threshold": threshold,
        "true_positives": tp,
        "false_positives": fp,
        "true_negatives": tn,
        "false_negatives": fn,
        "sensitivity": sensitivity,
        "specificity": specificity,
        "positive_predictive_value": ppv,
        "negative_predictive_value": npv,
        "alert_rate": alert_rate,
        "brier_score": brier,
        "clinical_utility_proxy": utility,
    }


def calibration_bins(records: pd.DataFrame, bins: int = 10) -> pd.DataFrame:
    """Compute bin-level calibration summary."""
    data = records.copy()
    data["risk_bin"] = pd.cut(
        data["predicted_probability"],
        bins=np.linspace(0, 1, bins + 1),
        include_lowest=True,
    )

    grouped = (
        data.groupby("risk_bin", observed=True)
        .agg(
            cases=("case_id", "count"),
            mean_predicted_risk=("predicted_probability", "mean"),
            observed_event_rate=("outcome", "mean"),
            mean_missingness=("missingness_score", "mean"),
        )
        .reset_index()
    )

    grouped["absolute_calibration_gap"] = (
        grouped["observed_event_rate"] - grouped["mean_predicted_risk"]
    ).abs()

    grouped["weighted_calibration_gap"] = (
        grouped["cases"] / grouped["cases"].sum()
    ) * grouped["absolute_calibration_gap"]

    return grouped


def subgroup_review(records: pd.DataFrame, threshold: float = 0.25) -> pd.DataFrame:
    """Compute clinical decision support metrics by subgroup."""
    rows = []

    for column in ["site", "unit", "age_band", "language_group"]:
        for value, subset in records.groupby(column):
            metrics = binary_metrics(subset, threshold=threshold)
            bins = calibration_bins(subset)
            rows.append(
                {
                    "subgroup_type": column,
                    "subgroup_value": value,
                    **metrics,
                    "expected_calibration_error": float(bins["weighted_calibration_gap"].sum()),
                }
            )

    summary = pd.DataFrame(rows)

    overall = binary_metrics(records, threshold=threshold)
    summary["sensitivity_gap_from_overall"] = summary["sensitivity"] - overall["sensitivity"]
    summary["alert_rate_gap_from_overall"] = summary["alert_rate"] - overall["alert_rate"]

    summary["review_required"] = (
        (summary["cases"] < 100)
        | (summary["sensitivity_gap_from_overall"].abs() > 0.12)
        | (summary["alert_rate_gap_from_overall"].abs() > 0.12)
        | (summary["expected_calibration_error"] > 0.08)
        | (summary["false_negatives"] > 20)
    )

    return summary.sort_values(["review_required", "expected_calibration_error"], ascending=[False, False])


def governance_risk(records: pd.DataFrame, threshold: float = 0.25) -> pd.DataFrame:
    """Score case-level governance risk for review routing."""
    scored = records.copy()

    scored["alert"] = scored["predicted_probability"] >= threshold
    scored["uncertainty_zone"] = scored["predicted_probability"].between(threshold - 0.05, threshold + 0.05)

    scored["clinical_ai_governance_risk"] = np.clip(
        0.25 * scored["missingness_score"]
        + 0.25 * scored["uncertainty_zone"].astype(float)
        + 0.20 * (scored["unit"] == "icu").astype(float)
        + 0.15 * (scored["age_band"] == "85_plus").astype(float)
        + 0.15 * (scored["language_group"] == "non_english").astype(float),
        0,
        1,
    )

    scored["human_review_recommended"] = (
        (scored["clinical_ai_governance_risk"] > 0.40)
        | (scored["missingness_score"] > 0.35)
        | (scored["uncertainty_zone"] & (scored["unit"].isin(["icu", "ed"])))
    )

    return scored.sort_values("clinical_ai_governance_risk", ascending=False)


def main() -> None:
    """Run clinical AI validation and governance review."""
    threshold = 0.25
    records = simulate_clinical_predictions()

    overall_metrics = pd.DataFrame([binary_metrics(records, threshold=threshold)])
    bins = calibration_bins(records)
    subgroup_summary = subgroup_review(records, threshold=threshold)
    scored = governance_risk(records, threshold=threshold)

    governance_summary = pd.DataFrame(
        [
            {
                "cases_reviewed": len(records),
                "threshold": threshold,
                "expected_calibration_error": float(bins["weighted_calibration_gap"].sum()),
                "subgroups_requiring_review": int(subgroup_summary["review_required"].sum()),
                "human_review_recommended_cases": int(scored["human_review_recommended"].sum()),
                "mean_governance_risk": float(scored["clinical_ai_governance_risk"].mean()),
                "max_governance_risk": float(scored["clinical_ai_governance_risk"].max()),
                **overall_metrics.iloc[0].to_dict(),
            }
        ]
    )

    records.to_csv(OUTPUT_DIR / "python_clinical_ai_prediction_logs.csv", index=False)
    overall_metrics.to_csv(OUTPUT_DIR / "python_clinical_ai_overall_metrics.csv", index=False)
    bins.to_csv(OUTPUT_DIR / "python_clinical_ai_calibration_bins.csv", index=False)
    subgroup_summary.to_csv(OUTPUT_DIR / "python_clinical_ai_subgroup_review.csv", index=False)
    scored.to_csv(OUTPUT_DIR / "python_clinical_ai_governance_scores.csv", index=False)
    governance_summary.to_csv(OUTPUT_DIR / "python_clinical_ai_governance_summary.csv", index=False)

    memo = f"""# Clinical AI Governance Memo

Cases reviewed: {int(governance_summary.loc[0, "cases_reviewed"])}
Decision threshold: {governance_summary.loc[0, "threshold"]:.2f}
Sensitivity: {governance_summary.loc[0, "sensitivity"]:.4f}
Specificity: {governance_summary.loc[0, "specificity"]:.4f}
Positive predictive value: {governance_summary.loc[0, "positive_predictive_value"]:.4f}
Negative predictive value: {governance_summary.loc[0, "negative_predictive_value"]:.4f}
Alert rate: {governance_summary.loc[0, "alert_rate"]:.4f}
Brier score: {governance_summary.loc[0, "brier_score"]:.4f}
Expected calibration error: {governance_summary.loc[0, "expected_calibration_error"]:.4f}
Subgroups requiring review: {int(governance_summary.loc[0, "subgroups_requiring_review"])}
Human-review recommended cases: {int(governance_summary.loc[0, "human_review_recommended_cases"])}
Mean governance risk: {governance_summary.loc[0, "mean_governance_risk"]:.4f}

Interpretation:
- Clinical AI should be evaluated beyond aggregate accuracy.
- Thresholds affect sensitivity, false negatives, false positives, and alert burden.
- Calibration and subgroup review are essential before and after deployment.
- Human review should be triggered by uncertainty, missingness, high-impact context, or equity concerns.
- This workflow is for systems analysis and does not provide medical advice.
"""

    (OUTPUT_DIR / "python_clinical_ai_governance_memo.md").write_text(memo)

    print(governance_summary.T)
    print(subgroup_summary.head(20))
    print(memo)


if __name__ == "__main__":
    main()
