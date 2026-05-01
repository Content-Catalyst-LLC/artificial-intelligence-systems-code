/*
Artificial Intelligence in Decision Support Systems

C++ example:
High-performance action ranking with expected utility and robust utility.

Compile:
c++ -std=c++17 action_utility_ranking.cpp -o action_utility_ranking

Run:
./action_utility_ranking
*/

#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct DecisionOption {
    std::string id;
    double predicted_risk;
    double benefit;
    double cost;
    double uncertainty;
    int equity_priority;
    double expected_utility;
    double robust_utility;
};

int main() {
    std::vector<DecisionOption> options = {
        {"A001", 0.42, 110.0, 35.0, 0.18, 0, 0.0, 0.0},
        {"A002", 0.77, 95.0, 42.0, 0.34, 1, 0.0, 0.0},
        {"A003", 0.31, 140.0, 50.0, 0.39, 0, 0.0, 0.0},
        {"A004", 0.58, 88.0, 26.0, 0.21, 0, 0.0, 0.0},
        {"A005", 0.63, 105.0, 31.0, 0.22, 1, 0.0, 0.0}
    };

    for (auto& option : options) {
        option.expected_utility =
            option.predicted_risk * option.benefit -
            option.cost +
            10.0 * option.equity_priority -
            8.0 * option.uncertainty;

        option.robust_utility =
            option.expected_utility -
            20.0 * option.uncertainty;
    }

    std::sort(
        options.begin(),
        options.end(),
        [](const DecisionOption& a, const DecisionOption& b) {
            return a.robust_utility > b.robust_utility;
        }
    );

    std::cout << "Decision option ranking\n";
    std::cout << "=======================\n";

    for (const auto& option : options) {
        std::cout
            << option.id
            << " expected_utility=" << option.expected_utility
            << " robust_utility=" << option.robust_utility
            << " uncertainty=" << option.uncertainty
            << " equity_priority=" << option.equity_priority
            << "\n";
    }

    return 0;
}
