# Economics of AI Systems and Platform Power Diagnostics
#
# This educational workflow simulates:
# - AI ecosystem actors
# - concentration scoring
# - platform-power scoring
# - value-capture shares
# - dependency-risk diagnostics

actors <- data.frame(
  actor = c(
    "cloud_compute_provider",
    "foundation_model_provider",
    "enterprise_application_firm",
    "downstream_users"
  ),
  layer = c(
    "infrastructure",
    "model",
    "application",
    "user"
  ),
  market_share = c(0.36, 0.28, 0.18, 0.18),
  data_control = c(0.45, 0.70, 0.55, 0.20),
  distribution_control = c(0.55, 0.60, 0.45, 0.10),
  switching_costs = c(0.80, 0.65, 0.40, 0.25),
  gatekeeping_power = c(0.85, 0.72, 0.35, 0.10),
  captured_surplus = c(35, 25, 20, 20)
)

concentration_score <- sum(actors$market_share^2)

actors$platform_power_score <-
  0.25 * actors$market_share +
  0.20 * actors$data_control +
  0.20 * actors$distribution_control +
  0.20 * actors$switching_costs +
  0.15 * actors$gatekeeping_power

actors$value_capture_share <-
  actors$captured_surplus / sum(actors$captured_surplus)

actors$dependency_risk <-
  0.40 * actors$switching_costs +
  0.35 * actors$gatekeeping_power +
  0.25 * actors$distribution_control

summary_table <- aggregate(
  cbind(
    market_share,
    data_control,
    distribution_control,
    switching_costs,
    gatekeeping_power,
    platform_power_score,
    value_capture_share,
    dependency_risk
  ) ~ layer,
  data = actors,
  FUN = mean
)

dir.create("../outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(actors, "../outputs/r_ai_platform_power_scores.csv", row.names = FALSE)
write.csv(summary_table, "../outputs/r_ai_platform_power_summary.csv", row.names = FALSE)

print(concentration_score)
print(actors[order(-actors$platform_power_score), ])
print(summary_table)
