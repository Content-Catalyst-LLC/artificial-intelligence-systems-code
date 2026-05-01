// Defensive residual-risk scoring example.
// This example does not implement attack techniques.

#include <iostream>
#include <vector>
#include <string>

double residual_risk(double exposure, double impact, double likelihood, double control_strength) {
    double inherent_risk = exposure * impact * likelihood;
    return inherent_risk * (1.0 - control_strength);
}

std::string risk_band(double score) {
    if (score < 0.10) {
        return "low";
    } else if (score < 0.20) {
        return "moderate";
    } else {
        return "high";
    }
}

int main() {
    std::vector<std::string> assets = {"retrieval_index", "model_endpoint", "tool_api_gateway"};
    std::vector<double> exposures = {0.75, 0.80, 0.90};
    std::vector<double> impacts = {0.75, 0.90, 0.95};
    std::vector<double> likelihoods = {0.60, 0.65, 0.70};
    std::vector<double> controls = {0.50, 0.65, 0.55};

    for (size_t i = 0; i < assets.size(); ++i) {
        double score = residual_risk(exposures[i], impacts[i], likelihoods[i], controls[i]);

        std::cout << assets[i]
                  << " residual_risk=" << score
                  << " band=" << risk_band(score)
                  << std::endl;
    }

    return 0;
}
