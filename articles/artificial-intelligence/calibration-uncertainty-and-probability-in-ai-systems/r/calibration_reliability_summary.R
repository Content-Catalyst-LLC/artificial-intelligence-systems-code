# Calibration, Uncertainty, and Probability in AI Systems
# R workflow: calibration summary and reliability review.

set.seed(42)

article_dir <- normalizePath(file.path(getwd(), "articles/artificial-intelligence/calibration-uncertainty-and-probability-in-ai-systems"), mustWork = FALSE)

if (!dir.exists(article_dir)) {
  article_dir <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."), mustWork = FALSE)
}

output_dir <- file.path(article_dir, "outputs")

if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

n <- 4500

source <- sample(
  c("standard_queue", "new_source", "high_variance_source", "manual_upload"),
  size = n,
  replace = TRUE,
  prob = c(0.55, 0.18, 0.17, 0.10)
)

feature_a <- rnorm(n, mean = 0, sd = 1)
feature_b <- rnorm(n, mean = 0, sd = 1)

source_shift <- ifelse(
  source == "standard_queue",
  0.0,
  ifelse(
    source == "new_source",
    0.35,
    ifelse(source == "high_variance_source", -0.20, 0.15)
  )
)

sigmoid <- function(x) {
  1 / (1 + exp(-x))
}

true_logit <- 0.9 * feature_a - 0.6 * feature_b + source_shift
true_probability <- sigmoid(true_logit)

label <- rbinom(n, size = 1, prob = true_probability)

raw_model_logit <- 1.55 * true_logit + rnorm(n, mean = 0, sd = 0.55)
predicted_probability <- sigmoid(raw_model_logit)

entropy <- -(
  predicted_probability * log(pmax(predicted_probability, 1e-9)) +
    (1 - predicted_probability) * log(pmax(1 - predicted_probability, 1e-9))
)

records <- data.frame(
  case_id = paste0("CASE-", sprintf("%05d", 1:n)),
  source = source,
  predicted_probability = predicted_probability,
  true_probability = true_probability,
  label = label,
  entropy = entropy
)

records$uncertainty_zone <- ifelse(
  records$predicted_probability < 0.30,
  "standard_processing",
  ifelse(records$predicted_probability <= 0.75, "human_review", "urgent_review")
)

records$probability_bin <- cut(
  records$predicted_probability,
  breaks = seq(0, 1, by = 0.1),
  include.lowest = TRUE
)

calibration_bins <- aggregate(
  cbind(predicted_probability, label, entropy) ~ probability_bin,
  data = records,
  FUN = mean
)

bin_counts <- aggregate(
  case_id ~ probability_bin,
  data = records,
  FUN = length
)

names(bin_counts)[2] <- "cases"
calibration_bins <- merge(calibration_bins, bin_counts, by = "probability_bin")
names(calibration_bins)[2:4] <- c("mean_confidence", "observed_rate", "mean_entropy")

calibration_bins$absolute_calibration_gap <- abs(
  calibration_bins$observed_rate - calibration_bins$mean_confidence
)

calibration_bins$weighted_calibration_gap <- (
  calibration_bins$cases / sum(calibration_bins$cases)
) * calibration_bins$absolute_calibration_gap

brier_score <- mean((records$predicted_probability - records$label)^2)

p <- pmin(pmax(records$predicted_probability, 1e-9), 1 - 1e-9)

negative_log_likelihood <- -mean(
  records$label * log(p) + (1 - records$label) * log(1 - p)
)

expected_calibration_error <- sum(calibration_bins$weighted_calibration_gap)
accuracy <- mean((records$predicted_probability >= 0.5) == records$label)

slice_summary <- aggregate(
  cbind(predicted_probability, label, entropy) ~ source,
  data = records,
  FUN = mean
)

source_cases <- aggregate(case_id ~ source, data = records, FUN = length)
names(source_cases)[2] <- "cases"
slice_summary <- merge(slice_summary, source_cases, by = "source")
names(slice_summary)[2:4] <- c("mean_confidence", "observed_rate", "mean_entropy")

slice_summary$absolute_calibration_gap <- abs(
  slice_summary$observed_rate - slice_summary$mean_confidence
)

slice_summary$calibration_review_required <- slice_summary$absolute_calibration_gap > 0.08

governance_summary <- data.frame(
  cases_reviewed = nrow(records),
  accuracy = accuracy,
  brier_score = brier_score,
  negative_log_likelihood = negative_log_likelihood,
  expected_calibration_error = expected_calibration_error,
  mean_entropy = mean(records$entropy),
  human_review_rate = mean(records$uncertainty_zone == "human_review"),
  urgent_review_rate = mean(records$uncertainty_zone == "urgent_review"),
  slice_review_count = sum(slice_summary$calibration_review_required)
)

write.csv(records, file.path(output_dir, "r_prediction_logs.csv"), row.names = FALSE)
write.csv(calibration_bins, file.path(output_dir, "r_calibration_bins.csv"), row.names = FALSE)
write.csv(slice_summary, file.path(output_dir, "r_slice_calibration_summary.csv"), row.names = FALSE)
write.csv(governance_summary, file.path(output_dir, "r_calibration_governance_summary.csv"), row.names = FALSE)

print("Calibration bins")
print(calibration_bins)

print("Slice summary")
print(slice_summary)

print("Governance summary")
print(governance_summary)
