package main

import (
	"encoding/json"
	"log"
	"net/http"
	"time"
)

type MultimodalMetric struct {
	Name             string    `json:"name"`
	Value            float64   `json:"value"`
	WarningThreshold float64   `json:"warning_threshold"`
	ActionThreshold  float64   `json:"action_threshold"`
	Status           string    `json:"status"`
	UpdatedAt        time.Time `json:"updated_at"`
}

type MultimodalSnapshot struct {
	SystemID   string             `json:"system_id"`
	SystemName string             `json:"system_name"`
	Generated  time.Time          `json:"generated_at"`
	Metrics    []MultimodalMetric `json:"metrics"`
}

func evaluateMetric(name string, value float64, warning float64, action float64) MultimodalMetric {
	status := "normal"

	if value >= action {
		status = "action"
	} else if value >= warning {
		status = "warning"
	}

	return MultimodalMetric{
		Name:             name,
		Value:            value,
		WarningThreshold: warning,
		ActionThreshold:  action,
		Status:           status,
		UpdatedAt:        time.Now().UTC(),
	}
}

func currentSnapshot() MultimodalSnapshot {
	return MultimodalSnapshot{
		SystemID:   "multimodal-ai-system-001",
		SystemName: "Multimodal AI Governance Monitor",
		Generated:  time.Now().UTC(),
		Metrics: []MultimodalMetric{
			evaluateMetric("low_alignment_rate", 0.14, 0.18, 0.30),
			evaluateMetric("low_grounding_rate", 0.12, 0.18, 0.30),
			evaluateMetric("modality_conflict_rate", 0.09, 0.15, 0.25),
			evaluateMetric("privacy_control_failure_rate", 0.05, 0.08, 0.15),
			evaluateMetric("unsafe_action_block_rate", 0.04, 0.08, 0.16),
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
	http.HandleFunc("/multimodal-metrics", metricsHandler)

	log.Println("Multimodal AI governance monitor listening on http://localhost:8104")
	log.Println("Health:  http://localhost:8104/health")
	log.Println("Metrics: http://localhost:8104/multimodal-metrics")

	if err := http.ListenAndServe(":8104", nil); err != nil {
		log.Fatal(err)
	}
}
