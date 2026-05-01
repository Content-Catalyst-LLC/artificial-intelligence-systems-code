package main

import (
	"encoding/json"
	"log"
	"net/http"
	"time"
)

type ClinicalMetric struct {
	Name             string    `json:"name"`
	Value            float64   `json:"value"`
	WarningThreshold float64   `json:"warning_threshold"`
	ActionThreshold  float64   `json:"action_threshold"`
	Status           string    `json:"status"`
	UpdatedAt        time.Time `json:"updated_at"`
}

type ClinicalSnapshot struct {
	SystemID   string           `json:"system_id"`
	SystemName string           `json:"system_name"`
	Generated  time.Time        `json:"generated_at"`
	Metrics    []ClinicalMetric `json:"metrics"`
}

func evaluateMetric(name string, value float64, warning float64, action float64, lowerIsWorse bool) ClinicalMetric {
	status := "normal"

	if lowerIsWorse {
		if value <= action {
			status = "action"
		} else if value <= warning {
			status = "warning"
		}
	} else {
		if value >= action {
			status = "action"
		} else if value >= warning {
			status = "warning"
		}
	}

	return ClinicalMetric{
		Name:             name,
		Value:            value,
		WarningThreshold: warning,
		ActionThreshold:  action,
		Status:           status,
		UpdatedAt:        time.Now().UTC(),
	}
}

func currentSnapshot() ClinicalSnapshot {
	return ClinicalSnapshot{
		SystemID:   "clinical-ai-system-001",
		SystemName: "Clinical AI Governance Monitor",
		Generated:  time.Now().UTC(),
		Metrics: []ClinicalMetric{
			evaluateMetric("sensitivity", 0.78, 0.72, 0.65, true),
			evaluateMetric("specificity", 0.69, 0.60, 0.50, true),
			evaluateMetric("expected_calibration_error", 0.052, 0.080, 0.120, false),
			evaluateMetric("alert_rate", 0.31, 0.40, 0.55, false),
			evaluateMetric("false_negative_rate", 0.15, 0.20, 0.30, false),
			evaluateMetric("human_override_rate", 0.08, 0.15, 0.25, false),
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
	http.HandleFunc("/clinical-ai-metrics", metricsHandler)

	log.Println("Clinical AI governance monitor listening on http://localhost:8111")
	log.Println("Health:  http://localhost:8111/health")
	log.Println("Metrics: http://localhost:8111/clinical-ai-metrics")

	if err := http.ListenAndServe(":8111", nil); err != nil {
		log.Fatal(err)
	}
}
