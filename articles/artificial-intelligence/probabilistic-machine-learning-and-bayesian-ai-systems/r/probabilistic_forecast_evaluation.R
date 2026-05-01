# Probabilistic Machine Learning and Bayesian AI Systems
# R workflow: probabilistic forecast evaluation.

set.seed(42)

article_dir <- normalizePath(file.path(getwd(), "articles/artificial-intelligence/probabilistic-machine-learning-and-bayesian-ai-systems"), mustWork = FALSE)

if (!dir.exists(article_dir)) {
  article_dir <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."), mustWork = FALSE)
}

output_dir <- file.path(article_dir, "outputs")

if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

n <- 200

records <- data.frame(
  case_id = paste0("CASE-", sprintf("%03d", 1:n)),
  risk_group = sample(c("low", "medium", "high"), size = n, replace = TRUE, prob = c(0.45, 0.40, 0.15)),
  evidence_quality = runif(n, min = 0.35, max = 0.98)
)

records$true_probability <- ifelse(
  records$risk_group == "low",
  runif(n, min = 0.02, max = 0.12),
  ifelse(
    records$risk_group == "medium",
    runif(n, min = 0.10, max = 0.28),
    runif(n, min = 0.25, max = 0.55)
  )
)

records$outcome <- rbinom(n, size = 1, prob = records$true_probability)

records$predicted_probability <- records$true_probability +
  rnorm(n, mean = 0, sd = 0.05) +
  0.04 * (1 - records$evidence_quality)

records$predicted_probability <- pmin(pmax(records$predicted_probability, 0.001), 0.999)

records$predictive_entropy <- -(
  records$predicted_probability * log(records$predicted_probability) +
    (1 - records$predicted_probability) * log(1 - records$predicted_probability)
)

records$brier_component <- (records$predicted_probability - records$outcome)^2

records$review_required <- records$predicted_probability > 0.25 |
  records$predictive_entropy > 0.60 |
  records$evidence_quality < 0.50

records$probability_bin <- cut(
  records$predicted_probability,
  breaks = seq(0, 1, by = 0.10),
  include.lowest = TRUE
)

calibration_summary <- aggregate(
  cbind(predicted_probability, outcome, predictive_entropy, review_required) ~ probability_bin,
  data = records,
  FUN = mean
)

calibration_summary$calibration_error <- abs(
  calibration_summary$predicted_probability - calibration_summary$outcome
)

group_summary <- aggregate(
  cbind(predicted_probability, outcome, brier_component, predictive_entropy, review_required) ~ risk_group,
  data = records,
  FUN = mean
)

governance_summary <- data.frame(
  cases_reviewed = nrow(records),
  brier_score = mean(records$brier_component),
  mean_predicted_probability = mean(records$predicted_probability),
  mean_observed_rate = mean(records$outcome),
  mean_calibration_error = mean(calibration_summary$calibration_error),
  review_required = sum(records$review_required)
)

write.csv(records, file.path(output_dir, "r_probabilistic_forecast_records.csv"), row.names = FALSE)
write.csv(calibration_summary, file.path(output_dir, "r_calibration_summary.csv"), row.names = FALSE)
write.csv(group_summary, file.path(output_dir, "r_group_forecast_summary.csv"), row.names = FALSE)
write.csv(governance_summary, file.path(output_dir, "r_probabilistic_governance_summary.csv"), row.names = FALSE)

print("Calibration summary")
print(calibration_summary)

print("Risk group summary")
print(group_summary)

print("Governance summary")
print(governance_summary)
