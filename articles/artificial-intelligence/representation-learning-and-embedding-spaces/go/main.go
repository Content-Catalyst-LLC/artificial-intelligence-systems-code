package main

import (
	"encoding/json"
	"log"
	"net/http"
	"time"
)

type EmbeddingMetric struct {
	Name             string    `json:"name"`
	Value            float64   `json:"value"`
	WarningThreshold float64   `json:"warning_threshold"`
	ActionThreshold  float64   `json:"action_threshold"`
	Status           string    `json:"status"`
	UpdatedAt        time.Time `json:"updated_at"`
}

type EmbeddingSnapshot struct {
	SystemID   string            `json:"system_id"`
	SystemName string            `json:"system_name"`
	Generated  time.Time         `json:"generated_at"`
	Metrics    []EmbeddingMetric `json:"metrics"`
}

func evaluateMetric(name string, value float64, warning float64, action float64) EmbeddingMetric {
	status := "normal"

	if value >= action {
		status = "action"
	} else if value >= warning {
		status = "warning"
	}

	return EmbeddingMetric{
		Name:             name,
		Value:            value,
		WarningThreshold: warning,
		ActionThreshold:  action,
		Status:           status,
		UpdatedAt:        time.Now().UTC(),
	}
}

func currentSnapshot() EmbeddingSnapshot {
	return EmbeddingSnapshot{
		SystemID:   "embedding-system-001",
		SystemName: "Representation Learning and Embedding Governance Monitor",
		Generated:  time.Now().UTC(),
		Metrics: []EmbeddingMetric{
			evaluateMetric("low_similarity_query_share", 0.12, 0.20, 0.35),
			evaluateMetric("stale_embedding_share", 0.18, 0.25, 0.40),
			evaluateMetric("open_bias_review_count", 1.0, 2.0, 5.0),
			evaluateMetric("index_drift_score", 0.16, 0.25, 0.45),
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
	http.HandleFunc("/embedding-metrics", metricsHandler)

	log.Println("Embedding governance monitor listening on http://localhost:8098")
	log.Println("Health:  http://localhost:8098/health")
	log.Println("Metrics: http://localhost:8098/embedding-metrics")

	if err := http.ListenAndServe(":8098", nil); err != nil {
		log.Fatal(err)
	}
}
