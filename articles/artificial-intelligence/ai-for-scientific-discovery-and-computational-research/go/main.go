package main

import (
	"encoding/json"
	"log"
	"net/http"
	"time"
)

type ResearchMetric struct {
	Name             string    `json:"name"`
	Value            float64   `json:"value"`
	WarningThreshold float64   `json:"warning_threshold"`
	ActionThreshold  float64   `json:"action_threshold"`
	Status           string    `json:"status"`
	UpdatedAt        time.Time `json:"updated_at"`
}

type ResearchSnapshot struct {
	ProjectID   string           `json:"project_id"`
	ProjectName string           `json:"project_name"`
	Generated   time.Time        `json:"generated_at"`
	Metrics     []ResearchMetric `json:"metrics"`
}

func evaluateMetric(name string, value float64, warning float64, action float64) ResearchMetric {
	status := "normal"

	if value >= action {
		status = "action"
	} else if value >= warning {
		status = "warning"
	}

	return ResearchMetric{
		Name:             name,
		Value:            value,
		WarningThreshold: warning,
		ActionThreshold:  action,
		Status:           status,
		UpdatedAt:        time.Now().UTC(),
	}
}

func currentSnapshot() ResearchSnapshot {
	return ResearchSnapshot{
		ProjectID:   "scientific-discovery-001",
		ProjectName: "AI Scientific Discovery Monitor",
		Generated:   time.Now().UTC(),
		Metrics: []ResearchMetric{
			evaluateMetric("open_validation_failures", 1.0, 2.0, 5.0),
			evaluateMetric("high_uncertainty_candidate_share", 0.12, 0.25, 0.40),
			evaluateMetric("reproducibility_failure_rate", 0.03, 0.05, 0.10),
			evaluateMetric("unreviewed_hypothesis_count", 4.0, 8.0, 15.0),
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
	http.HandleFunc("/research-metrics", metricsHandler)

	log.Println("Scientific discovery monitor listening on http://localhost:8094")
	log.Println("Health:  http://localhost:8094/health")
	log.Println("Metrics: http://localhost:8094/research-metrics")

	if err := http.ListenAndServe(":8094", nil); err != nil {
		log.Fatal(err)
	}
}
