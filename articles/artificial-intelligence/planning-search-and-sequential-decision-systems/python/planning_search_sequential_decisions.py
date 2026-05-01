"""
Planning, Search, and Sequential Decision Systems

Python workflow:
- Build a simple planning environment.
- Run A* search over a grid with risky and blocked cells.
- Evaluate plan cost, uncertainty, constraint risk, reversibility, and governance risk.
- Produce governance-ready summaries.
"""

from __future__ import annotations

from dataclasses import dataclass
from heapq import heappop, heappush
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

import numpy as np
import pandas as pd


ARTICLE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ARTICLE_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

RANDOM_SEED = 42
rng = np.random.default_rng(RANDOM_SEED)

GridPoint = Tuple[int, int]


@dataclass(frozen=True)
class PlanningEnvironment:
    """Grid environment with blocked cells, risky cells, and uncertain cells."""
    width: int
    height: int
    blocked: frozenset[GridPoint]
    risky: frozenset[GridPoint]
    uncertain: frozenset[GridPoint]
    irreversible: frozenset[GridPoint]


def neighbors(point: GridPoint, environment: PlanningEnvironment) -> Iterable[GridPoint]:
    """Generate valid neighboring grid points."""
    x, y = point

    candidates = [
        (x + 1, y),
        (x - 1, y),
        (x, y + 1),
        (x, y - 1),
    ]

    for candidate in candidates:
        cx, cy = candidate
        in_bounds = 0 <= cx < environment.width and 0 <= cy < environment.height

        if in_bounds and candidate not in environment.blocked:
            yield candidate


def heuristic(point: GridPoint, goal: GridPoint) -> float:
    """Manhattan-distance heuristic."""
    return abs(point[0] - goal[0]) + abs(point[1] - goal[1])


def step_cost(point: GridPoint, environment: PlanningEnvironment) -> float:
    """Cost of entering a grid cell."""
    cost = 1.0

    if point in environment.risky:
        cost += 2.0

    if point in environment.uncertain:
        cost += 1.25

    if point in environment.irreversible:
        cost += 3.0

    return cost


def reconstruct_path(came_from: Dict[GridPoint, GridPoint], current: GridPoint) -> List[GridPoint]:
    """Reconstruct a path from parent pointers."""
    path = [current]

    while current in came_from:
        current = came_from[current]
        path.append(current)

    path.reverse()
    return path


def astar_search(
    start: GridPoint,
    goal: GridPoint,
    environment: PlanningEnvironment,
    risk_weight: float = 1.0,
) -> Optional[List[GridPoint]]:
    """Run A* search with a configurable risk penalty."""
    frontier: list[tuple[float, GridPoint]] = []
    heappush(frontier, (0.0, start))

    came_from: Dict[GridPoint, GridPoint] = {}
    cost_so_far: Dict[GridPoint, float] = {start: 0.0}

    while frontier:
        _, current = heappop(frontier)

        if current == goal:
            return reconstruct_path(came_from, current)

        for next_point in neighbors(current, environment):
            risk_penalty = 0.0

            if next_point in environment.risky:
                risk_penalty += 2.0 * risk_weight

            if next_point in environment.uncertain:
                risk_penalty += 1.25 * risk_weight

            if next_point in environment.irreversible:
                risk_penalty += 3.0 * risk_weight

            new_cost = cost_so_far[current] + 1.0 + risk_penalty

            if next_point not in cost_so_far or new_cost < cost_so_far[next_point]:
                cost_so_far[next_point] = new_cost
                priority = new_cost + heuristic(next_point, goal)
                heappush(frontier, (priority, next_point))
                came_from[next_point] = current

    return None


