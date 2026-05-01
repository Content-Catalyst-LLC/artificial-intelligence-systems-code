/*
Synthetic Data, Simulation, and AI Evaluation Environments

C++ example:
Evaluation-risk scoring and synthetic artifact routing.

Compile:
c++ -std=c++17 synthetic_evaluation_risk.cpp -o synthetic_evaluation_risk

Run:
./synthetic_evaluation_risk
*/

#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct SyntheticArtifactEvaluation {
    std::string artifact_id;
    double fidelity_risk;
    double utility_gap;
    double privacy_proximity_risk;
    double rare_case_coverage_gap;
    double sim_to_real_gap;
};

double evaluation_risk(const SyntheticArtifactEvaluation& record) {
    return std::min(
        1.0,
        0.24 * record.fidelity_risk
        + 0.20 * record.utility_gap
        + 0.24 * record.privacy_proximity_risk
        + 0.16 * record.rare_case_coverage_gap
        + 0.16 * record.sim_to_real_gap
    );
}

std::string review_route(const SyntheticArtifactEvaluation& record) {
    if (record.privacy_proximity_risk > 0.05) {
        return "privacy_review";
    }

    if (record.sim_to_real_gap > 0.18) {
        return "sim_to_real_validation";
    }

    if (record.rare_case_coverage_gap > 0.06) {
        return "scenario_coverage_review";
    }

    if (record.utility_gap > 0.05 || record.fidelity_risk > 0.25) {
        return "utility_and_fidelity_review";
    }

    return "controlled_use";
}

int main() {
    std::vector<SyntheticArtifactEvaluation> records = {
        {"SYN-001", 0.08, 0.02, 0.01, 0.02, 0.06},
        {"SYN-002", 0.28, 0.03, 0.02, 0.02, 0.05},
        {"SYN-003", 0.10, 0.07, 0.02, 0.01, 0.08},
        {"SYN-004", 0.06, 0.02, 0.08, 0.02, 0.04},
        {"SYN-005", 0.12, 0.03, 0.02, 0.08, 0.07},
        {"SYN-006", 0.13, 0.03, 0.02, 0.02, 0.22}
    };

    for (const auto& record : records) {
        std::cout
            << record.artifact_id
            << " evaluation_risk=" << evaluation_risk(record)
            << " route=" << review_route(record)
            << "\n";
    }

    return 0;
}
