"""
Calibration, Uncertainty, and Probability in AI Systems

Python workflow:
- Simulate probabilistic predictions and observed labels.
- Compute calibration diagnostics, Brier score, negative log likelihood,
  entropy, uncertainty flags, and bin-level reliability summaries.
- Score governance risk for probability-based AI systems.
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


def simulate_prediction_logs(n: int = 4500) -> pd.DataFrame:
    """Create synthetic prediction logs with imperfect calibration."""
    source = rng.choice(
        ["standard_queue", "new_source", "high_variance_source", "manual_upload"],
        size=n,
        p=[0.55, 0.18, 0.17, 0.10],
    )

    feature_a = rng.normal(0, 1, n)
    feature_b = rng.normal(0, 1, n)
    source_shift = np.select(
        [
            source == "standard_queue",
            source == "new_source",
            source == "high_variance_source",
            source == "manual_upload",
        ],
        [0.0, 0.35, -0.20, 0.15],
        default=0.0,
    )

    true_logit = 0.9 * feature_a - 0.6 * feature_b + source_shift
    true_probability = sigmoid(true_logit)
    label = rng.binomial(1, true_probability)

    raw_model_logit = 1.55 * true_logit + rng.normal(0, 0.55, n)
    predicted_probability = sigmoid(raw_model_logit)

    entropy = -(
        predicted_probability * np.log(np.clip(predicted_probability, 1e-9, 1))
        + (1 - predicted_probability) * np.log(np.clip(1 - predicted_probability, 1e-9, 1))
    )

    uncertainty_zone = np.select(
        [
            predicted_probability < 0.30,
            predicted_probability <= 0.75,
            predicted_probability > 0.75,
        ],
        [
            "standard_processing",
            "human_review",
            "urgent_review",
        ],
        default="human_review",
    )

    return pd.DataFrame(
        {
            "case_id": [f"CASE-{i:05d}" for i in range(n)],
            "source": source,
            "predicted_probability": predicted_probability,
            "true_probability": true_probability,
            "label": label,
            "entropy": entropy,
            "uncertainty_zone": uncertainty_zone,
        }
    )


def calibration_bins(records: pd.DataFrame, bins: int = 10) -> pd.DataFrame:
    """Create bin-level calibration summary."""
    data = records.copy()
    data["probability_bin"] = pd.cut(
        data["predicted_probability"],
        bins=np.linspace(0, 1, bins + 1),
        include_lowest=True,
    )

    grouped = (
        data.groupby("probability_bin", observed=True)
        .agg(
            cases=("case_id", "count"),
            mean_confidence=("predicted_probability", "mean"),
            observed_rate=("label", "mean"),
            mean_entropy=("entropy", "mean"),
        )
        .reset_index()
    )

    grouped["absolute_calibration_gap"] = (
        grouped["observed_rate"] - grouped["mean_confidence"]
    ).abs()

    grouped["weighted_calibration_gap"] = (
        grouped["cases"] / grouped["cases"].sum()
    ) * grouped["absolute_calibration_gap"]

    return grouped


def compute_metrics(records: pd.DataFrame) -> dict[str, float]:
    """Compute core probabilistic evaluation metrics."""
    p = np.clip(records["predicted_probability"].to_numpy(), 1e-9, 1 - 1e-9)
    y = records["label"].to_numpy()

    brier = float(np.mean((p - y) ** 2))
    nll = float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))

    bins = calibration_bins(records)
    ece = float(bins["weighted_calibration_gap"].sum())

    predicted_label = (p >= 0.5).astype(int)
    accuracy = float(np.mean(predicted_label == y))

    return {
        "brier_score": brier,
        "negative_log_likelihood": nll,
        "expected_calibration_error": ece,
        "accuracy": accuracy,
        "mean_entropy": float(records["entropy"].mean()),
        "urgent_review_rate": float((records["uncertainty_zone"] == "urgent_review").mean()),
        "human_review_rate": float((records["uncertainty_zone"] == "human_review").mean()),
    }


def summarize_slices(records: pd.DataFrame) -> pd.DataFrame:
    """Summarize calibration and uncertainty by source slice."""
    rows = []

    for source, subset in records.groupby("source"):
        metrics = compute_metrics(subset)
        rows.append({"source": source, "cases": len(subset), **metrics})

    summary = pd.DataFrame(rows)
    summary["calibration_review_required"] = (
        (summary["expected_calibration_error"] > 0.08)
        | (summary["brier_score"] > 0.22)
        | (summary["negative_log_likelihood"] > 0.70)
    )

    return summary.sort_values("expected_calibration_error", ascending=False)


def score_governance_risk(records: pd.DataFrame) -> pd.DataFrame:
    """Score calibration and uncertainty governance risk for records."""
    scored = records.copy()

    scored["high_confidence_error_risk"] = np.where(
        scored["predicted_probability"] > 0.85,
        1 - scored["true_probability"],
        0.0,
    )

    scored["uncertainty_review_required"] = (
        (scored["entropy"] > 0.62)
        | (scored["source"].isin(["new_source", "high_variance_source"]))
        | (scored["predicted_probability"].between(0.45, 0.60))
    )

    scored["probability_governance_risk"] = np.clip(
        0.35 * scored["entropy"]
        + 0.30 * scored["high_confidence_error_risk"]
        + 0.20 * scored["source"].isin(["new_source", "high_variance_source"]).astype(float)
        + 0.15 * scored["predicted_probability"].between(0.45, 0.60).astype(float),
        0,
        1,
    )

    return scored.sort_values("probability_governance_risk", ascending=False)


def main() -> None:
    """Run calibration and uncertainty review."""
    records = simulate_prediction_logs()
    bins = calibration_bins(records)
    metrics = compute_metrics(records)
    slice_summary = summarize_slices(records)
    scored = score_governance_risk(records)

    governance_summary = pd.DataFrame(
        [
            {
                "cases_reviewed": len(records),
                **metrics,
                "slice_review_count": int(slice_summary["calibration_review_required"].sum()),
                "uncertainty_review_cases": int(scored["uncertainty_review_required"].sum()),
                "high_probability_high_risk_cases": int((scored["high_confidence_error_risk"] > 0.25).sum()),
                "mean_probability_governance_risk": scored["probability_governance_risk"].mean(),
            }
        ]
    )

    records.to_csv(OUTPUT_DIR / "python_prediction_logs.csv", index=False)
    bins.to_csv(OUTPUT_DIR / "python_calibration_bins.csv", index=False)
    slice_summary.to_csv(OUTPUT_DIR / "python_slice_calibration_summary.csv", index=False)
    scored.to_csv(OUTPUT_DIR / "python_probability_governance_scores.csv", index=False)
    governance_summary.to_csv(OUTPUT_DIR / "python_calibration_governance_summary.csv", index=False)

    memo = f"""# Calibration and Uncertainty Governance Memo

