package main

import (
	"encoding/json"
	"log"
	"net/http"
	"time"
)

type ProbabilisticMetric struct {
	Name             string    `json:"name"`
	Value            float64   `json:"value"`
	WarningThreshold float64   `json:"warning_threshold"`
	ActionThreshold  float64   `json:"action_threshold"`
	Status           string    `json:"status"`
	UpdatedAt        time.Time `json:"updated_at"`
}

type ProbabilisticSnapshot struct {
	SystemID   string                `json:"system_id"`
	SystemName string                `json:"system_name"`
	Generated  time.Time             `json:"generated_at"`
	Metrics    []ProbabilisticMetric `json:"metrics"`
}

func evaluateMetric(name string, value float64, warning float64, action float64) ProbabilisticMetric {
	status := "normal"

	if value >= action {
		status = "action"
	} else if value >= warning {
		status = "warning"
	}

	return ProbabilisticMetric{
		Name:             name,
		Value:            value,
		WarningThreshold: warning,
		ActionThreshold:  action,
		Status:           status,
		UpdatedAt:        time.Now().UTC(),
	}
}

func currentSnapshot() ProbabilisticSnapshot {
	return ProbabilisticSnapshot{
		SystemID:   "bayesian-ai-system-001",
		SystemName: "Probabilistic Machine Learning Governance Monitor",
		Generated:  time.Now().UTC(),
		Metrics: []ProbabilisticMetric{
			evaluateMetric("mean_calibration_error", 0.06, 0.08, 0.12),
			evaluateMetric("high_uncertainty_case_share", 0.18, 0.25, 0.40),
			evaluateMetric("unreviewed_prior_count", 1.0, 2.0, 5.0),
			evaluateMetric("inference_diagnostic_warning_count", 2.0, 3.0, 8.0),
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
	http.HandleFunc("/probabilistic-metrics", metricsHandler)

	log.Println("Probabilistic ML governance monitor listening on http://localhost:8101")
	log.Println("Health:  http://localhost:8101/health")
	log.Println("Metrics: http://localhost:8101/probabilistic-metrics")

	if err := http.ListenAndServe(":8101", nil); err != nil {
		log.Fatal(err)
	}
}
