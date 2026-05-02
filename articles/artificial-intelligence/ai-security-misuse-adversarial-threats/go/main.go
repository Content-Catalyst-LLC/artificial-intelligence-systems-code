package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
)

// AISecurityStatus summarizes defensive monitoring signals.
type AISecurityStatus struct {
	SystemName       string  `json:"system_name"`
	MeanMisuseScore float64 `json:"mean_misuse_score"`
	ResidualRisk    float64 `json:"residual_risk"`
	OpenIncidents   int     `json:"open_incidents"`
	ReviewFlagRate  float64 `json:"review_flag_rate"`
	Status           string  `json:"status"`
}

func statusHandler(w http.ResponseWriter, r *http.Request) {
	status := AISecurityStatus{
		SystemName:       "synthetic-ai-assistant",
		MeanMisuseScore: 0.31,
		ResidualRisk:    0.14,
		OpenIncidents:   1,
		ReviewFlagRate:  0.08,
		Status:          "monitoring_required",
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(status)
}

func main() {
	http.HandleFunc("/ai-security/status", statusHandler)
	fmt.Println("AI security monitoring service running on http://localhost:8080/ai-security/status")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
