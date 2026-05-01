package main

import (
	"encoding/json"
	"log"
	"net/http"
	"time"
)

type MetricStatus string

const (
	StatusNormal  MetricStatus = "normal"
	StatusWarning MetricStatus = "warning"
	StatusAction  MetricStatus = "action"
)

type SafetyMetric struct {
	Name             string       `json:"name"`
	Value            float64      `json:"value"`
	WarningThreshold float64      `json:"warning_threshold"`
	ActionThreshold  float64      `json:"action_threshold"`
	Status           MetricStatus `json:"status"`
	UpdatedAt        time.Time    `json:"updated_at"`
}

type SafetySnapshot struct {
	SystemID   string         `json:"system_id"`
	SystemName string         `json:"system_name"`
	Metrics    []SafetyMetric `json:"metrics"`
	Generated  time.Time      `json:"generated_at"`
}

func evaluateMetric(name string, value float64, warning float64, action float64) SafetyMetric {
	status := StatusNormal

	if value >= action {
		status = StatusAction
	} else if value >= warning {
		status = StatusWarning
	}

	return SafetyMetric{
		Name:             name,
		Value:            value,
		WarningThreshold: warning,
		ActionThreshold:  action,
		Status:           status,
		UpdatedAt:        time.Now().UTC(),
	}
}

func currentSnapshot() SafetySnapshot {
	return SafetySnapshot{
		SystemID:   "ai-safety-system-001",
		SystemName: "AI Safety and System Reliability Monitor",
		Generated:  time.Now().UTC(),
		Metrics: []SafetyMetric{
			evaluateMetric("missed_failure_rate", 0.018, 0.010, 0.025),
			evaluateMetric("expected_calibration_error", 0.061, 0.050, 0.100),
			evaluateMetric("data_drift_index", 0.190, 0.100, 0.250),
			evaluateMetric("human_review_rate", 0.214, 0.350, 0.500),
			evaluateMetric("monitoring_latency_seconds", 4.800, 10.000, 30.000),
		},
	}
}

func healthHandler(writer http.ResponseWriter, request *http.Request) {
	response := map[string]string{
		"status": "ok",
		"time":   time.Now().UTC().Format(time.RFC3339),
	}

	writer.Header().Set("Content-Type", "application/json")
	json.NewEncoder(writer).Encode(response)
}

func metricsHandler(writer http.ResponseWriter, request *http.Request) {
	snapshot := currentSnapshot()

	writer.Header().Set("Content-Type", "application/json")
	json.NewEncoder(writer).Encode(snapshot)
}

func main() {
	http.HandleFunc("/health", healthHandler)
	http.HandleFunc("/metrics", metricsHandler)

	log.Println("AI safety monitor listening on http://localhost:8088")
	log.Println("Health endpoint:  http://localhost:8088/health")
	log.Println("Metrics endpoint: http://localhost:8088/metrics")

	if err := http.ListenAndServe(":8088", nil); err != nil {
		log.Fatal(err)
	}
}