def evaluate_plan(path: List[GridPoint], environment: PlanningEnvironment, plan_name: str) -> dict[str, object]:
    """Evaluate plan cost, risk, uncertainty, reversibility, and governance status."""
    if not path:
        return {
            "plan_name": plan_name,
            "feasible": False,
            "steps": 0,
            "path_cost": np.nan,
            "risky_steps": np.nan,
            "uncertain_steps": np.nan,
            "irreversible_steps": np.nan,
            "planning_risk": 1.0,
            "review_required": True,
            "recommended_action": "reject_infeasible_plan",
        }

    risky_steps = sum(point in environment.risky for point in path)
    uncertain_steps = sum(point in environment.uncertain for point in path)
    irreversible_steps = sum(point in environment.irreversible for point in path)
    total_cost = sum(step_cost(point, environment) for point in path[1:])

    normalized_cost = min(total_cost / 30, 1.0)
    uncertainty_risk = min(uncertain_steps / max(len(path), 1), 1.0)
    constraint_risk = min(risky_steps / max(len(path), 1), 1.0)
    irreversibility_risk = min(irreversible_steps / max(len(path), 1), 1.0)

    planning_risk = (
        0.30 * normalized_cost
        + 0.25 * uncertainty_risk
        + 0.25 * constraint_risk
        + 0.20 * irreversibility_risk
    )

    review_required = (
        planning_risk > 0.25
        or risky_steps > 0
        or uncertain_steps >= 3
        or irreversible_steps > 0
    )

    recommended_action = "approve_for_execution"

    if irreversible_steps > 0:
        recommended_action = "require_human_approval_before_irreversible_action"
    elif risky_steps > 0:
        recommended_action = "route_to_safety_review"
    elif uncertain_steps >= 3:
        recommended_action = "collect_more_information_before_execution"
    elif planning_risk > 0.25:
        recommended_action = "review_plan_tradeoffs"

    return {
        "plan_name": plan_name,
        "feasible": True,
        "steps": len(path) - 1,
        "path_cost": total_cost,
        "risky_steps": risky_steps,
        "uncertain_steps": uncertain_steps,
        "irreversible_steps": irreversible_steps,
        "planning_risk": planning_risk,
        "review_required": review_required,
        "recommended_action": recommended_action,
        "path": " -> ".join([f"({x},{y})" for x, y in path]),
    }


def create_environment() -> PlanningEnvironment:
    """Create a small planning environment."""
    blocked = frozenset({(2, 1), (2, 2), (2, 3), (5, 4), (6, 4)})
    risky = frozenset({(3, 3), (4, 3), (5, 3), (7, 2)})
    uncertain = frozenset({(1, 4), (3, 4), (4, 4), (6, 2), (6, 3)})
    irreversible = frozenset({(7, 4)})

    return PlanningEnvironment(
        width=9,
        height=6,
        blocked=blocked,
        risky=risky,
        uncertain=uncertain,
        irreversible=irreversible,
    )


def main() -> None:
    """Run planning, search, and governance review."""
    environment = create_environment()
    start = (0, 0)
    goal = (8, 5)

    candidate_configs = [
        ("cost_prioritized_plan", 0.25),
        ("balanced_plan", 1.0),
        ("risk_averse_plan", 2.5),
    ]

    evaluations = []

    for plan_name, risk_weight in candidate_configs:
        path = astar_search(start, goal, environment, risk_weight=risk_weight)
        evaluations.append(evaluate_plan(path or [], environment, plan_name))

    evaluation_table = pd.DataFrame(evaluations)

    governance_summary = pd.DataFrame(
        [
            {
                "plans_reviewed": len(evaluation_table),
                "feasible_plans": int(evaluation_table["feasible"].sum()),
                "plans_requiring_review": int(evaluation_table["review_required"].sum()),
                "minimum_planning_risk": float(evaluation_table["planning_risk"].min()),
                "maximum_planning_risk": float(evaluation_table["planning_risk"].max()),
                "minimum_path_cost": float(evaluation_table["path_cost"].min()),
            }
        ]
    )

    evaluation_table.to_csv(OUTPUT_DIR / "python_planning_search_evaluations.csv", index=False)
    governance_summary.to_csv(OUTPUT_DIR / "python_planning_governance_summary.csv", index=False)

    memo = f"""# Planning, Search, and Sequential Decision Governance Memo

Plans reviewed: {int(governance_summary.loc[0, "plans_reviewed"])}
Feasible plans: {int(governance_summary.loc[0, "feasible_plans"])}
Plans requiring review: {int(governance_summary.loc[0, "plans_requiring_review"])}
Minimum planning risk: {governance_summary.loc[0, "minimum_planning_risk"]:.4f}
Maximum planning risk: {governance_summary.loc[0, "maximum_planning_risk"]:.4f}
Minimum path cost: {governance_summary.loc[0, "minimum_path_cost"]:.4f}

Interpretation:
- Search efficiency is not the same as safe planning.
- Candidate plans should be evaluated for cost, uncertainty, constraints, and reversibility.
- Irreversible or high-impact actions should trigger human approval.
- Planning systems should preserve traces for audit, monitoring, and rollback.
"""

    (OUTPUT_DIR / "python_planning_governance_memo.md").write_text(memo)

    print(evaluation_table)
    print(governance_summary.T)
    print(memo)


if __name__ == "__main__":
    main()
