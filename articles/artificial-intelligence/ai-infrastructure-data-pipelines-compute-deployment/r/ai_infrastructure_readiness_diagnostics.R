# AI Infrastructure: Data Pipelines, Compute, and Deployment Systems Diagnostics
#
# This educational workflow simulates:
# - infrastructure readiness scoring
# - pipeline reliability
# - serving latency analysis
# - MLOps risk scoring

components <- data.frame(
  component = c(
    "data_pipeline",
    "feature_store",
    "training_cluster",
    "model_registry",
    "serving_layer",
    "observability",
    "security_controls",
    "governance_controls"
  ),
  readiness_score = c(0.82, 0.76, 0.78, 0.84, 0.80, 0.72, 0.74, 0.70),
  technical_debt = c(0.28, 0.34, 0.30, 0.20, 0.25, 0.42, 0.36, 0.40),
  criticality = c(0.95, 0.90, 0.92, 0.82, 0.94, 0.88, 0.90, 0.92)
)

components$weighted_risk <- components$technical_debt * components$criticality

components$priority <- ifelse(
  components$weighted_risk >= 0.35,
  "high",
  ifelse(components$weighted_risk >= 0.25, "medium", "low")
)

pipeline_tasks <- data.frame(
  task = c(
    "ingest_raw_data",
    "validate_schema",
    "transform_records",
    "build_features",
    "train_model",
    "evaluate_model",
    "register_model",
    "deploy_model",
    "monitor_predictions"
  ),
  duration_minutes = c(18, 7, 24, 16, 95, 20, 6, 12, 5),
  failure_probability = c(0.03, 0.02, 0.05, 0.04, 0.06, 0.03, 0.01, 0.02, 0.02)
)

pipeline_reliability <- prod(1 - pipeline_tasks$failure_probability)

serving <- data.frame(
  service = "risk_model_api",
  required_qps = 1200,
  throughput_per_replica = 150,
  feature_latency_ms = 45,
  model_latency_ms = 80,
  network_latency_ms = 35,
  postprocess_latency_ms = 20,
  latency_budget_ms = 200
)

serving$required_replicas <- ceiling(
  serving$required_qps / serving$throughput_per_replica
)

serving$total_latency_ms <-
  serving$feature_latency_ms +
  serving$model_latency_ms +
  serving$network_latency_ms +
  serving$postprocess_latency_ms

serving$meets_latency_budget <-
  serving$total_latency_ms <= serving$latency_budget_ms

summary_table <- data.frame(
  metric = c(
    "mean_readiness_score",
    "mean_weighted_risk",
    "pipeline_total_duration_minutes",
    "pipeline_reliability",
    "serving_required_replicas",
    "serving_total_latency_ms",
    "serving_meets_latency_budget"
  ),
  value = c(
    mean(components$readiness_score),
    mean(components$weighted_risk),
    sum(pipeline_tasks$duration_minutes),
    pipeline_reliability,
    serving$required_replicas[1],
    serving$total_latency_ms[1],
    as.numeric(serving$meets_latency_budget[1])
  )
)

dir.create("../outputs", recursive = TRUE, showWarnings = FALSE)

write.csv(components, "../outputs/r_ai_infrastructure_components.csv", row.names = FALSE)
write.csv(pipeline_tasks, "../outputs/r_ai_pipeline_tasks.csv", row.names = FALSE)
write.csv(serving, "../outputs/r_ai_serving_capacity.csv", row.names = FALSE)
write.csv(summary_table, "../outputs/r_ai_infrastructure_summary.csv", row.names = FALSE)

print(components[order(-components$weighted_risk), ])
print(serving)
print(summary_table)