Cases reviewed: {int(governance_summary.loc[0, "cases_reviewed"])}
Accuracy: {governance_summary.loc[0, "accuracy"]:.4f}
Brier score: {governance_summary.loc[0, "brier_score"]:.4f}
Negative log likelihood: {governance_summary.loc[0, "negative_log_likelihood"]:.4f}
Expected calibration error: {governance_summary.loc[0, "expected_calibration_error"]:.4f}
Mean entropy: {governance_summary.loc[0, "mean_entropy"]:.4f}
Human-review rate: {governance_summary.loc[0, "human_review_rate"]:.4f}
Urgent-review rate: {governance_summary.loc[0, "urgent_review_rate"]:.4f}
Slices requiring calibration review: {int(governance_summary.loc[0, "slice_review_count"])}
Cases requiring uncertainty review: {int(governance_summary.loc[0, "uncertainty_review_cases"])}
Mean probability governance risk: {governance_summary.loc[0, "mean_probability_governance_risk"]:.4f}

Interpretation:
- Accuracy alone is insufficient for probability-based AI systems.
- Calibration should be reviewed globally and by operational slice.
- High entropy, new sources, and uncertain decision zones should trigger review.
- Threshold policies should be tied to calibrated probabilities, uncertainty, and decision consequences.
"""

    (OUTPUT_DIR / "python_calibration_governance_memo.md").write_text(memo)

    print(governance_summary.T)
    print(slice_summary)
    print(bins)
    print(memo)


if __name__ == "__main__":
    main()
