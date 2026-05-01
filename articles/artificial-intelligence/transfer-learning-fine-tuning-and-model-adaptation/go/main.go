package main

import (
	"encoding/json"
	"log"
	"net/http"
	"time"
)

type AdaptationMetric struct {
	Name             string    `json:"name"`
	Value            float64   `json:"value"`
	WarningThreshold float64   `json:"warning_threshold"`
	ActionThreshold  float64   `json:"action_threshold"`
	Status           string    `json:"status"`
	UpdatedAt        time.Time `json:"updated_at"`
}

type AdaptationSnapshot struct {
	SystemID   string             `json:"system_id"`
	SystemName string             `json:"system_name"`
	Generated  time.Time          `json:"generated_at"`
	Metrics    []AdaptationMetric `json:"metrics"`
}

func evaluateMetric(name string, value float64, warning float64, action float64) AdaptationMetric {
	status := "normal"

	if value >= action {
		status = "action"
	} else if value >= warning {
		status = "warning"
	}

	return AdaptationMetric{
		Name:             name,
		Value:            value,
		WarningThreshold: warning,
		ActionThreshold:  action,
		Status:           status,
		UpdatedAt:        time.Now().UTC(),
	}
}

func currentSnapshot() AdaptationSnapshot {
	return AdaptationSnapshot{
		SystemID:   "model-adaptation-001",
		SystemName: "Transfer Learning and Fine-Tuning Governance Monitor",
		Generated:  time.Now().UTC(),
		Metrics: []AdaptationMetric{
			evaluateMetric("negative_transfer_rate", 0.06, 0.10, 0.20),
			evaluateMetric("low_retention_rate", 0.12, 0.15, 0.30),
			evaluateMetric("unapproved_sensitive_adaptations", 1.0, 2.0, 5.0),
			evaluateMetric("adapter_sprawl_index", 0.18, 0.25, 0.45),
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
	http.HandleFunc("/adaptation-metrics", metricsHandler)

	log.Println("Model adaptation monitor listening on http://localhost:8099")
	log.Println("Health:  http://localhost:8099/health")
	log.Println("Metrics: http://localhost:8099/adaptation-metrics")

	if err := http.ListenAndServe(":8099", nil); err != nil {
		log.Fatal(err)
	}
}
