#include <cmath>
#include <iostream>
#include <vector>

double combined_score(double ai_score, double expert_score, double ai_reliance) {
    return ai_reliance * ai_score + (1.0 - ai_reliance) * expert_score;
}

bool automation_bias_flag(double observed_reliance, double warranted_reliance) {
    return observed_reliance > warranted_reliance + 0.15;
}

bool disagreement_requires_review(double ai_score, double expert_score) {
    return std::abs(ai_score - expert_score) > 0.30;
}

int main() {
    std::vector<double> ai_scores = {0.20, 0.70, 0.85};
    std::vector<double> expert_scores = {0.25, 0.40, 0.80};
    std::vector<double> observed_reliance = {0.40, 0.82, 0.55};
    std::vector<double> warranted_reliance = {0.45, 0.60, 0.50};

    for (size_t i = 0; i < ai_scores.size(); ++i) {
        double score = combined_score(
            ai_scores[i],
            expert_scores[i],
            observed_reliance[i]
        );

        bool disagreement_review = disagreement_requires_review(
            ai_scores[i],
            expert_scores[i]
        );

        bool bias_review = automation_bias_flag(
            observed_reliance[i],
            warranted_reliance[i]
        );

        std::cout << "Case " << i + 1
                  << " combined_score=" << score
                  << " disagreement_review_required=" << disagreement_review
                  << " automation_bias_flag=" << bias_review
                  << std::endl;
    }

    return 0;
}
