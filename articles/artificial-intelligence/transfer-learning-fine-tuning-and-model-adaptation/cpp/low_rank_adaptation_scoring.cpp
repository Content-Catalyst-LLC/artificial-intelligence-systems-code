/*
Transfer Learning, Fine-Tuning, and Model Adaptation

C++ example:
Low-rank adaptation scoring and transfer-gain review.

Compile:
c++ -std=c++17 low_rank_adaptation_scoring.cpp -o low_rank_adaptation_scoring

Run:
./low_rank_adaptation_scoring
*/

#include <iostream>
#include <string>
#include <vector>

struct AdaptationRun {
    std::string id;
    std::string method;
    double target_performance;
    double baseline_performance;
    double source_retention;
    double compute_cost;
    double adaptation_risk;
};

int main() {
    std::vector<AdaptationRun> runs = {
        {"ADAPT-001", "lora", 0.78, 0.66, 0.92, 0.24, 0.0},
        {"ADAPT-002", "full_fine_tuning", 0.81, 0.66, 0.76, 0.90, 0.0},
        {"ADAPT-003", "qlora", 0.76, 0.66, 0.89, 0.16, 0.0},
        {"ADAPT-004", "adapter_tuning", 0.64, 0.66, 0.93, 0.28, 0.0}
    };

    for (auto& run : runs) {
        double transfer_gain = run.target_performance - run.baseline_performance;
        double forgetting_risk = 1.0 - run.source_retention;

        run.adaptation_risk =
            0.45 * forgetting_risk +
            0.35 * (transfer_gain < 0.0 ? 1.0 : 0.0) +
            0.20 * run.compute_cost;

        std::cout
            << run.id
            << " method=" << run.method
            << " transfer_gain=" << transfer_gain
            << " source_retention=" << run.source_retention
            << " adaptation_risk=" << run.adaptation_risk
            << "\n";
    }

    return 0;
}
