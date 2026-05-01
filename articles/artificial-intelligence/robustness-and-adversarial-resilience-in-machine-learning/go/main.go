package main

import (
	"encoding/json"
	"log"
	"net/http"
	"time"
)

type ResilienceMetric struct {
	Name             string    `json:"name"`
	Value            float64   `json:"value"`
	WarningThreshold float64   `json:"warning_threshold"`
	ActionThreshold  float64   `json:"action_threshold"`
	Status           string    `json:"status"`
	UpdatedAt        time.Time `json:"updated_at"`
}

type ResilienceSnapshot struct {
	SystemID   string             `json:"system_id"`
	SystemName string             `json:"system_name"`
	Generated  time.Time          `json:"generated_at"`
	Metrics    []ResilienceMetric `json:"metrics"`
}

func evaluateMetric(name string, value float64, warning float64, action float64) ResilienceMetric {
	status := "normal"

	if value >= action {
		status = "action"
	} else if value >= warning {
		status = "warning"
	}

	return ResilienceMetric{
		Name:             name,
		Value:            value,
		WarningThreshold: warning,
		ActionThreshold:  action,
		Status:           status,
		UpdatedAt:        time.Now().UTC(),
	}
}

func currentSnapshot() ResilienceSnapshot {
	return ResilienceSnapshot{
		SystemID:   "adversarial-resilience-system-001",
		SystemName: "Adversarial Resilience Governance Monitor",
		Generated:  time.Now().UTC(),
		Metrics: []ResilienceMetric{
			evaluateMetric("adversarial_performance_drop", 0.18, 0.20, 0.30),
			evaluateMetric("attack_success_rate", 0.14, 0.20, 0.35),
			evaluateMetric("prompt_injection_success_rate", 0.09, 0.12, 0.25),
			evaluateMetric("retrieval_poisoning_detection_gap", 0.11, 0.15, 0.25),
			evaluateMetric("containment_failure_rate", 0.05, 0.08, 0.15),
			evaluateMetric("high_severity_incident_rate", 0.03, 0.05, 0.10),
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
	http.HandleFunc("/adversarial-resilience-metrics", metricsHandler)

	log.Println("Adversarial resilience monitor listening on http://localhost:8107")
	log.Println("Health:  http://localhost:8107/health")
	log.Println("Metrics: http://localhost:8107/adversarial-resilience-metrics")

	if err := http.ListenAndServe(":8107", nil); err != nil {
		log.Fatal(err)
	}
}
