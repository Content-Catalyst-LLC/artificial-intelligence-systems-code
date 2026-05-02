// High-throughput documentation-priority scoring example.

#include <iostream>
#include <vector>
#include <string>

double residual_risk(double likelihood, double impact, double mitigation_strength) {
    return likelihood * impact * (1.0 - mitigation_strength);
}

double documentation_priority(
    double residual_risk_value,
    double documentation_completeness,
    double staleness_score
) {
    return residual_risk_value *
           (1.0 - documentation_completeness) *
           (1.0 + 0.25 * staleness_score);
}

std::string priority_band(double score) {
    if (score < 0.05) {
        return "low";
    } else if (score < 0.10) {
        return "moderate";
    } else {
        return "high";
    }
}

int main() {
    std::vector<std::string> risks = {
        "unfair_outcome_disparity",
        "insufficient_human_review",
        "monitoring_not_reviewed"
    };

    std::vector<double> likelihood = {0.35, 0.30, 0.50};
    std::vector<double> impact = {0.90, 0.85, 0.65};
    std::vector<double> mitigation = {0.45, 0.50, 0.35};
    std::vector<double> completeness = {0.60, 0.55, 0.40};
    std::vector<double> staleness = {0.50, 1.00, 1.80};

    for (size_t i = 0; i < risks.size(); ++i) {
        double risk = residual_risk(likelihood[i], impact[i], mitigation[i]);
        double priority = documentation_priority(risk, completeness[i], staleness[i]);

        std::cout << risks[i]
                  << " residual_risk=" << risk
                  << " documentation_priority=" << priority
                  << " band=" << priority_band(priority)
                  << std::endl;
    }

    return 0;
}
