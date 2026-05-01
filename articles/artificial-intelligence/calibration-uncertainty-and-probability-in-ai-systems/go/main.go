package main

import (
	"encoding/json"
	"log"
	"net/http"
	"time"
)

type CalibrationMetric struct {
	Name             string    `json:"name"`
	Value            float64   `json:"value"`
	WarningThreshold float64   `json:"warning_threshold"`
	ActionThreshold  float64   `json:"action_threshold"`
	Status           string    `json:"status"`
	UpdatedAt        time.Time `json:"updated_at"`
}

type CalibrationSnapshot struct {
	SystemID   string              `json:"system_id"`
	SystemName string              `json:"system_name"`
	Generated  time.Time           `json:"generated_at"`
	Metrics    []CalibrationMetric `json:"metrics"`
}

func evaluateMetric(name string, value float64, warning float64, action float64) CalibrationMetric {
	status := "normal"

	if value >= action {
		status = "action"
	} else if value >= warning {
		status = "warning"
	}

	return CalibrationMetric{
		Name:             name,
		Value:            value,
		WarningThreshold: warning,
		ActionThreshold:  action,
		Status:           status,
		UpdatedAt:        time.Now().UTC(),
	}
}

func currentSnapshot() CalibrationSnapshot {
	return CalibrationSnapshot{
		SystemID:   "calibration-uncertainty-system-001",
		SystemName: "Calibration and Uncertainty Governance Monitor",
		Generated:  time.Now().UTC(),
		Metrics: []CalibrationMetric{
			evaluateMetric("expected_calibration_error", 0.064, 0.080, 0.120),
			evaluateMetric("brier_score", 0.196, 0.220, 0.280),
			evaluateMetric("negative_log_likelihood", 0.612, 0.700, 0.900),
			evaluateMetric("mean_entropy", 0.482, 0.620, 0.700),
			evaluateMetric("human_review_rate", 0.426, 0.500, 0.650),
			evaluateMetric("slice_calibration_gap", 0.072, 0.080, 0.120),
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
	http.HandleFunc("/calibration-metrics", metricsHandler)

	log.Println("Calibration and uncertainty monitor listening on http://localhost:8108")
	log.Println("Health:  http://localhost:8108/health")
	log.Println("Metrics: http://localhost:8108/calibration-metrics")

	if err := http.ListenAndServe(":8108", nil); err != nil {
		log.Fatal(err)
	}
}
