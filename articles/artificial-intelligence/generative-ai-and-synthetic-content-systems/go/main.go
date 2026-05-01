package main

import (
	"encoding/json"
	"log"
	"net/http"
	"time"
)

type SyntheticContentMetric struct {
	Name             string    `json:"name"`
	Value            float64   `json:"value"`
	WarningThreshold float64   `json:"warning_threshold"`
	ActionThreshold  float64   `json:"action_threshold"`
	Status           string    `json:"status"`
	UpdatedAt        time.Time `json:"updated_at"`
}

type SyntheticContentSnapshot struct {
	SystemID   string                   `json:"system_id"`
	SystemName string                   `json:"system_name"`
	Generated  time.Time                `json:"generated_at"`
	Metrics    []SyntheticContentMetric `json:"metrics"`
}

func evaluateMetric(name string, value float64, warning float64, action float64) SyntheticContentMetric {
	status := "normal"

	if value >= action {
		status = "action"
	} else if value >= warning {
		status = "warning"
	}

	return SyntheticContentMetric{
		Name:             name,
		Value:            value,
		WarningThreshold: warning,
		ActionThreshold:  action,
		Status:           status,
		UpdatedAt:        time.Now().UTC(),
	}
}

func currentSnapshot() SyntheticContentSnapshot {
	return SyntheticContentSnapshot{
		SystemID:   "synthetic-content-001",
		SystemName: "Generative AI Synthetic Content Monitor",
		Generated:  time.Now().UTC(),
		Metrics: []SyntheticContentMetric{
			evaluateMetric("high_risk_artifact_share", 0.14, 0.20, 0.35),
			evaluateMetric("missing_provenance_share", 0.22, 0.25, 0.40),
			evaluateMetric("unreviewed_sensitive_artifacts", 2.0, 3.0, 8.0),
			evaluateMetric("open_synthetic_content_incidents", 1.0, 2.0, 5.0),
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
	http.HandleFunc("/synthetic-content-metrics", metricsHandler)

	log.Println("Synthetic content monitor listening on http://localhost:8096")
	log.Println("Health:  http://localhost:8096/health")
	log.Println("Metrics: http://localhost:8096/synthetic-content-metrics")

	if err := http.ListenAndServe(":8096", nil); err != nil {
		log.Fatal(err)
	}
}
