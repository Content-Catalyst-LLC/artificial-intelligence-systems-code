"""
AI Agents, Tool Use, and Workflow Automation

Python workflow:
- agent workflow evaluation simulation
- task success, tool selection, argument validity, permission compliance,
  error recovery, safety, auditability, and human-review scoring
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


def simulate_agent_workflows(n: int = 260) -> pd.DataFrame:
    """Create synthetic agent workflow evaluation records."""
    workflow_types = [
        "research_summary",
        "database_query",
        "code_execution",
        "ticket_creation",
        "calendar_coordination",
        "document_update",
        "multi_step_operations",
    ]

    tool_risk_levels = ["read_only", "compute", "write", "external_action", "sensitive"]

    rows = []

    for i in range(n):
        workflow_type = rng.choice(workflow_types)

        tool_risk = rng.choice(
            tool_risk_levels,
            p=[0.40, 0.25, 0.18, 0.09, 0.08],
        )

        steps = int(rng.integers(2, 18))
        tool_calls = int(rng.integers(1, max(2, steps + 1)))

        confirmation_required = int(tool_risk in ["write", "external_action", "sensitive"])
        confirmation_obtained = int(
            confirmation_required == 0 or rng.choice([0, 1], p=[0.12, 0.88]) == 1
        )

        rows.append(
            {
                "eval_id": f"AGENT-EVAL-{i:03d}",
                "workflow_type": workflow_type,
                "tool_risk": tool_risk,
                "steps": steps,
                "tool_calls": tool_calls,
                "task_success": float(rng.uniform(0.45, 1.0)),
                "tool_selection_score": float(rng.uniform(0.45, 1.0)),
                "argument_validity": float(rng.uniform(0.50, 1.0)),
                "permission_compliance": float(rng.uniform(0.60, 1.0)),
                "error_recovery_score": float(rng.uniform(0.35, 1.0)),
                "safety_score": float(rng.uniform(0.55, 1.0)),
                "auditability_score": float(rng.uniform(0.55, 1.0)),
                "human_review_score": float(rng.uniform(0.45, 1.0)),
                "confirmation_required": confirmation_required,
                "confirmation_obtained": confirmation_obtained,
                "denied_action_attempt": int(rng.choice([0, 1], p=[0.88, 0.12])),
                "prompt_injection_exposure": int(rng.choice([0, 1], p=[0.86, 0.14])),
                "latency_seconds": float(rng.gamma(shape=2.6, scale=1.4)),
                "token_cost_index": float(rng.uniform(0.05, 1.0)),
            }
        )

    return pd.DataFrame(rows)


def score_agent_workflows(records: pd.DataFrame) -> pd.DataFrame:
    """Score agent workflows for performance and governance risk."""
    scored = records.copy()

    scored["execution_quality_score"] = (
        0.25 * scored["task_success"]
        + 0.20 * scored["tool_selection_score"]
        + 0.20 * scored["argument_validity"]
        + 0.15 * scored["error_recovery_score"]
        + 0.10 * scored["auditability_score"]
        + 0.10 * scored["human_review_score"]
    )

    scored["safety_governance_score"] = (
        0.30 * scored["safety_score"]
        + 0.25 * scored["permission_compliance"]
        + 0.20 * scored["auditability_score"]
        + 0.15 * scored["human_review_score"]
        + 0.10 * scored["argument_validity"]
    )

    risk_weight = scored["tool_risk"].map(
        {
            "read_only": 0.05,
            "compute": 0.15,
            "write": 0.30,
            "external_action": 0.45,
            "sensitive": 0.55,
        }
    )

    scored["workflow_complexity_index"] = np.clip(
        (scored["steps"] / 20) + (scored["tool_calls"] / 20),
        0,
        1.5,
    )

    scored["operational_cost_index"] = np.clip(
        (scored["latency_seconds"] / 15) + scored["token_cost_index"],
        0,
        1.5,
    )

    scored["agent_system_risk"] = (
        0.20 * (1 - scored["execution_quality_score"])
        + 0.25 * (1 - scored["safety_governance_score"])
        + 0.15 * risk_weight
        + 0.10 * scored["workflow_complexity_index"]
        + 0.10 * scored["operational_cost_index"]
        + 0.10 * scored["denied_action_attempt"]
        + 0.10 * scored["prompt_injection_exposure"]
    )

    scored["review_required"] = (
        (scored["agent_system_risk"] > 0.42)
        | (scored["tool_risk"].isin(["external_action", "sensitive"]))
        | (scored["task_success"] < 0.65)
        | (scored["argument_validity"] < 0.70)
        | (scored["permission_compliance"] < 0.80)
        | (scored["safety_score"] < 0.75)
        | (scored["denied_action_attempt"] == 1)
        | (scored["prompt_injection_exposure"] == 1)
        | ((scored["confirmation_required"] == 1) & (scored["confirmation_obtained"] == 0))
    )

    scored["deployment_recommendation"] = np.select(
        [
            scored["agent_system_risk"] > 0.58,
            scored["review_required"],
            scored["execution_quality_score"] > 0.84,
        ],
        [
            "pause_for_agent_governance_review",
            "approve_only_after_tool_and_permission_review",
            "candidate_for_controlled_deployment",
        ],
        default="continue_evaluation",
    )

    return scored.sort_values("agent_system_risk", ascending=False)


def summarize_by_workflow(scored: pd.DataFrame) -> pd.DataFrame:
    """Summarize agent performance and risk by workflow type."""
    return (
        scored.groupby("workflow_type")
        .agg(
            evaluations=("eval_id", "count"),
            mean_steps=("steps", "mean"),
            mean_tool_calls=("tool_calls", "mean"),
            mean_execution_quality=("execution_quality_score", "mean"),
            mean_safety_governance=("safety_governance_score", "mean"),
            mean_agent_system_risk=("agent_system_risk", "mean"),
            review_rate=("review_required", "mean"),
            denied_action_rate=("denied_action_attempt", "mean"),
            prompt_injection_exposure_rate=("prompt_injection_exposure", "mean"),
        )
        .reset_index()
        .sort_values("mean_agent_system_risk", ascending=False)
    )


def main() -> None:
    """Run agent evaluation and governance review."""
    records = simulate_agent_workflows()
    scored = score_agent_workflows(records)
    workflow_summary = summarize_by_workflow(scored)

    governance_summary = pd.DataFrame(
        [
            {
                "evaluations_reviewed": len(scored),
                "review_required": int(scored["review_required"].sum()),
                "sensitive_or_external_action_cases": int(
                    scored["tool_risk"].isin(["external_action", "sensitive"]).sum()
                ),
                "failed_confirmation_cases": int(
                    ((scored["confirmation_required"] == 1) & (scored["confirmation_obtained"] == 0)).sum()
                ),
                "denied_action_attempts": int(scored["denied_action_attempt"].sum()),
                "prompt_injection_exposures": int(scored["prompt_injection_exposure"].sum()),
                "mean_execution_quality": scored["execution_quality_score"].mean(),
                "mean_safety_governance": scored["safety_governance_score"].mean(),
                "mean_agent_system_risk": scored["agent_system_risk"].mean(),
            }
        ]
    )

    records.to_csv(OUTPUT_DIR / "python_agent_workflow_records.csv", index=False)
    scored.to_csv(OUTPUT_DIR / "python_agent_system_risk_scores.csv", index=False)
    workflow_summary.to_csv(OUTPUT_DIR / "python_agent_workflow_summary.csv", index=False)
    governance_summary.to_csv(OUTPUT_DIR / "python_agent_governance_summary.csv", index=False)

    memo = f"""# AI Agent Governance Memo

