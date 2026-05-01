# AI in Health, Medicine, and Clinical Decision Support
# R workflow: clinical decision support evaluation summary.
#
# Educational systems workflow only.
# Not medical advice and not a substitute for local clinical validation.

set.seed(42)

article_dir <- normalizePath(file.path(getwd(), "articles/artificial-intelligence/ai-in-health-medicine-and-clinical-decision-support"), mustWork = FALSE)

if (!dir.exists(article_dir)) {
  article_dir <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."), mustWork = FALSE)
}

output_dir <- file.path(article_dir, "outputs")

if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

n <- 5000
threshold <- 0.25

site <- sample(c("hospital_a", "hospital_b", "hospital_c"), size = n, replace = TRUE, prob = c(0.50, 0.32, 0.18))
unit <- sample(c("ward", "icu", "ed"), size = n, replace = TRUE, prob = c(0.58, 0.22, 0.20))
age_band <- sample(c("18_44", "45_64", "65_84", "85_plus"), size = n, replace = TRUE, prob = c(0.22, 0.34, 0.34, 0.10))
language_group <- sample(c("english", "non_english"), size = n, replace = TRUE, prob = c(0.82, 0.18))

vital_score <- rnorm(n)
lab_score <- rnorm(n)
comorbidity_score <- rgamma(n, shape = 2.0, scale = 0.6)
missingness_score <- rbeta(n, shape1 = 1.2, shape2 = 6.0)

unit_shift <- ifelse(unit == "ward", 0.0, ifelse(unit == "icu", 0.9, 0.35))
age_shift <- ifelse(age_band == "18_44", -0.35, ifelse(age_band == "45_64", 0.0, ifelse(age_band == "65_84", 0.45, 0.75)))
language_shift <- ifelse(language_group == "non_english", 0.18, 0.0)
site_shift <- ifelse(site == "hospital_a", 0.0, ifelse(site == "hospital_b", 0.15, -0.10))

sigmoid <- function(x) {
  1 / (1 + exp(-x))
}

true_logit <- 0.90 * vital_score +
  0.65 * lab_score +
  0.55 * comorbidity_score +
  unit_shift +
  age_shift +
  language_shift +
  site_shift -
  2.45

true_probability <- sigmoid(true_logit)
outcome <- rbinom(n, size = 1, prob = true_probability)

model_logit <- 0.82 * vital_score +
  0.58 * lab_score +
  0.48 * comorbidity_score +
  0.72 * unit_shift +
  0.35 * age_shift +
  0.03 * language_shift +
  0.05 * site_shift -
  2.10 +
  rnorm(n, mean = 0, sd = 0.45)

predicted_probability <- sigmoid(model_logit)

records <- data.frame(
  case_id = paste0("CLIN-", sprintf("%05d", 1:n)),
  site = site,
  unit = unit,
  age_band = age_band,
  language_group = language_group,
  missingness_score = missingness_score,
  true_probability = true_probability,
  predicted_probability = predicted_probability,
  outcome = outcome
)

records$alert <- records$predicted_probability >= threshold
records$uncertainty_zone <- records$predicted_probability >= (threshold - 0.05) &
  records$predicted_probability <= (threshold + 0.05)

tp <- sum(records$alert == TRUE & records$outcome == 1)
fp <- sum(records$alert == TRUE & records$outcome == 0)
tn <- sum(records$alert == FALSE & records$outcome == 0)
fn <- sum(records$alert == FALSE & records$outcome == 1)

overall_metrics <- data.frame(
  cases = nrow(records),
  threshold = threshold,
  true_positives = tp,
  false_positives = fp,
  true_negatives = tn,
  false_negatives = fn,
  sensitivity = tp / max(tp + fn, 1),
  specificity = tn / max(tn + fp, 1),
  positive_predictive_value = tp / max(tp + fp, 1),
  negative_predictive_value = tn / max(tn + fn, 1),
  alert_rate = mean(records$alert),
  brier_score = mean((records$predicted_probability - records$outcome)^2)
)

records$risk_bin <- cut(
  records$predicted_probability,
  breaks = seq(0, 1, by = 0.1),
  include.lowest = TRUE
)

calibration_bins <- aggregate(
  cbind(predicted_probability, outcome, missingness_score) ~ risk_bin,
  data = records,
  FUN = mean
)

