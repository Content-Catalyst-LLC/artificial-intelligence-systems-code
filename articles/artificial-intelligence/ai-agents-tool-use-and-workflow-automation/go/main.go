package main

import (
	"encoding/json"
	"log"
	"net/http"
	"time"
)

type AgentMetric struct {
	Name             string    `json:"name"`
	Value            float64   `json:"value"`
	WarningThreshold float64   `json:"warning_threshold"`
	ActionThreshold  float64   `json:"action_threshold"`
	Status           string    `json:"status"`
	UpdatedAt        time.Time `json:"updated_at"`
}

type AgentSnapshot struct {
	SystemID   string        `json:"system_id"`
	SystemName string        `json:"system_name"`
	Generated  time.Time     `json:"generated_at"`
	Metrics    []AgentMetric `json:"metrics"`
}

func evaluateMetric(name string, value float64, warning float64, action float64) AgentMetric {
	status := "normal"

	if value >= action {
		status = "action"
	} else if value >= warning {
		status = "warning"
	}

	return AgentMetric{
		Name:             name,
		Value:            value,
		WarningThreshold: warning,
		ActionThreshold:  action,
		Status:           status,
		UpdatedAt:        time.Now().UTC(),
	}
}

func currentSnapshot() AgentSnapshot {
	return AgentSnapshot{
		SystemID:   "agent-workflow-system-001",
		SystemName: "AI Agent Workflow Governance Monitor",
		Generated:  time.Now().UTC(),
		Metrics: []AgentMetric{
			evaluateMetric("tool_call_failure_rate", 0.07, 0.10, 0.20),
			evaluateMetric("denied_action_attempt_rate", 0.04, 0.08, 0.15),
			evaluateMetric("failed_confirmation_rate", 0.03, 0.06, 0.12),
			evaluateMetric("prompt_injection_exposure_rate", 0.05, 0.10, 0.20),
			evaluateMetric("high_risk_tool_use_rate", 0.09, 0.15, 0.25),
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
	http.HandleFunc("/agent-metrics", metricsHandler)

	log.Println("AI agent governance monitor listening on http://localhost:8105")
	log.Println("Health:  http://localhost:8105/health")
	log.Println("Metrics: http://localhost:8105/agent-metrics")

	if err := http.ListenAndServe(":8105", nil); err != nil {
		log.Fatal(err)
	}
}
