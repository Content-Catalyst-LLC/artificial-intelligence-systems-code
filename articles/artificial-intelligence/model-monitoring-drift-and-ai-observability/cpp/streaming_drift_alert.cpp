/*
Model Monitoring, Drift, and AI Observability

C++ example:
Streaming drift scoring and threshold-based alerting.

Compile:
c++ -std=c++17 streaming_drift_alert.cpp -o streaming_drift_alert

Run:
./streaming_drift_alert
*/

#include <iostream>
#include <string>
#include <vector>

struct MonitoringBatch {
    std::string batch_id;
    double max_feature_psi;
    double prediction_psi;
    double accuracy;
    double latency_ms;
    int incident_count;
};

double observability_risk(const MonitoringBatch& batch) {
    double performance_degradation = std::max(0.0, 0.88 - batch.accuracy);
    double drift_signal = 0.45 * batch.max_feature_psi + 0.35 * batch.prediction_psi;
    double operational_signal = std::min(1.0, batch.latency_ms / 1200.0) + std::min(1.0, batch.incident_count / 4.0);

    return 0.40 * drift_signal
        + 0.30 * performance_degradation
        + 0.30 * operational_signal;
}

std::string alert_level(const MonitoringBatch& batch) {
    double risk = observability_risk(batch);

    if (risk > 0.60) {
        return "incident_review";
    }

    if (risk > 0.40) {
        return "action_required";
    }

    if (risk > 0.25 || batch.max_feature_psi > 0.25 || batch.prediction_psi > 0.25) {
        return "warning";
    }

    return "normal";
}

int main() {
    std::vector<MonitoringBatch> batches = {
        {"BATCH-001", 0.05, 0.04, 0.88, 410, 0},
        {"BATCH-002", 0.18, 0.12, 0.84, 520, 0},
        {"BATCH-003", 0.31, 0.16, 0.82, 610, 0},
        {"BATCH-004", 0.15, 0.29, 0.83, 590, 0},
        {"BATCH-005", 0.10, 0.09, 0.74, 720, 0},
        {"BATCH-006", 0.08, 0.07, 0.86, 1400, 0},
        {"BATCH-007", 0.06, 0.05, 0.87, 500, 3}
    };

    for (const auto& batch : batches) {
        std::cout
            << batch.batch_id
            << " risk=" << observability_risk(batch)
            << " alert=" << alert_level(batch)
            << "\n";
    }

    return 0;
}
