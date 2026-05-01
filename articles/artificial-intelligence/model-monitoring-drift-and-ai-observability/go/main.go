package main

import (
	"encoding/json"
	"log"
	"net/http"
	"time"
)

type ObservabilityMetric struct {
	Name             string    `json:"name"`
	Value            float64   `json:"value"`
	WarningThreshold float64   `json:"warning_threshold"`
	ActionThreshold  float64   `json:"action_threshold"`
	Status           string    `json:"status"`
	UpdatedAt        time.Time `json:"updated_at"`
}

type ObservabilitySnapshot struct {
	SystemID   string                `json:"system_id"`
	SystemName string                `json:"system_name"`
	Generated  time.Time             `json:"generated_at"`
	Metrics    []ObservabilityMetric `json:"metrics"`
}

func evaluateMetric(name string, value float64, warning float64, action float64) ObservabilityMetric {
	status := "normal"

	if value >= action {
		status = "action"
	} else if value >= warning {
		status = "warning"
	}

	return ObservabilityMetric{
		Name:             name,
		Value:            value,
		WarningThreshold: warning,
		ActionThreshold:  action,
		Status:           status,
		UpdatedAt:        time.Now().UTC(),
	}
}

func currentSnapshot() ObservabilitySnapshot {
	return ObservabilitySnapshot{
		SystemID:   "ai-observability-system-001",
		SystemName: "Model Monitoring and AI Observability Monitor",
		Generated:  time.Now().UTC(),
		Metrics: []ObservabilityMetric{
			evaluateMetric("max_feature_psi", 0.21, 0.20, 0.35),
			evaluateMetric("prediction_psi", 0.18, 0.20, 0.35),
			evaluateMetric("performance_degradation", 0.07, 0.08, 0.15),
			evaluateMetric("missing_rate", 0.035, 0.05, 0.10),
			evaluateMetric("incident_rate", 0.06, 0.08, 0.15),
			evaluateMetric("mean_latency_ms", 680.0, 900.0, 1200.0),
		},
	}
}

func healthHandler(writer http.ResponseWriter, request *http.Request) {
	writer.Header().Set("Content-Type", "application/json")
	json.NewEncoder(writer).Encode(map[string]string{
		"status": "ok",
		"time":   time.Now().UTC().Format(time.RFC3339),
	})
}

func metricsHandler(writer http.ResponseWriter, request *http.Request) {
	writer.Header().Set("Content-Type", "application/json")
	json.NewEncoder(writer).Encode(currentSnapshot())
}

func main() {
	http.HandleFunc("/health", healthHandler)
	http.HandleFunc("/observability-metrics", metricsHandler)

	log.Println("AI observability monitor listening on http://localhost:8106")
	log.Println("Health:  http://localhost:8106/health")
	log.Println("Metrics: http://localhost:8106/observability-metrics")

	if err := http.ListenAndServe(":8106", nil); err != nil {
		log.Fatal(err)
	}
}
