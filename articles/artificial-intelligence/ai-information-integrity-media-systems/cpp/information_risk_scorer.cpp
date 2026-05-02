// High-throughput information-integrity risk scoring example.

#include <iostream>
#include <vector>
#include <string>

double information_integrity_risk(
    double claim_uncertainty,
    double amplification_risk,
    double public_impact,
    double provenance_gap,
    double verification_strength,
    double correction_gap,
    double human_review_gap
) {
    return 0.22 * claim_uncertainty
        + 0.18 * amplification_risk
        + 0.18 * public_impact
        + 0.18 * provenance_gap
        + 0.14 * (1.0 - verification_strength)
        + 0.05 * correction_gap
        + 0.05 * human_review_gap;
}

std::string risk_band(double score) {
    if (score < 0.30) {
        return "low";
    } else if (score < 0.50) {
        return "moderate";
    } else {
        return "high";
    }
}

int main() {
    std::vector<std::string> content = {
        "news_summary",
        "synthetic_video",
        "health_claim_post"
    };

    std::vector<double> uncertainty = {0.20, 0.75, 0.80};
    std::vector<double> amplification = {0.27, 0.92, 1.00};
    std::vector<double> impact = {0.70, 0.85, 0.90};
    std::vector<double> provenance_gap = {0.0, 1.0, 1.0};
    std::vector<double> verification = {0.80, 0.25, 0.30};
    std::vector<double> correction_gap = {0.0, 1.0, 1.0};
    std::vector<double> human_review_gap = {0.0, 1.0, 1.0};

    for (size_t i = 0; i < content.size(); ++i) {
        double score = information_integrity_risk(
            uncertainty[i],
            amplification[i],
            impact[i],
            provenance_gap[i],
            verification[i],
            correction_gap[i],
            human_review_gap[i]
        );

        std::cout << content[i]
                  << " information_integrity_risk=" << score
                  << " band=" << risk_band(score)
                  << std::endl;
    }

    return 0;
}
