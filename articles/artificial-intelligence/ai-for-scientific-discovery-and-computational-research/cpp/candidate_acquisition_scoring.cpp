/*
AI for Scientific Discovery and Computational Research

C++ example:
Candidate ranking with acquisition scoring.

Compile:
c++ -std=c++17 candidate_acquisition_scoring.cpp -o candidate_acquisition_scoring

Run:
./candidate_acquisition_scoring
*/

#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct Candidate {
    std::string id;
    double predicted_property;
    double uncertainty;
    double cost;
    double safety_penalty;
    double acquisition_score;
};

int main() {
    std::vector<Candidate> candidates = {
        {"C001", 2.14, 0.21, 0.42, 0.00, 0.0},
        {"C002", 1.88, 0.82, 0.55, 0.00, 0.0},
        {"C003", 2.31, 0.34, 0.71, 0.35, 0.0},
        {"C004", 1.12, 0.18, 0.33, 0.00, 0.0},
        {"C005", 2.01, 0.41, 0.48, 0.00, 0.0}
    };

    for (auto& candidate : candidates) {
        candidate.acquisition_score =
            0.60 * candidate.predicted_property +
            0.30 * candidate.uncertainty -
            0.20 * candidate.cost -
            0.40 * candidate.safety_penalty;
    }

    std::sort(
        candidates.begin(),
        candidates.end(),
        [](const Candidate& a, const Candidate& b) {
            return a.acquisition_score > b.acquisition_score;
        }
    );

    std::cout << "Scientific candidate ranking\n";
    std::cout << "============================\n";

    for (const auto& candidate : candidates) {
        std::cout
            << candidate.id
            << " acquisition=" << candidate.acquisition_score
            << " predicted_property=" << candidate.predicted_property
            << " uncertainty=" << candidate.uncertainty
            << " safety_penalty=" << candidate.safety_penalty
            << "\n";
    }

    return 0;
}
