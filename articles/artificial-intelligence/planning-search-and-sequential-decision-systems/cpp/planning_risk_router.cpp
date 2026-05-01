/*
Planning, Search, and Sequential Decision Systems

C++ example:
Planning-risk scoring and action routing.

Compile:
c++ -std=c++17 planning_risk_router.cpp -o planning_risk_router

Run:
./planning_risk_router
*/

#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct CandidatePlan {
    std::string plan_id;
    double plan_cost;
    double uncertainty_risk;
    double constraint_violation_risk;
    double irreversibility_risk;
    double governance_readiness;
};

double planning_risk(const CandidatePlan& plan) {
    return std::min(
        1.0,
        0.30 * plan.plan_cost
        + 0.25 * plan.uncertainty_risk
        + 0.25 * plan.constraint_violation_risk
        + 0.20 * plan.irreversibility_risk
    );
}

std::string review_route(const CandidatePlan& plan) {
    if (plan.irreversibility_risk > 0.15) {
        return "human_approval_required";
    }

    if (plan.constraint_violation_risk > 0.20) {
        return "constraint_review";
    }

    if (plan.uncertainty_risk > 0.45) {
        return "collect_more_information";
    }

    if (plan.governance_readiness < 0.65) {
        return "traceability_review";
    }

    if (planning_risk(plan) > 0.28) {
        return "planning_governance_review";
    }

    return "approved_for_execution";
}

int main() {
    std::vector<CandidatePlan> plans = {
        {"PLAN-001", 0.20, 0.10, 0.03, 0.02, 0.88},
        {"PLAN-002", 0.45, 0.52, 0.05, 0.04, 0.82},
        {"PLAN-003", 0.35, 0.12, 0.24, 0.02, 0.75},
        {"PLAN-004", 0.22, 0.14, 0.04, 0.21, 0.80},
        {"PLAN-005", 0.24, 0.12, 0.03, 0.02, 0.58}
    };

    for (const auto& plan : plans) {
        std::cout
            << plan.plan_id
            << " planning_risk=" << planning_risk(plan)
            << " route=" << review_route(plan)
            << "\n";
    }

    return 0;
}
