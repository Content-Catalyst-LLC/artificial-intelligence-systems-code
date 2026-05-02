#include <iostream>
#include <vector>

double expected_risk(double harm_probability, double harm_impact) {
    return harm_probability * harm_impact;
}

bool should_review(
    double expected_risk_value,
    double uncertainty,
    bool rights_sensitive,
    bool vulnerable_context
) {
    const double risk_threshold = 0.18;
    const double uncertainty_threshold = 0.55;

    return expected_risk_value >= risk_threshold ||
           uncertainty >= uncertainty_threshold ||
           rights_sensitive ||
           vulnerable_context;
}

int main() {
    std::vector<double> harm_probabilities = {0.10, 0.25, 0.40};
    std::vector<double> harm_impacts = {0.50, 0.80, 0.90};
    std::vector<double> uncertainties = {0.20, 0.60, 0.30};
    std::vector<bool> rights_sensitive = {false, false, true};
    std::vector<bool> vulnerable_context = {false, true, false};

    for (size_t i = 0; i < harm_probabilities.size(); ++i) {
        double risk = expected_risk(harm_probabilities[i], harm_impacts[i]);

        bool review = should_review(
            risk,
            uncertainties[i],
            rights_sensitive[i],
            vulnerable_context[i]
        );

        std::cout << "Case " << i + 1
                  << " risk=" << risk
                  << " review=" << review
                  << std::endl;
    }

    return 0;
}
