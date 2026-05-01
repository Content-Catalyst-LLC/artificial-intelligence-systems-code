/*
Artificial Intelligence in Environmental Monitoring

C++ example:
Environmental risk-priority scoring.

Compile:
c++ -std=c++17 environmental_priority_scoring.cpp -o environmental_priority_scoring

Run:
./environmental_priority_scoring
*/

#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct Zone {
    std::string id;
    double stress_probability;
    double anomaly_score;
    double data_quality_risk;
    double exposure_score;
    int environmental_justice_priority;
    double priority_score;
};

int main() {
    std::vector<Zone> zones = {
        {"Z001", 0.44, 0.75, 0.12, 0.80, 0, 0.0},
        {"Z002", 0.61, 1.30, 0.28, 0.65, 1, 0.0},
        {"Z003", 0.37, 0.44, 0.18, 0.50, 0, 0.0},
        {"Z004", 0.72, 1.55, 0.20, 0.91, 1, 0.0},
        {"Z005", 0.28, 0.38, 0.09, 0.30, 0, 0.0}
    };

    for (auto& zone : zones) {
        zone.priority_score =
            0.35 * zone.stress_probability +
            0.20 * std::min(zone.anomaly_score, 2.0) / 2.0 +
            0.15 * zone.data_quality_risk +
            0.15 * zone.exposure_score +
            0.15 * zone.environmental_justice_priority;
    }

    std::sort(
        zones.begin(),
        zones.end(),
        [](const Zone& a, const Zone& b) {
            return a.priority_score > b.priority_score;
        }
    );

    std::cout << "Environmental monitoring priority ranking\n";
    std::cout << "=========================================\n";

    for (const auto& zone : zones) {
        std::cout
            << zone.id
            << " priority=" << zone.priority_score
            << " stress_probability=" << zone.stress_probability
            << " anomaly_score=" << zone.anomaly_score
            << " environmental_justice_priority=" << zone.environmental_justice_priority
            << "\n";
    }

    return 0;
}
