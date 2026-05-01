package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
)

// WorkforceAIStatus summarizes workplace AI monitoring signals.
type WorkforceAIStatus struct {
	SystemName              string  `json:"system_name"`
	MeanAIExposure         float64 `json:"mean_ai_exposure"`
	MeanJobQuality         float64 `json:"mean_job_quality"`
	MeanTrainingAccess     float64 `json:"mean_training_access"`
	MeanMonitoringBurden   float64 `json:"mean_monitoring_burden"`
	TransitionPriorityRate float64 `json:"transition_priority_rate"`
	Status                 string  `json:"status"`
}

func statusHandler(w http.ResponseWriter, r *http.Request) {
	status := WorkforceAIStatus{
		SystemName:              "synthetic-workplace-ai-system",
		MeanAIExposure:         0.58,
		MeanJobQuality:         0.52,
		MeanTrainingAccess:     0.46,
		MeanMonitoringBurden:   0.61,
		TransitionPriorityRate: 0.24,
		Status:                 "worker_consultation_required",
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(status)
}

func main() {
	http.HandleFunc("/workforce-ai/status", statusHandler)
	fmt.Println("Workforce AI governance service running on http://localhost:8080/workforce-ai/status")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