bin_counts <- aggregate(case_id ~ risk_bin, data = records, FUN = length)
names(bin_counts)[2] <- "cases"

calibration_bins <- merge(calibration_bins, bin_counts, by = "risk_bin")
names(calibration_bins)[2:4] <- c("mean_predicted_risk", "observed_event_rate", "mean_missingness")

calibration_bins$absolute_calibration_gap <- abs(
  calibration_bins$observed_event_rate - calibration_bins$mean_predicted_risk
)

calibration_bins$weighted_calibration_gap <- (
  calibration_bins$cases / sum(calibration_bins$cases)
) * calibration_bins$absolute_calibration_gap

expected_calibration_error <- sum(calibration_bins$weighted_calibration_gap)

summarize_group <- function(data, group_name) {
  split_data <- split(data, data[[group_name]])

  rows <- lapply(names(split_data), function(value) {
    subset <- split_data[[value]]

    tp_g <- sum(subset$alert == TRUE & subset$outcome == 1)
    fp_g <- sum(subset$alert == TRUE & subset$outcome == 0)
    tn_g <- sum(subset$alert == FALSE & subset$outcome == 0)
    fn_g <- sum(subset$alert == FALSE & subset$outcome == 1)

    data.frame(
      subgroup_type = group_name,
      subgroup_value = value,
      cases = nrow(subset),
      sensitivity = tp_g / max(tp_g + fn_g, 1),
      specificity = tn_g / max(tn_g + fp_g, 1),
      alert_rate = mean(subset$alert),
      false_negatives = fn_g,
      brier_score = mean((subset$predicted_probability - subset$outcome)^2)
    )
  })

  do.call(rbind, rows)
}

subgroup_summary <- rbind(
  summarize_group(records, "site"),
  summarize_group(records, "unit"),
  summarize_group(records, "age_band"),
  summarize_group(records, "language_group")
)

subgroup_summary$sensitivity_gap_from_overall <- subgroup_summary$sensitivity - overall_metrics$sensitivity
subgroup_summary$alert_rate_gap_from_overall <- subgroup_summary$alert_rate - overall_metrics$alert_rate

subgroup_summary$review_required <- abs(subgroup_summary$sensitivity_gap_from_overall) > 0.12 |
  abs(subgroup_summary$alert_rate_gap_from_overall) > 0.12 |
  subgroup_summary$false_negatives > 20 |
  subgroup_summary$brier_score > 0.22

records$clinical_ai_governance_risk <- pmin(
  1,
  0.25 * records$missingness_score +
    0.25 * as.numeric(records$uncertainty_zone) +
    0.20 * as.numeric(records$unit == "icu") +
    0.15 * as.numeric(records$age_band == "85_plus") +
    0.15 * as.numeric(records$language_group == "non_english")
)

records$human_review_recommended <- records$clinical_ai_governance_risk > 0.40 |
  records$missingness_score > 0.35 |
  (records$uncertainty_zone & records$unit %in% c("icu", "ed"))

governance_summary <- data.frame(
  cases_reviewed = nrow(records),
  threshold = threshold,
  expected_calibration_error = expected_calibration_error,
  subgroups_requiring_review = sum(subgroup_summary$review_required),
  human_review_recommended_cases = sum(records$human_review_recommended),
  mean_governance_risk = mean(records$clinical_ai_governance_risk),
  max_governance_risk = max(records$clinical_ai_governance_risk)
)

write.csv(records, file.path(output_dir, "r_clinical_ai_prediction_logs.csv"), row.names = FALSE)
write.csv(overall_metrics, file.path(output_dir, "r_clinical_ai_overall_metrics.csv"), row.names = FALSE)
write.csv(calibration_bins, file.path(output_dir, "r_clinical_ai_calibration_bins.csv"), row.names = FALSE)
write.csv(subgroup_summary, file.path(output_dir, "r_clinical_ai_subgroup_review.csv"), row.names = FALSE)
write.csv(governance_summary, file.path(output_dir, "r_clinical_ai_governance_summary.csv"), row.names = FALSE)

print("Overall metrics")
print(overall_metrics)

print("Calibration bins")
print(calibration_bins)

print("Subgroup summary")
print(subgroup_summary)

print("Governance summary")
print(governance_summary)
