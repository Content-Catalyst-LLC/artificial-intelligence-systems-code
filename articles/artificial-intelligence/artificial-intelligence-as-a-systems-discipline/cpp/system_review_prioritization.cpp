/*
Artificial Intelligence as a Systems Discipline

C++ example:
High-performance AI system review prioritization.

Compile:
c++ -std=c++17 system_review_prioritization.cpp -o system_review_prioritization

Run:
./system_review_prioritization
*/

#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct AISystem {
    std::string id;
    double technical_maturity;
    double governance_maturity;
    double monitoring_coverage;
    double external_impact;
    int high_stakes;
    double systemic_risk;
};

int main() {
    std::vector<AISystem> systems = {
        {"AI-SYS-001", 0.82, 0.74, 0.76, 0.30, 0, 0.0},
        {"AI-SYS-002", 0.68, 0.44, 0.61, 0.72, 1, 0.0},
        {"AI-SYS-003", 0.73, 0.51, 0.39, 0.55, 0, 0.0},
        {"AI-SYS-004", 0.59, 0.67, 0.33, 0.81, 1, 0.0},
        {"AI-SYS-005", 0.77, 0.69, 0.58, 0.42, 0, 0.0}
    };

    for (auto& system : systems) {
        double system_maturity = 0.5 * system.technical_maturity + 0.5 * system.governance_maturity;

        system.systemic_risk =
            0.35 * (1.0 - system_maturity) +
            0.25 * (1.0 - system.monitoring_coverage) +
            0.20 * system.external_impact +
            0.20 * system.high_stakes;
    }

    std::sort(
        systems.begin(),
        systems.end(),
        [](const AISystem& a, const AISystem& b) {
            return a.systemic_risk > b.systemic_risk;
        }
    );

    std::cout << "AI system review prioritization\n";
    std::cout << "================================\n";

    for (const auto& system : systems) {
        std::cout
            << system.id
            << " systemic_risk=" << system.systemic_risk
            << " technical_maturity=" << system.technical_maturity
            << " governance_maturity=" << system.governance_maturity
            << " monitoring=" << system.monitoring_coverage
            << " high_stakes=" << system.high_stakes
            << "\n";
    }

    return 0;
}
