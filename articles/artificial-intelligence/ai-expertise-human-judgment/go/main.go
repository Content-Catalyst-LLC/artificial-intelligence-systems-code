package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
)

type ExpertReviewStatus struct {
	SystemName            string  `json:"system_name"`
	AIExpertDisagreement float64 `json:"ai_expert_disagreement"`
	AutomationBiasRate   float64 `json:"automation_bias_rate"`
	ReviewRequiredRate   float64 `json:"review_required_rate"`
	Status                string  `json:"status"`
}

func statusHandler(w http.ResponseWriter, r *http.Request) {
	status := ExpertReviewStatus{
		SystemName:            "synthetic-expert-decision-support-system",
		AIExpertDisagreement: 0.24,
		AutomationBiasRate:   0.18,
		ReviewRequiredRate:   0.31,
		Status:               "monitoring_required",
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(status)
}

func main() {
	http.HandleFunc("/expertise/status", statusHandler)
	fmt.Println("Expertise monitoring service running on http://localhost:8080/expertise/status")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
