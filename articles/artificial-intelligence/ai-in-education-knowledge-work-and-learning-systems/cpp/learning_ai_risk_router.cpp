/*
AI in Education, Knowledge Work, and Learning Systems

C++ example:
Learning-support routing and governance-risk scoring.

Educational systems workflow only.
Does not make student-specific educational decisions.

Compile:
c++ -std=c++17 learning_ai_risk_router.cpp -o learning_ai_risk_router

Run:
./learning_ai_risk_router
*/

#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct LearningRecord {
    std::string record_id;
    double learning_gain;
    double independent_transfer;
    double assistance_gap;
    double feedback_quality;
    double privacy_risk;
    double assessment_substitution_risk;
};

double governance_risk(const LearningRecord& record) {
    return std::min(
        1.0,
        0.24 * record.assessment_substitution_risk
        + 0.22 * record.privacy_risk
        + 0.20 * std::max(record.assistance_gap, 0.0)
        + 0.18 * (1.0 - record.feedback_quality)
        + 0.16 * std::max(0.0, 0.08 - record.learning_gain)
    );
}

std::string review_route(const LearningRecord& record) {
    double risk = governance_risk(record);

    if (record.privacy_risk > 0.50) {
        return "privacy_review";
    }

    if (record.assessment_substitution_risk > 0.55) {
        return "assessment_validity_review";
    }

    if (record.assistance_gap > 0.22) {
        return "independent_transfer_review";
    }

    if (record.feedback_quality < 0.40) {
        return "feedback_quality_review";
    }

    if (risk > 0.42) {
        return "learning_governance_review";
    }

    return "approved_for_controlled_learning_support";
}

int main() {
    std::vector<LearningRecord> records = {
        {"LEARN-001", 0.14, 0.68, 0.08, 0.72, 0.22, 0.24},
        {"LEARN-002", 0.02, 0.61, 0.09, 0.66, 0.24, 0.31},
        {"LEARN-003", 0.11, 0.46, 0.25, 0.62, 0.30, 0.34},
        {"LEARN-004", 0.15, 0.66, 0.10, 0.34, 0.20, 0.28},
        {"LEARN-005", 0.10, 0.60, 0.12, 0.60, 0.52, 0.32}
    };

    for (const auto& record : records) {
        std::cout
            << record.record_id
            << " governance_risk=" << governance_risk(record)
            << " route=" << review_route(record)
            << "\n";
    }

    return 0;
}
