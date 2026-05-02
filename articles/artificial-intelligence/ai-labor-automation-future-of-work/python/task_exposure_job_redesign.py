"""
Task exposure and job-redesign workflow.

This script creates synthetic task data and estimates:
- task-level AI exposure
- automation pressure
- augmentation potential
- protected human judgment needs
- job-redesign category
- job-level exposure summary

It is intended for educational and governance-design purposes, not production use.
"""

from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd


def create_task_inventory() -> pd.DataFrame:
    """Create a synthetic task inventory for an AI-exposed job."""
    return pd.DataFrame(
        {
            "task": [
                "document_summarization",
                "first_draft_generation",
                "client_context_interpretation",
                "quality_review",
                "routine_data_entry",
                "ethical_decision_review",
                "team_coordination",
                "training_and_mentoring",
                "source_verification",
                "final_accountability_review",
            ],
            "task_weight": [0.10, 0.12, 0.13, 0.12, 0.08, 0.10, 0.09, 0.10, 0.08, 0.08],
            "ai_capability": [0.85, 0.80, 0.45, 0.55, 0.90, 0.30, 0.40, 0.35, 0.60, 0.25],
            "routineness": [0.70, 0.60, 0.20, 0.35, 0.90, 0.10, 0.30, 0.20, 0.45, 0.10],
            "human_judgment_requirement": [0.35, 0.45, 0.90, 0.80, 0.20, 0.95, 0.75, 0.85, 0.85, 0.98],
            "task_value": [0.65, 0.70, 0.95, 0.85, 0.40, 0.95, 0.80, 0.85, 0.88, 0.98],
            "training_function": [0.40, 0.65, 0.85, 0.75, 0.35, 0.90, 0.70, 0.95, 0.80, 0.90],
            "worker_autonomy_importance": [0.40, 0.55, 0.90, 0.75, 0.25, 0.90, 0.80, 0.85, 0.80, 0.95],
        }
    )


def classify_task(row: pd.Series) -> str:
    """Classify a task into a redesign category."""
    if row["automation_pressure"] > 0.35 and row["human_judgment_requirement"] < 0.40:
        return "candidate_for_careful_automation"

    if row["augmentation_potential"] > 0.35:
        return "candidate_for_augmentation"

    if row["human_judgment_requirement"] > 0.80:
        return "protect_human_judgment"

    return "redesign_with_monitoring"


def score_tasks(tasks: pd.DataFrame) -> pd.DataFrame:
    """Score task exposure, automation pressure, and augmentation potential."""
    scored = tasks.copy()

    scored["automation_pressure"] = (
        scored["ai_capability"]
        * scored["routineness"]
        * (1 - scored["human_judgment_requirement"])
    )

    scored["augmentation_potential"] = (
        scored["ai_capability"]
        * scored["human_judgment_requirement"]
        * scored["task_value"]
    )

    scored["deskilling_risk"] = (
        scored["ai_capability"]
        * scored["training_function"]
        * (1 - scored["human_judgment_requirement"])
    )

    scored["worker_autonomy_risk"] = (
        scored["ai_capability"]
        * scored["worker_autonomy_importance"]
        * scored["routineness"]
    )

    scored["redesign_category"] = scored.apply(classify_task, axis=1)

    scored["governance_review_required"] = np.where(
        (scored["deskilling_risk"] >= 0.30)
        | (scored["worker_autonomy_risk"] >= 0.35)
        | (scored["human_judgment_requirement"] >= 0.85),
        1,
        0,
    )

    return scored


def summarize_job(scored_tasks: pd.DataFrame) -> pd.DataFrame:
    """Create job-level AI exposure and redesign summary."""
    return pd.DataFrame(
        {
            "job_exposure": [(scored_tasks["task_weight"] * scored_tasks["ai_capability"]).sum()],
            "weighted_automation_pressure": [
                (scored_tasks["task_weight"] * scored_tasks["automation_pressure"]).sum()
            ],
            "weighted_augmentation_potential": [
                (scored_tasks["task_weight"] * scored_tasks["augmentation_potential"]).sum()
            ],
            "weighted_deskilling_risk": [
                (scored_tasks["task_weight"] * scored_tasks["deskilling_risk"]).sum()
            ],
            "weighted_worker_autonomy_risk": [
                (scored_tasks["task_weight"] * scored_tasks["worker_autonomy_risk"]).sum()
            ],
            "tasks_candidate_for_automation": [
                (scored_tasks["redesign_category"] == "candidate_for_careful_automation").sum()
            ],
            "tasks_candidate_for_augmentation": [
                (scored_tasks["redesign_category"] == "candidate_for_augmentation").sum()
            ],
            "tasks_to_protect_human_judgment": [
                (scored_tasks["redesign_category"] == "protect_human_judgment").sum()
            ],
            "tasks_requiring_governance_review": [
                scored_tasks["governance_review_required"].sum()
            ],
        }
    )


def summarize_by_category(scored_tasks: pd.DataFrame) -> pd.DataFrame:
    """Summarize task scores by redesign category."""
    return (
        scored_tasks.groupby("redesign_category")
        .agg(
            tasks=("task", "count"),
            mean_ai_capability=("ai_capability", "mean"),
            mean_automation_pressure=("automation_pressure", "mean"),
            mean_augmentation_potential=("augmentation_potential", "mean"),
            mean_deskilling_risk=("deskilling_risk", "mean"),
            mean_worker_autonomy_risk=("worker_autonomy_risk", "mean"),
            review_required_share=("governance_review_required", "mean"),
        )
        .reset_index()
    )


def main() -> None:
    """Run task exposure and job redesign workflow."""
    article_dir = Path(__file__).resolve().parents[1]
    output_dir = article_dir / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    tasks = create_task_inventory()
    scored_tasks = score_tasks(tasks)
    job_summary = summarize_job(scored_tasks)
    category_summary = summarize_by_category(scored_tasks)

    scored_tasks.to_csv(output_dir / "task_exposure_redesign_scores.csv", index=False)
    job_summary.to_csv(output_dir / "job_redesign_summary.csv", index=False)
    category_summary.to_csv(output_dir / "task_redesign_category_summary.csv", index=False)

    print("\nTask exposure and redesign scores")
    print(scored_tasks.to_string(index=False))

    print("\nJob redesign summary")
    print(job_summary.to_string(index=False))

    print("\nTask redesign category summary")
    print(category_summary.to_string(index=False))


if __name__ == "__main__":
    main()
