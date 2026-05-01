# Data Quality, Bias, and Measurement in Machine Learning Diagnostics
#
# This educational workflow simulates:
# - subgroup representation imbalance
# - group-dependent missingness
# - measurement error
# - noisy labels
# - subgroup error diagnostics

set.seed(42)

n <- 5000

group <- sample(
  c("A", "B"),
  n,
  replace = TRUE,
  prob = c(0.82, 0.18)
)

feature_signal <- rnorm(n, mean = 0, sd = 1)

measurement_quality <- sample(
  c("high", "medium", "low"),
  n,
  replace = TRUE,
  prob = c(0.55, 0.30, 0.15)
)

measurement_error_sd <- ifelse(group == "B", 0.45, 0.20)

measured_feature <- feature_signal + rnorm(n, mean = 0, sd = measurement_error_sd)

logit <- -0.10 + 1.20 * feature_signal + ifelse(group == "B", -0.15, 0)
probability <- 1 / (1 + exp(-logit))

true_label <- rbinom(n, size = 1, prob = probability)

label_flip_probability <- ifelse(
  measurement_quality == "low",
  0.18,
  ifelse(measurement_quality == "medium", 0.08, 0.03)
)

label_flip <- rbinom(n, size = 1, prob = label_flip_probability)

observed_label <- ifelse(
  label_flip == 1,
  1 - true_label,
  true_label
)

missing_probability <- ifelse(group == "B", 0.20, 0.06)
measured_feature_missing <- rbinom(n, size = 1, prob = missing_probability)

measured_feature_observed <- measured_feature
measured_feature_observed[measured_feature_missing == 1] <- NA

imputed_feature <- measured_feature_observed
imputed_feature[is.na(imputed_feature)] <- mean(imputed_feature, na.rm = TRUE)

score <- 1 / (1 + exp(-(-0.05 + 1.05 * imputed_feature)))
predicted_label <- ifelse(score >= 0.50, 1, 0)

prediction_error <- ifelse(predicted_label != true_label, 1, 0)

quality_data <- data.frame(
  group = group,
  feature_signal = feature_signal,
  measured_feature = measured_feature_observed,
  measurement_quality = measurement_quality,
  true_label = true_label,
  observed_label = observed_label,
  measured_feature_missing = measured_feature_missing,
  predicted_label = predicted_label,
  prediction_error = prediction_error
)

representation_table <- aggregate(
  cbind(
    measured_feature_missing,
    observed_label,
    true_label,
    predicted_label,
    prediction_error
  ) ~ group,
  data = quality_data,
  FUN = mean
)

group_counts <- as.data.frame(table(quality_data$group))
names(group_counts) <- c("group", "units")
group_counts$share <- group_counts$units / sum(group_counts$units)

summary_table <- merge(group_counts, representation_table, by = "group")

statistical_parity_difference <-
  summary_table$predicted_label[summary_table$group == "A"] -
  summary_table$predicted_label[summary_table$group == "B"]

diagnostics <- data.frame(
  metric = c(
    "overall_missing_rate",
    "label_noise_rate",
    "statistical_parity_difference_A_minus_B",
    "overall_prediction_error"
  ),
  value = c(
    mean(quality_data$measured_feature_missing),
    mean(label_flip),
    statistical_parity_difference,
    mean(quality_data$prediction_error)
  )
)

dir.create("../outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(quality_data, "../outputs/r_data_quality_bias_synthetic_data.csv", row.names = FALSE)
write.csv(summary_table, "../outputs/r_data_quality_bias_group_summary.csv", row.names = FALSE)
write.csv(diagnostics, "../outputs/r_data_quality_bias_diagnostics.csv", row.names = FALSE)

print(summary_table)
print(diagnostics)