Evaluations reviewed: {int(governance_summary.loc[0, "evaluations_reviewed"])}
Review required: {int(governance_summary.loc[0, "review_required"])}
Sensitive or external-action cases: {int(governance_summary.loc[0, "sensitive_or_external_action_cases"])}
Failed confirmation cases: {int(governance_summary.loc[0, "failed_confirmation_cases"])}
Denied action attempts: {int(governance_summary.loc[0, "denied_action_attempts"])}
Prompt-injection exposures: {int(governance_summary.loc[0, "prompt_injection_exposures"])}
Mean execution quality: {governance_summary.loc[0, "mean_execution_quality"]:.4f}
Mean safety/governance score: {governance_summary.loc[0, "mean_safety_governance"]:.4f}
Mean agent system risk: {governance_summary.loc[0, "mean_agent_system_risk"]:.4f}

Interpretation:
- Agentic systems should be evaluated by workflow, tool risk, permissions, recovery, and auditability.
- Write, sensitive, and external-action tools require stronger confirmation and review.
- Prompt-injection exposure and denied action attempts should trigger governance review.
- Task success alone is not sufficient evidence of safe deployment.
"""

    (OUTPUT_DIR / "python_agent_governance_memo.md").write_text(memo)

    print(governance_summary.T)
    print(workflow_summary)
    print(scored.head(10))
    print(memo)


if __name__ == "__main__":
    main()
