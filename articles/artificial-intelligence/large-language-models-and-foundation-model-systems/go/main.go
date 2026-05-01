package main

import (
	"encoding/json"
	"log"
	"net/http"
	"time"
)

type LlmMetric struct {
	Name             string    `json:"name"`
	Value            float64   `json:"value"`
	WarningThreshold float64   `json:"warning_threshold"`
	ActionThreshold  float64   `json:"action_threshold"`
	Status           string    `json:"status"`
	UpdatedAt        time.Time `json:"updated_at"`
}

type LlmSnapshot struct {
	SystemID   string      `json:"system_id"`
	SystemName string      `json:"system_name"`
	Generated  time.Time   `json:"generated_at"`
	Metrics    []LlmMetric `json:"metrics"`
}

func evaluateMetric(name string, value float64, warning float64, action float64) LlmMetric {
	status := "normal"

	if value >= action {
		status = "action"
	} else if value >= warning {
		status = "warning"
	}

	return LlmMetric{
		Name:             name,
		Value:            value,
		WarningThreshold: warning,
		ActionThreshold:  action,
		Status:           status,
		UpdatedAt:        time.Now().UTC(),
	}
}

func currentSnapshot() LlmSnapshot {
	return LlmSnapshot{
		SystemID:   "llm-foundation-system-001",
		SystemName: "LLM Foundation Model System Governance Monitor",
		Generated:  time.Now().UTC(),
		Metrics: []LlmMetric{
			evaluateMetric("low_grounding_rate", 0.16, 0.20, 0.35),
			evaluateMetric("prompt_injection_failure_rate", 0.07, 0.10, 0.20),
			evaluateMetric("privacy_control_failure_rate", 0.05, 0.08, 0.15),
			evaluateMetric("mean_latency_seconds", 3.8, 6.0, 10.0),
			evaluateMetric("high_risk_unreviewed_count", 1.0, 2.0, 5.0),
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
	http.HandleFunc("/llm-system-metrics", metricsHandler)

	log.Println("LLM foundation model system monitor listening on http://localhost:8102")
	log.Println("Health:  http://localhost:8102/health")
	log.Println("Metrics: http://localhost:8102/llm-system-metrics")

	if err := http.ListenAndServe(":8102", nil); err != nil {
		log.Fatal(err)
	}
}
