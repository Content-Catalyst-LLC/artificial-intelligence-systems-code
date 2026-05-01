package main

import (
	"encoding/json"
	"log"
	"net/http"
	"time"
)

type FoundationMetric struct {
	Name             string    `json:"name"`
	Value            float64   `json:"value"`
	WarningThreshold float64   `json:"warning_threshold"`
	ActionThreshold  float64   `json:"action_threshold"`
	Status           string    `json:"status"`
	UpdatedAt        time.Time `json:"updated_at"`
}

type FoundationSnapshot struct {
	SystemID   string             `json:"system_id"`
	SystemName string             `json:"system_name"`
	Generated  time.Time          `json:"generated_at"`
	Metrics    []FoundationMetric `json:"metrics"`
}

func evaluateMetric(name string, value float64, warning float64, action float64) FoundationMetric {
	status := "normal"

	if value >= action {
		status = "action"
	} else if value >= warning {
		status = "warning"
	}

	return FoundationMetric{
		Name:             name,
		Value:            value,
		WarningThreshold: warning,
		ActionThreshold:  action,
		Status:           status,
		UpdatedAt:        time.Now().UTC(),
	}
}

func currentSnapshot() FoundationSnapshot {
	return FoundationSnapshot{
		SystemID:   "foundation-model-001",
		SystemName: "Self-Supervised Learning and Foundation Model Governance Monitor",
		Generated:  time.Now().UTC(),
		Metrics: []FoundationMetric{
			evaluateMetric("weak_provenance_run_share", 0.14, 0.20, 0.35),
			evaluateMetric("high_privacy_risk_run_share", 0.08, 0.15, 0.30),
			evaluateMetric("open_bias_review_count", 1.0, 2.0, 5.0),
			evaluateMetric("broad_reuse_low_governance_count", 2.0, 3.0, 8.0),
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
	http.HandleFunc("/foundation-model-metrics", metricsHandler)

	log.Println("Foundation model governance monitor listening on http://localhost:8100")
	log.Println("Health:  http://localhost:8100/health")
	log.Println("Metrics: http://localhost:8100/foundation-model-metrics")

	if err := http.ListenAndServe(":8100", nil); err != nil {
		log.Fatal(err)
	}
}
