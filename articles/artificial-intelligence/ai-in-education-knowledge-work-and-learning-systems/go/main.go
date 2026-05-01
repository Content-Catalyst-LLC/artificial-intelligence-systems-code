package main

import (
	"encoding/json"
	"log"
	"net/http"
	"time"
)

type LearningMetric struct {
	Name             string    `json:"name"`
	Value            float64   `json:"value"`
	WarningThreshold float64   `json:"warning_threshold"`
	ActionThreshold  float64   `json:"action_threshold"`
	LowerIsWorse     bool      `json:"lower_is_worse"`
	Status           string    `json:"status"`
	UpdatedAt        time.Time `json:"updated_at"`
}

type LearningSnapshot struct {
	SystemID   string           `json:"system_id"`
	SystemName string           `json:"system_name"`
	Generated  time.Time        `json:"generated_at"`
	Metrics    []LearningMetric `json:"metrics"`
}

func evaluateMetric(name string, value float64, warning float64, action float64, lowerIsWorse bool) LearningMetric {
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

	return LearningMetric{
		Name:             name,
		Value:            value,
		WarningThreshold: warning,
		ActionThreshold:  action,
		LowerIsWorse:     lowerIsWorse,
		Status:           status,
		UpdatedAt:        time.Now().UTC(),
	}
}

func currentSnapshot() LearningSnapshot {
	return LearningSnapshot{
		SystemID:   "learning-ai-system-001",
		SystemName: "Education AI and Learning-System Governance Monitor",
		Generated:  time.Now().UTC(),
		Metrics: []LearningMetric{
			evaluateMetric("learning_gain", 0.13, 0.05, 0.02, true),
			evaluateMetric("independent_transfer", 0.64, 0.55, 0.45, true),
			evaluateMetric("assistance_gap", 0.12, 0.18, 0.25, false),
			evaluateMetric("feedback_quality", 0.68, 0.45, 0.35, true),
			evaluateMetric("privacy_risk", 0.28, 0.45, 0.60, false),
			evaluateMetric("assessment_substitution_risk", 0.31, 0.50, 0.65, false),
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
	http.HandleFunc("/learning-ai-metrics", metricsHandler)

	log.Println("Learning-system governance monitor listening on http://localhost:8112")
	log.Println("Health:  http://localhost:8112/health")
	log.Println("Metrics: http://localhost:8112/learning-ai-metrics")

	if err := http.ListenAndServe(":8112", nil); err != nil {
		log.Fatal(err)
	}
}
