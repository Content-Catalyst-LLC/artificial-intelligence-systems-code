/*
AI in Health, Medicine, and Clinical Decision Support

C++ example:
Clinical decision support routing and governance-risk scoring.

Educational systems workflow only.
Not medical advice.

Compile:
c++ -std=c++17 clinical_ai_risk_router.cpp -o clinical_ai_risk_router

Run:
./clinical_ai_risk_router
*/

#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct ClinicalCase {
    std::string case_id;
    double predicted_probability;
    double missingness_score;
    bool intensive_care_context;
    bool high_age_band;
    bool language_access_flag;
};

double governance_risk(const ClinicalCase& record, double threshold) {
    bool uncertainty_zone = record.predicted_probability >= threshold - 0.05 &&
                            record.predicted_probability <= threshold + 0.05;

    return std::min(
        1.0,
        0.25 * record.missingness_score
        + 0.25 * static_cast<double>(uncertainty_zone)
        + 0.20 * static_cast<double>(record.intensive_care_context)
        + 0.15 * static_cast<double>(record.high_age_band)
        + 0.15 * static_cast<double>(record.language_access_flag)
    );
}

std::string review_route(const ClinicalCase& record, double threshold) {
    double risk = governance_risk(record, threshold);
    bool alert = record.predicted_probability >= threshold;
    bool uncertainty_zone = record.predicted_probability >= threshold - 0.05 &&
                            record.predicted_probability <= threshold + 0.05;

    if (risk > 0.45 || record.missingness_score > 0.35) {
        return "human_review_required";
    }

    if (uncertainty_zone) {
        return "review_due_to_threshold_uncertainty";
    }

    if (alert) {
        return "clinical_workflow_alert";
    }

    return "standard_monitoring";
}

int main() {
    double threshold = 0.25;

    std::vector<ClinicalCase> cases = {
        {"CLIN-001", 0.18, 0.08, false, false, false},
        {"CLIN-002", 0.26, 0.12, false, false, true},
        {"CLIN-003", 0.33, 0.41, true, false, false},
        {"CLIN-004", 0.24, 0.18, true, true, true},
        {"CLIN-005", 0.52, 0.09, false, false, false}
    };

    for (const auto& record : cases) {
        std::cout
            << record.case_id
            << " governance_risk=" << governance_risk(record, threshold)
            << " route=" << review_route(record, threshold)
            << "\n";
    }

    return 0;
}
