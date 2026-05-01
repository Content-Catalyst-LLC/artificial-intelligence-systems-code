package main

import (
	"encoding/json"
	"log"
	"net/http"
	"time"
)

type ExplanationMetric struct {
	Name      string  `json:"name"`
	Value     float64 `json:"value"`
	Threshold float64 `json:"threshold"`
	Status    string  `json:"status"`
}

type ExplanationAuditSummary struct {
	SystemID       string              `json:"system_id"`
	SystemName     string              `json:"system_name"`
	GeneratedAt    time.Time           `json:"generated_at"`
	AuditMetrics   []ExplanationMetric `json:"audit_metrics"`
	ReviewRequired bool                `json:"review_required"`
}

func evaluate(name string, value float64, threshold float64, higherIsBetter bool) ExplanationMetric {
	status := "pass"

	if higherIsBetter && value < threshold {
		status = "review"
	}

	if !higherIsBetter && value > threshold {
		status = "review"
	}

	return ExplanationMetric{
		Name:      name,
		Value:     value,
		Threshold: threshold,
		Status:    status,
	}
}

func currentAuditSummary() ExplanationAuditSummary {
	metrics := []ExplanationMetric{
		evaluate("mean_explanation_stability", 0.78, 0.70, true),
		evaluate("mean_explanation_fidelity", 0.86, 0.80, true),
		evaluate("counterfactual_actionability", 0.74, 0.70, true),
		evaluate("sensitive_feature_change_rate", 0.02, 0.05, false),
	}

	reviewRequired := false

	for _, metric := range metrics {
		if metric.Status == "review" {
			reviewRequired = true
		}
	}

	return ExplanationAuditSummary{
		SystemID:       "xai-system-001",
		SystemName:     "Explainable AI Audit Service",
		GeneratedAt:    time.Now().UTC(),
		AuditMetrics:   metrics,
		ReviewRequired: reviewRequired,
	}
}

func healthHandler(writer http.ResponseWriter, request *http.Request) {
	writer.Header().Set("Content-Type", "application/json")
	json.NewEncoder(writer).Encode(map[string]string{
		"status": "ok",
		"time":   time.Now().UTC().Format(time.RFC3339),
	})
}

func auditHandler(writer http.ResponseWriter, request *http.Request) {
	writer.Header().Set("Content-Type", "application/json")
	json.NewEncoder(writer).Encode(currentAuditSummary())
}

func main() {
	http.HandleFunc("/health", healthHandler)
	http.HandleFunc("/explanation-audit", auditHandler)

	log.Println("Explainability audit service listening on http://localhost:8091")
	log.Println("Health: http://localhost:8091/health")
	log.Println("Audit:  http://localhost:8091/explanation-audit")

	if err := http.ListenAndServe(":8091", nil); err != nil {
		log.Fatal(err)
	}
}
