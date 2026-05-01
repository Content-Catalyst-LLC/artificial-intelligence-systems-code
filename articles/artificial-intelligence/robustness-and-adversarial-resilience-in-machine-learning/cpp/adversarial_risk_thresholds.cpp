/*
Robustness and Adversarial Resilience in Machine Learning

C++ example:
Adversarial risk scoring and threshold-based escalation.

Compile:
c++ -std=c++17 adversarial_risk_thresholds.cpp -o adversarial_risk_thresholds

Run:
./adversarial_risk_thresholds
*/

#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct RobustnessCase {
    std::string case_id;
    double clean_performance;
    double adversarial_performance;
    double attack_success_rate;
    double containment_score;
    double recovery_score;
    int incident_severity;
};

double risk_score(const RobustnessCase& record) {
    double adversarial_drop = std::max(0.0, record.clean_performance - record.adversarial_performance);
    double severity_score = static_cast<double>(record.incident_severity) / 5.0;

    return 0.30 * adversarial_drop
        + 0.30 * record.attack_success_rate
        + 0.15 * (1.0 - record.containment_score)
        + 0.15 * (1.0 - record.recovery_score)
        + 0.10 * severity_score;
}

std::string escalation_level(const RobustnessCase& record) {
    double risk = risk_score(record);
    double adversarial_drop = std::max(0.0, record.clean_performance - record.adversarial_performance);

    if (risk > 0.45 || record.incident_severity >= 4) {
        return "incident_review";
    }

    if (risk > 0.30 || adversarial_drop > 0.22 || record.attack_success_rate > 0.30) {
        return "action_required";
    }

    if (risk > 0.20) {
        return "warning";
    }

    return "normal";
}

int main() {
    std::vector<RobustnessCase> cases = {
        {"CASE-001", 0.92, 0.86, 0.08, 0.88, 0.84, 1},
        {"CASE-002", 0.91, 0.62, 0.22, 0.82, 0.80, 2},
        {"CASE-003", 0.89, 0.79, 0.42, 0.85, 0.77, 2},
        {"CASE-004", 0.93, 0.84, 0.12, 0.54, 0.79, 2},
        {"CASE-005", 0.88, 0.80, 0.14, 0.76, 0.52, 2},
        {"CASE-006", 0.90, 0.82, 0.18, 0.80, 0.74, 4}
    };

    for (const auto& record : cases) {
        std::cout
            << record.case_id
            << " risk=" << risk_score(record)
            << " escalation=" << escalation_level(record)
            << "\n";
    }

    return 0;
}
