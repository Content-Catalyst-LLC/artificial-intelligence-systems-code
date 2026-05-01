package main

import (
	"encoding/json"
	"log"
	"net/http"
	"time"
)

type PortfolioMetric struct {
	Name             string    `json:"name"`
	Value            float64   `json:"value"`
	WarningThreshold float64   `json:"warning_threshold"`
	ActionThreshold  float64   `json:"action_threshold"`
	Status           string    `json:"status"`
	UpdatedAt        time.Time `json:"updated_at"`
}

type PortfolioSnapshot struct {
	PortfolioID   string            `json:"portfolio_id"`
	PortfolioName string            `json:"portfolio_name"`
	Generated     time.Time         `json:"generated_at"`
	Metrics       []PortfolioMetric `json:"metrics"`
}

func evaluateMetric(name string, value float64, warning float64, action float64) PortfolioMetric {
	status := "normal"

	if value >= action {
		status = "action"
	} else if value >= warning {
		status = "warning"
	}

	return PortfolioMetric{
		Name:             name,
		Value:            value,
		WarningThreshold: warning,
		ActionThreshold:  action,
		Status:           status,
		UpdatedAt:        time.Now().UTC(),
	}
}

func currentSnapshot() PortfolioSnapshot {
	return PortfolioSnapshot{
		PortfolioID:   "ai-systems-portfolio-001",
		PortfolioName: "AI Systems Discipline Governance Monitor",
		Generated:     time.Now().UTC(),
		Metrics: []PortfolioMetric{
			evaluateMetric("systems_requiring_review_share", 0.22, 0.25, 0.40),
			evaluateMetric("high_risk_low_oversight_count", 2.0, 3.0, 8.0),
			evaluateMetric("low_monitoring_system_share", 0.18, 0.25, 0.40),
			evaluateMetric("open_ai_incidents", 1.0, 2.0, 5.0),
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
	http.HandleFunc("/portfolio-metrics", metricsHandler)

	log.Println("AI systems discipline monitor listening on http://localhost:8097")
	log.Println("Health:  http://localhost:8097/health")
	log.Println("Metrics: http://localhost:8097/portfolio-metrics")

	if err := http.ListenAndServe(":8097", nil); err != nil {
		log.Fatal(err)
	}
}
