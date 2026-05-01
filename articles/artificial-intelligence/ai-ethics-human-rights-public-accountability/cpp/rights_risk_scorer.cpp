// High-throughput rights-risk scoring example.

#include <iostream>
#include <vector>
#include <string>

double residual_rights_risk(
    double harm_probability,
    double harm_impact,
    double vulnerability_exposure,
    double institutional_power,
    double governance_control_strength
) {
    double inherent =
        0.30 * harm_probability +
        0.30 * harm_impact +
        0.20 * vulnerability_exposure +
        0.20 * institutional_power;

    return inherent * (1.0 - governance_control_strength);
}

std::string risk_band(double score) {
    if (score < 0.20) {
        return "low";
    } else if (score < 0.35) {
        return "moderate";
    } else {
        return "high";
    }
}

int main() {
    std::vector<std::string> use_cases = {
        "public_benefits_review",
        "student_risk_prediction",
        "hiring_screening"
    };

    std::vector<double> harm_probability = {0.35, 0.30, 0.40};
    std::vector<double> harm_impact = {0.90, 0.75, 0.80};
    std::vector<double> vulnerability = {0.90, 0.70, 0.75};
    std::vector<double> institutional_power = {0.95, 0.75, 0.70};
    std::vector<double> controls = {0.45, 0.50, 0.40};

    for (size_t i = 0; i < use_cases.size(); ++i) {
        double score = residual_rights_risk(
            harm_probability[i],
            harm_impact[i],
            vulnerability[i],
            institutional_power[i],
            controls[i]
        );

        std::cout << use_cases[i]
                  << " residual_rights_risk=" << score
                  << " band=" << risk_band(score)
                  << std::endl;
    }

    return 0;
}
