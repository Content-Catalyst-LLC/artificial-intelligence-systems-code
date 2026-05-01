package main

import (
	"encoding/json"
	"log"
	"net/http"
	"time"
)

type EvaluationMetric struct {
	Name             string    `json:"name"`
	Value            float64   `json:"value"`
	WarningThreshold float64   `json:"warning_threshold"`
	ActionThreshold  float64   `json:"action_threshold"`
	Status           string    `json:"status"`
	UpdatedAt        time.Time `json:"updated_at"`
}

type EvaluationSnapshot struct {
	SystemID   string             `json:"system_id"`
	SystemName string             `json:"system_name"`
	Generated  time.Time          `json:"generated_at"`
	Metrics    []EvaluationMetric `json:"metrics"`
}

func evaluateMetric(name string, value float64, warning float64, action float64) EvaluationMetric {
	status := "normal"

	if value >= action {
		status = "action"
	} else if value >= warning {
		status = "warning"
	}

	return EvaluationMetric{
		Name:             name,
		Value:            value,
		WarningThreshold: warning,
		ActionThreshold:  action,
		Status:           status,
		UpdatedAt:        time.Now().UTC(),
	}
}

func currentSnapshot() EvaluationSnapshot {
	return EvaluationSnapshot{
		SystemID:   "synthetic-evaluation-system-001",
		SystemName: "Synthetic Data and Simulation Evaluation Monitor",
		Generated:  time.Now().UTC(),
		Metrics: []EvaluationMetric{
			evaluateMetric("fidelity_risk", 0.14, 0.20, 0.30),
			evaluateMetric("utility_gap", 0.03, 0.05, 0.10),
			evaluateMetric("privacy_proximity_risk", 0.02, 0.05, 0.10),
			evaluateMetric("rare_case_coverage_gap", 0.04, 0.06, 0.12),
			evaluateMetric("sim_to_real_gap", 0.11, 0.18, 0.30),
			evaluateMetric("benchmark_overfit_risk", 0.08, 0.15, 0.25),
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
	http.HandleFunc("/synthetic-evaluation-metrics", metricsHandler)

	log.Println("Synthetic evaluation monitor listening on http://localhost:8109")
	log.Println("Health:  http://localhost:8109/health")
	log.Println("Metrics: http://localhost:8109/synthetic-evaluation-metrics")

	if err := http.ListenAndServe(":8109", nil); err != nil {
		log.Fatal(err)
	}
}
