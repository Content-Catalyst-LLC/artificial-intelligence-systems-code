# Systemic Risk, Feedback Loops, and Cascading Failures Diagnostics
#
# This educational workflow simulates:
# - component dependency intensity
# - feedback intensity
# - coupling level
# - concentration exposure
# - systemic-risk scoring

set.seed(42)

n <- 24

risk_data <- data.frame(
  component_id = paste0("component_", sprintf("%02d", 1:n)),
  dependency_intensity = runif(n, 0.05, 1.00),
  feedback_intensity = runif(n, 0.00, 1.00),
  coupling_level = runif(n, 0.00, 1.00),
  provider_concentration = runif(n, 0.10, 1.00),
  buffer_capacity = runif(n, 0.00, 0.80)
)

risk_data$systemic_risk_score <-
  0.25 * risk_data$dependency_intensity +
  0.25 * risk_data$feedback_intensity +
  0.20 * risk_data$coupling_level +
  0.20 * risk_data$provider_concentration -
  0.20 * risk_data$buffer_capacity

risk_data$risk_band <- ifelse(
  risk_data$systemic_risk_score < 0.25,
  "low",
  ifelse(
    risk_data$systemic_risk_score < 0.50,
    "moderate",
    "high"
  )
)

summary_table <- aggregate(
  cbind(
    dependency_intensity,
    feedback_intensity,
    coupling_level,
    provider_concentration,
    buffer_capacity,
    systemic_risk_score
  ) ~ risk_band,
  data = risk_data,
  FUN = mean
)

dir.create("../outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(risk_data, "../outputs/r_systemic_ai_risk_component_scores.csv", row.names = FALSE)
write.csv(summary_table, "../outputs/r_systemic_ai_risk_summary.csv", row.names = FALSE)

print(risk_data)
print(summary_table)
