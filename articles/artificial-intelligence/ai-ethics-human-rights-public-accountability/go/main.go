package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
)

// PublicAccountabilityStatus summarizes rights-governance monitoring.
type PublicAccountabilityStatus struct {
	SystemName          string  `json:"system_name"`
	AdverseOutcomeRate float64 `json:"adverse_outcome_rate"`
	AppealRate         float64 `json:"appeal_rate"`
	RemedyRate         float64 `json:"remedy_rate"`
	MeanRemedyDays     float64 `json:"mean_remedy_days"`
	Status             string  `json:"status"`
}

func statusHandler(w http.ResponseWriter, r *http.Request) {
	status := PublicAccountabilityStatus{
		SystemName:          "synthetic-public-benefits-review",
		AdverseOutcomeRate: 0.22,
		AppealRate:         0.12,
		RemedyRate:         0.35,
		MeanRemedyDays:     18.0,
		Status:             "monitoring_required",
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(status)
}

func main() {
	http.HandleFunc("/public-accountability/status", statusHandler)
	fmt.Println("Public accountability monitoring service running on http://localhost:8080/public-accountability/status")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
