/*
AI Systems for Infrastructure and Smart Networks

C++ example:
Simple network centrality and infrastructure-priority scoring.

Compile:
c++ -std=c++17 network_priority_scoring.cpp -o network_priority_scoring

Run:
./network_priority_scoring
*/

#include <algorithm>
#include <iostream>
#include <string>
#include <unordered_map>
#include <vector>

struct Asset {
    std::string id;
    double failure_probability;
    double service_population_score;
    double data_quality_risk;
    int equity_priority;
    double centrality;
    double priority_score;
};

int main() {
    std::vector<std::pair<std::string, std::string>> edges = {
        {"A001", "A002"},
        {"A002", "A003"},
        {"A003", "A004"},
        {"A002", "A005"},
        {"A005", "A006"},
        {"A006", "A001"}
    };

    std::unordered_map<std::string, int> degree;

    for (const auto& edge : edges) {
        degree[edge.first]++;
        degree[edge.second]++;
    }

    int max_degree = 1;
    for (const auto& item : degree) {
        max_degree = std::max(max_degree, item.second);
    }

    std::vector<Asset> assets = {
        {"A001", 0.42, 0.80, 0.10, 0, 0.0, 0.0},
        {"A002", 0.51, 0.95, 0.18, 1, 0.0, 0.0},
        {"A003", 0.34, 0.40, 0.28, 0, 0.0, 0.0},
        {"A004", 0.62, 0.55, 0.12, 0, 0.0, 0.0},
        {"A005", 0.39, 0.75, 0.20, 1, 0.0, 0.0},
        {"A006", 0.47, 0.60, 0.16, 0, 0.0, 0.0}
    };

    for (auto& asset : assets) {
        asset.centrality = static_cast<double>(degree[asset.id]) / max_degree;

        asset.priority_score =
            0.35 * asset.failure_probability +
            0.25 * asset.centrality +
            0.20 * asset.service_population_score +
            0.10 * asset.data_quality_risk +
            0.10 * asset.equity_priority;
    }

    std::sort(
        assets.begin(),
        assets.end(),
        [](const Asset& a, const Asset& b) {
            return a.priority_score > b.priority_score;
        }
    );

    std::cout << "Infrastructure priority ranking\n";
    std::cout << "================================\n";

    for (const auto& asset : assets) {
        std::cout
            << asset.id
            << " priority=" << asset.priority_score
            << " centrality=" << asset.centrality
            << " failure_probability=" << asset.failure_probability
            << " equity_priority=" << asset.equity_priority
            << "\n";
    }

    return 0;
}
