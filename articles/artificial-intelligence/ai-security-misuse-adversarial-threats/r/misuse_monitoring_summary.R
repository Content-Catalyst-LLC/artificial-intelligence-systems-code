# Defensive misuse monitoring and residual-risk summary.
# This workflow uses synthetic data and does not implement attack techniques.

set.seed(42)

article_dir <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."), mustWork = FALSE)
output_dir <- file.path(article_dir, "outputs")
dir.create(output_dir, showWarnings = FALSE, recursive = TRUE)

n <- 500

events <- data.frame(
  event_id = 1:n,
  unusual_query_score = runif(n, 0, 1),
  tool_call_intensity = runif(n, 0, 1),
  sensitive_output_signal = runif(n, 0, 1),
  permission_risk = runif(n, 0, 1),
  control_strength = runif(n, 0.30, 0.90)
)

events$misuse_signal <-
  0.30 * events$unusual_query_score +
  0.25 * events$tool_call_intensity +
  0.25 * events$sensitive_output_signal +
  0.20 * events$permission_risk

events$residual_risk <- events$misuse_signal * (1 - events$control_strength)

events$risk_band <- ifelse(
  events$residual_risk < 0.15,
  "low",
  ifelse(events$residual_risk < 0.30, "moderate", "high")
)

summary_table <- aggregate(
  cbind(misuse_signal, residual_risk) ~ risk_band,
  data = events,
  FUN = mean
)

write.csv(events, file.path(output_dir, "synthetic_misuse_monitoring_events.csv"), row.names = FALSE)
write.csv(summary_table, file.path(output_dir, "misuse_monitoring_summary.csv"), row.names = FALSE)

print(summary_table)
