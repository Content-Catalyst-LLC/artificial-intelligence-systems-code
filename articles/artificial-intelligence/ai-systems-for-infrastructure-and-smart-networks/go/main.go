package main

import (
	"encoding/json"
	"log"
	"net/http"
	"time"
)

type InfrastructureMetric struct {
	Name             string    `json:"name"`
	Value            float64   `json:"value"`
	WarningThreshold float64   `json:"warning_threshold"`
	ActionThreshold  float64   `json:"action_threshold"`
	Status           string    `json:"status"`
	UpdatedAt        time.Time `json:"updated_at"`
}

type InfrastructureSnapshot struct {
	SystemID   string                 `json:"system_id"`
	SystemName string                 `json:"system_name"`
	Domain     string                 `json:"domain"`
	Generated  time.Time              `json:"generated_at"`
	Metrics    []InfrastructureMetric `json:"metrics"`
}

func evaluateMetric(name string, value float64, warning float64, action float64) InfrastructureMetric {
	status := "normal"

	if value >= action {
		status = "action"
	} else if value >= warning {
		status = "warning"
	}

	return InfrastructureMetric{
		Name:             name,
		Value:            value,
		WarningThreshold: warning,
		ActionThreshold:  action,
		Status:           status,
		UpdatedAt:        time.Now().UTC(),
	}
}

func currentSnapshot() InfrastructureSnapshot {
	return InfrastructureSnapshot{
		SystemID:   "smart-network-001",
		SystemName: "Smart Infrastructure Network Monitor",
		Domain:     "water-energy-transport-cyberphysical",
		Generated:  time.Now().UTC(),
		Metrics: []InfrastructureMetric{
			evaluateMetric("mean_failure_probability", 0.31, 0.45, 0.60),
			evaluateMetric("data_quality_risk", 0.18, 0.20, 0.35),
			evaluateMetric("telemetry_latency_seconds", 7.8, 15.0, 30.0),
			evaluateMetric("high_criticality_asset_share", 0.14, 0.20, 0.35),
			evaluateMetric("open_incident_count", 2.0, 3.0, 5.0),
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
	http.HandleFunc("/infrastructure-metrics", metricsHandler)

	log.Println("Smart infrastructure monitor listening on http://localhost:8092")
	log.Println("Health:  http://localhost:8092/health")
	log.Println("Metrics: http://localhost:8092/infrastructure-metrics")

	if err := http.ListenAndServe(":8092", nil); err != nil {
		log.Fatal(err)
	}
}
