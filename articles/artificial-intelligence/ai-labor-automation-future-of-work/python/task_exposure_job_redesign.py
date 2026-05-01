"""
Task exposure and job-redesign workflow.

This script creates synthetic task data and estimates:
- AI exposure
- automation pressure
- augmentation potential
- task redesign category
- job-level exposure summary

It is intended for educational and governance-design purposes, not production use.
"""

from pathlib import Path
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
            ],
            "task_weight": [0.12, 0.14, 0.16, 0.14, 0.10, 0.12, 0.10, 0.12],
            "ai_capability": [0.85, 0.80, 0.45, 0.55, 0.90, 0.30, 0.40, 0.35],
            "routineness": [0.70, 0.60, 0.20, 0.35, 0.90, 0.10, 0.30, 0.20],
            "human_judgment_requirement": [0.35, 0.45, 0.90, 0.80, 0.20, 0.95, 0.75, 0.85],
            "task_value": [0.65, 0.70, 0.95, 0.85, 0.40, 0.95, 0.80, 0.85],
        }
    )


def classify_task(row: pd.Series) -> str:
    """Classify task into a redesign category."""
    if row["automation_pressure"] > 0.35 and row["human_judgment_requirement"] < 0.40:
        return "candidate_for_careful_automation"

    if row["augmentation_potential"] > 0.35:
        return "candidate_for_augmentation"

    if row["human_judgment_requirement"] > 0.80:
        return "protect_human_judgment"

    return "redesign_with_monitoring"


def score_tasks(tasks: pd.DataFrame) -> pd.DataFrame:
    """Score task exposure, automation pressure, and augmentation potential."""
    tasks = tasks.copy()

    tasks["automation_pressure"] = (
        tasks["ai_capability"]
        * tasks["routineness"]
        * (1 - tasks["human_judgment_requirement"])
    )

    tasks["augmentation_potential"] = (
        tasks["ai_capability"]
        * tasks["human_judgment_requirement"]
        * tasks["task_value"]
    )

    tasks["redesign_category"] = tasks.apply(classify_task, axis=1)

    return tasks


def summarize_job(tasks: pd.DataFrame) -> pd.DataFrame:
    """Create job-level AI exposure and redesign summary."""
    return pd.DataFrame(
        {
            "job_exposure": [(tasks["task_weight"] * tasks["ai_capability"]).sum()],
            "mean_automation_pressure": [tasks["automation_pressure"].mean()],
            "mean_augmentation_potential": [tasks["augmentation_potential"].mean()],
            "tasks_candidate_for_automation": [
                (tasks["redesign_category"] == "candidate_for_careful_automation").sum()
            ],
            "tasks_candidate_for_augmentation": [
                (tasks["redesign_category"] == "candidate_for_augmentation").sum()
            ],
            "tasks_to_protect_human_judgment": [
                (tasks["redesign_category"] == "protect_human_judgment").sum()
            ],
        }
    )


def main() -> None:
    """Run task exposure and job redesign workflow."""
    article_dir = Path(__file__).resolve().parents[1]
    output_dir = article_dir / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    tasks = create_task_inventory()
    scored_tasks = score_tasks(tasks)
    summary = summarize_job(scored_tasks)

    scored_tasks.to_csv(output_dir / "task_exposure_redesign_scores.csv", index=False)
    summary.to_csv(output_dir / "job_redesign_summary.csv", index=False)

    print(scored_tasks)
    print(summary)


if __name__ == "__main__":
    main()
