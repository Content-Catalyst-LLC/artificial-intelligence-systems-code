/*
Probabilistic Machine Learning and Bayesian AI Systems

C++ example:
Posterior updating and expected-loss prioritization.

Compile:
c++ -std=c++17 bayesian_expected_loss.cpp -o bayesian_expected_loss

Run:
./bayesian_expected_loss
*/

#include <iostream>
#include <string>
#include <vector>

struct AssetRecord {
    std::string id;
    int observed_events;
    int observations;
    double alpha_prior;
    double beta_prior;
};

int main() {
    std::vector<AssetRecord> assets = {
        {"ASSET-001", 1, 20, 2.0, 18.0},
        {"ASSET-002", 7, 35, 2.0, 18.0},
        {"ASSET-003", 0, 10, 2.0, 18.0},
        {"ASSET-004", 10, 40, 2.0, 18.0}
    };

    double cost_false_negative = 100.0;
    double cost_inspection = 8.0;

    for (const auto& asset : assets) {
        double alpha_posterior = asset.alpha_prior + asset.observed_events;
        double beta_posterior = asset.beta_prior + asset.observations - asset.observed_events;
        double posterior_mean = alpha_posterior / (alpha_posterior + beta_posterior);

        double expected_loss_no_inspection = posterior_mean * cost_false_negative;
        double expected_loss_inspection = cost_inspection;
        double expected_loss_reduction = expected_loss_no_inspection - expected_loss_inspection;

        std::cout
            << asset.id
            << " posterior_mean=" << posterior_mean
            << " expected_loss_reduction=" << expected_loss_reduction
            << " recommendation="
            << (expected_loss_reduction > 0.0 ? "prioritize_inspection" : "routine_monitoring")
            << "\n";
    }

    return 0;
}
