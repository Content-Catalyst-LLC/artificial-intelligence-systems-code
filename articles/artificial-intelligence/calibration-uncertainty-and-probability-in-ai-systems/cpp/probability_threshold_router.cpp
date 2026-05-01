/*
Calibration, Uncertainty, and Probability in AI Systems

C++ example:
Probability threshold routing and calibration-risk scoring.

Compile:
c++ -std=c++17 probability_threshold_router.cpp -o probability_threshold_router

Run:
./probability_threshold_router
*/

#include <algorithm>
#include <cmath>
#include <iostream>
#include <string>
#include <vector>

struct PredictionCase {
    std::string case_id;
    double predicted_probability;
    double entropy;
    double slice_calibration_gap;
    bool new_source;
};

std::string route_case(const PredictionCase& record) {
    if (record.entropy > 0.62 || record.slice_calibration_gap > 0.08 || record.new_source) {
        return "human_review";
    }

    if (record.predicted_probability < 0.30) {
        return "standard_processing";
    }

    if (record.predicted_probability <= 0.75) {
        return "human_review";
    }

    return "urgent_review";
}

double governance_risk(const PredictionCase& record) {
    double threshold_uncertainty = (record.predicted_probability >= 0.45 && record.predicted_probability <= 0.60) ? 1.0 : 0.0;
    double source_risk = record.new_source ? 1.0 : 0.0;

    return std::min(
        1.0,
        0.35 * record.entropy
        + 0.30 * record.slice_calibration_gap
        + 0.20 * threshold_uncertainty
        + 0.15 * source_risk
    );
}

int main() {
    std::vector<PredictionCase> cases = {
        {"CASE-001", 0.22, 0.50, 0.03, false},
        {"CASE-002", 0.52, 0.68, 0.04, false},
        {"CASE-003", 0.82, 0.41, 0.10, false},
        {"CASE-004", 0.78, 0.39, 0.04, true},
        {"CASE-005", 0.91, 0.28, 0.03, false}
    };

    for (const auto& record : cases) {
        std::cout
            << record.case_id
            << " route=" << route_case(record)
            << " governance_risk=" << governance_risk(record)
            << "\n";
    }

    return 0;
}
