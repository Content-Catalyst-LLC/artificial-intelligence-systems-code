package main

import (
	"encoding/json"
	"log"
	"net/http"
	"time"
)

type RagMetric struct {
	Name             string    `json:"name"`
	Value            float64   `json:"value"`
	WarningThreshold float64   `json:"warning_threshold"`
	ActionThreshold  float64   `json:"action_threshold"`
	Status           string    `json:"status"`
	UpdatedAt        time.Time `json:"updated_at"`
}

type RagSnapshot struct {
	SystemID   string      `json:"system_id"`
	SystemName string      `json:"system_name"`
	Generated  time.Time   `json:"generated_at"`
	Metrics    []RagMetric `json:"metrics"`
}

func evaluateMetric(name string, value float64, warning float64, action float64) RagMetric {
	status := "normal"

	if value >= action {
		status = "action"
	} else if value >= warning {
		status = "warning"
	}

	return RagMetric{
		Name:             name,
		Value:            value,
		WarningThreshold: warning,
		ActionThreshold:  action,
		Status:           status,
		UpdatedAt:        time.Now().UTC(),
	}
}

func currentSnapshot() RagSnapshot {
	return RagSnapshot{
		SystemID:   "rag-knowledge-system-001",
		SystemName: "RAG Knowledge System Governance Monitor",
		Generated:  time.Now().UTC(),
		Metrics: []RagMetric{
			evaluateMetric("unsupported_citation_rate", 0.07, 0.10, 0.20),
			evaluateMetric("low_grounding_rate", 0.12, 0.18, 0.30),
			evaluateMetric("stale_source_rate", 0.09, 0.15, 0.25),
			evaluateMetric("prompt_injection_detection_rate", 0.03, 0.08, 0.15),
			evaluateMetric("access_control_denial_rate", 0.04, 0.08, 0.16),
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
	http.HandleFunc("/rag-metrics", metricsHandler)

	log.Println("RAG knowledge system monitor listening on http://localhost:8103")
	log.Println("Health:  http://localhost:8103/health")
	log.Println("Metrics: http://localhost:8103/rag-metrics")

	if err := http.ListenAndServe(":8103", nil); err != nil {
		log.Fatal(err)
	}
}
