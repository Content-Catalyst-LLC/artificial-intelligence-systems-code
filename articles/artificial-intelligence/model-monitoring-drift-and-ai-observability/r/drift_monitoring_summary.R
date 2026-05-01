# Model Monitoring, Drift, and AI Observability
# R workflow: drift and monitoring summary.

set.seed(42)

article_dir <- normalizePath(file.path(getwd(), "articles/artificial-intelligence/model-monitoring-drift-and-ai-observability"), mustWork = FALSE)

if (!dir.exists(article_dir)) {
  article_dir <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."), mustWork = FALSE)
}

output_dir <- file.path(article_dir, "outputs")

if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

n_batches <- 24

monitoring <- data.frame(
  batch = 1:n_batches,
  psi_feature_a = pmax(0, rnorm(n_batches, mean = seq(0.02, 0.32, length.out = n_batches), sd = 0.04)),
  psi_feature_b = pmax(0, rnorm(n_batches, mean = seq(0.01, 0.26, length.out = n_batches), sd = 0.04)),
  psi_feature_c = pmax(0, rnorm(n_batches, mean = seq(0.02, 0.22, length.out = n_batches), sd = 0.03)),
  prediction_psi = pmax(0, rnorm(n_batches, mean = seq(0.02, 0.28, length.out = n_batches), sd = 0.05)),
  accuracy = pmin(0.92, pmax(0.65, rnorm(n_batches, mean = seq(0.88, 0.76, length.out = n_batches), sd = 0.03))),
  latency_ms = rgamma(n_batches, shape = 2.6, scale = 130) + seq(0, 240, length.out = n_batches),
  missing_rate = pmax(0, rnorm(n_batches, mean = seq(0.01, 0.055, length.out = n_batches), sd = 0.01)),
  incident_count = rpois(n_batches, lambda = seq(0.1, 1.7, length.out = n_batches))
)

monitoring$max_feature_psi <- pmax(
  monitoring$psi_feature_a,
  monitoring$psi_feature_b,
  monitoring$psi_feature_c
)

monitoring$performance_degradation <- pmax(0, 0.88 - monitoring$accuracy)

monitoring$drift_signal <- pmin(
  1.5,
  0.45 * monitoring$max_feature_psi +
    0.35 * monitoring$prediction_psi +
    0.20 * monitoring$missing_rate * 5
)

monitoring$operational_signal <- pmin(
  1.5,
  (monitoring$latency_ms / 1200) + (monitoring$incident_count / 8)
)

monitoring$observability_risk <- 0.35 * monitoring$drift_signal +
  0.30 * monitoring$performance_degradation +
  0.20 * monitoring$operational_signal +
  0.15 * pmin(monitoring$missing_rate * 5, 1)

monitoring$alert_level <- ifelse(
  monitoring$observability_risk > 0.60,
  "incident_review",
  ifelse(
    monitoring$observability_risk > 0.40,
    "action_required",
    ifelse(monitoring$observability_risk > 0.25, "warning", "normal")
  )
)

monitoring$review_required <- monitoring$alert_level %in% c("action_required", "incident_review") |
  monitoring$max_feature_psi > 0.25 |
  monitoring$prediction_psi > 0.25 |
  monitoring$accuracy < 0.78 |
  monitoring$incident_count >= 2

governance_summary <- data.frame(
  batches_reviewed = nrow(monitoring),
  review_required = sum(monitoring$review_required),
  incident_review_batches = sum(monitoring$alert_level == "incident_review"),
  max_feature_psi_observed = max(monitoring$max_feature_psi),
  max_prediction_psi_observed = max(monitoring$prediction_psi),
  minimum_accuracy_observed = min(monitoring$accuracy),
  mean_latency_ms = mean(monitoring$latency_ms),
  total_incidents = sum(monitoring$incident_count),
  mean_observability_risk = mean(monitoring$observability_risk)
)

alert_summary <- aggregate(
  cbind(
    max_feature_psi,
    prediction_psi,
    accuracy,
    latency_ms,
    incident_count,
    observability_risk,
    review_required
  ) ~ alert_level,
  data = monitoring,
  FUN = mean
)

write.csv(monitoring, file.path(output_dir, "r_observability_monitoring_records.csv"), row.names = FALSE)
write.csv(alert_summary, file.path(output_dir, "r_observability_alert_summary.csv"), row.names = FALSE)
write.csv(governance_summary, file.path(output_dir, "r_observability_governance_summary.csv"), row.names = FALSE)

print("Monitoring records")
print(monitoring)

print("Alert summary")
print(alert_summary)

print("Governance summary")
print(governance_summary)
