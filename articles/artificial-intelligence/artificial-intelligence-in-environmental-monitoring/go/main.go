package main

import (
	"encoding/json"
	"log"
	"net/http"
	"time"
)

type EnvironmentalMetric struct {
	Name             string    `json:"name"`
	Value            float64   `json:"value"`
	WarningThreshold float64   `json:"warning_threshold"`
	ActionThreshold  float64   `json:"action_threshold"`
	Status           string    `json:"status"`
	UpdatedAt        time.Time `json:"updated_at"`
}

type EnvironmentalSnapshot struct {
	SystemID   string                `json:"system_id"`
	SystemName string                `json:"system_name"`
	Generated  time.Time             `json:"generated_at"`
	Metrics    []EnvironmentalMetric `json:"metrics"`
}

func evaluateMetric(name string, value float64, warning float64, action float64) EnvironmentalMetric {
	status := "normal"

	if value >= action {
		status = "action"
	} else if value >= warning {
		status = "warning"
	}

	return EnvironmentalMetric{
		Name:             name,
		Value:            value,
		WarningThreshold: warning,
		ActionThreshold:  action,
		Status:           status,
		UpdatedAt:        time.Now().UTC(),
	}
}

func currentSnapshot() EnvironmentalSnapshot {
	return EnvironmentalSnapshot{
		SystemID:   "environmental-monitoring-001",
		SystemName: "AI Environmental Monitoring Service",
		Generated:  time.Now().UTC(),
		Metrics: []EnvironmentalMetric{
			evaluateMetric("mean_environmental_stress_probability", 0.42, 0.50, 0.65),
			evaluateMetric("mean_anomaly_score", 0.81, 1.00, 1.50),
			evaluateMetric("data_quality_risk", 0.17, 0.25, 0.35),
			evaluateMetric("open_alert_count", 3.00, 5.00, 10.00),
			evaluateMetric("environmental_justice_review_share", 0.28, 0.35, 0.50),
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
	http.HandleFunc("/environmental-metrics", metricsHandler)

	log.Println("Environmental monitoring service listening on http://localhost:8093")
	log.Println("Health:  http://localhost:8093/health")
	log.Println("Metrics: http://localhost:8093/environmental-metrics")

	if err := http.ListenAndServe(":8093", nil); err != nil {
		log.Fatal(err)
	}
}
