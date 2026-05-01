package main

import (
	"encoding/json"
	"log"
	"net/http"
	"time"
)

type PlanningMetric struct {
	Name             string    `json:"name"`
	Value            float64   `json:"value"`
	WarningThreshold float64   `json:"warning_threshold"`
	ActionThreshold  float64   `json:"action_threshold"`
	Status           string    `json:"status"`
	UpdatedAt        time.Time `json:"updated_at"`
}

type PlanningSnapshot struct {
	SystemID   string           `json:"system_id"`
	SystemName string           `json:"system_name"`
	Generated  time.Time        `json:"generated_at"`
	Metrics    []PlanningMetric `json:"metrics"`
}

func evaluateMetric(name string, value float64, warning float64, action float64) PlanningMetric {
	status := "normal"

	if value >= action {
		status = "action"
	} else if value >= warning {
		status = "warning"
	}

	return PlanningMetric{
		Name:             name,
		Value:            value,
		WarningThreshold: warning,
		ActionThreshold:  action,
		Status:           status,
		UpdatedAt:        time.Now().UTC(),
	}
}

func currentSnapshot() PlanningSnapshot {
	return PlanningSnapshot{
		SystemID:   "planning-sequential-decision-system-001",
		SystemName: "Planning and Sequential Decision Governance Monitor",
		Generated:  time.Now().UTC(),
		Metrics: []PlanningMetric{
			evaluateMetric("planning_risk", 0.21, 0.25, 0.35),
			evaluateMetric("constraint_violation_risk", 0.09, 0.15, 0.25),
			evaluateMetric("irreversibility_risk", 0.04, 0.10, 0.20),
			evaluateMetric("human_override_rate", 0.07, 0.12, 0.20),
			evaluateMetric("plan_failure_rate", 0.03, 0.08, 0.15),
			evaluateMetric("traceability_gap", 0.05, 0.10, 0.18),
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
	http.HandleFunc("/planning-metrics", metricsHandler)

	log.Println("Planning governance monitor listening on http://localhost:8110")
	log.Println("Health:  http://localhost:8110/health")
	log.Println("Metrics: http://localhost:8110/planning-metrics")

	if err := http.ListenAndServe(":8110", nil); err != nil {
		log.Fatal(err)
	}
}
