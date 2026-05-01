package main

import (
	"encoding/json"
	"log"
	"net/http"
	"time"
)

type DecisionMetric struct {
	Name             string    `json:"name"`
	Value            float64   `json:"value"`
	WarningThreshold float64   `json:"warning_threshold"`
	ActionThreshold  float64   `json:"action_threshold"`
	Status           string    `json:"status"`
	UpdatedAt        time.Time `json:"updated_at"`
}

type DecisionSnapshot struct {
	SystemID   string           `json:"system_id"`
	SystemName string           `json:"system_name"`
	Generated  time.Time        `json:"generated_at"`
	Metrics    []DecisionMetric `json:"metrics"`
}

func evaluateMetric(name string, value float64, warning float64, action float64) DecisionMetric {
	status := "normal"

	if value >= action {
		status = "action"
	} else if value >= warning {
		status = "warning"
	}

	return DecisionMetric{
		Name:             name,
		Value:            value,
		WarningThreshold: warning,
		ActionThreshold:  action,
		Status:           status,
		UpdatedAt:        time.Now().UTC(),
	}
}

func currentSnapshot() DecisionSnapshot {
	return DecisionSnapshot{
		SystemID:   "decision-support-001",
		SystemName: "AI Decision Support Monitor",
		Generated:  time.Now().UTC(),
		Metrics: []DecisionMetric{
			evaluateMetric("high_uncertainty_decision_share", 0.18, 0.25, 0.40),
			evaluateMetric("human_override_rate", 0.07, 0.15, 0.30),
			evaluateMetric("unreviewed_high_risk_count", 1.0, 2.0, 5.0),
			evaluateMetric("open_governance_actions", 3.0, 5.0, 10.0),
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
	http.HandleFunc("/decision-metrics", metricsHandler)

	log.Println("Decision support monitor listening on http://localhost:8095")
	log.Println("Health:  http://localhost:8095/health")
	log.Println("Metrics: http://localhost:8095/decision-metrics")

	if err := http.ListenAndServe(":8095", nil); err != nil {
		log.Fatal(err)
	}
}
