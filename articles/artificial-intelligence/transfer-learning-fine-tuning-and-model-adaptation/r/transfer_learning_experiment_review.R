# Transfer Learning, Fine-Tuning, and Model Adaptation
# R workflow: transfer learning experiment review.

set.seed(42)

article_dir <- normalizePath(file.path(getwd(), "articles/artificial-intelligence/transfer-learning-fine-tuning-and-model-adaptation"), mustWork = FALSE)

if (!dir.exists(article_dir)) {
  article_dir <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."), mustWork = FALSE)
}

output_dir <- file.path(article_dir, "outputs")

if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

n <- 120

methods <- c(
  "base_model_zero_shot",
  "linear_head_only",
  "full_fine_tuning",
  "regularized_fine_tuning",
  "adapter_tuning",
  "lora",
  "qlora"
)

records <- data.frame(
  experiment_id = paste0("ADAPT-", sprintf("%03d", 1:n)),
  method = sample(methods, size = n, replace = TRUE),
  target_dataset_size = sample(100:5000, size = n, replace = TRUE),
  target_data_quality = runif(n, min = 0.45, max = 0.98),
  domain_shift_score = runif(n, min = 0.05, max = 0.70),
  sensitive_domain = sample(c(0, 1), size = n, replace = TRUE, prob = c(0.75, 0.25))
)

records$target_performance <- 0.62 + rnorm(n, mean = 0, sd = 0.04)
records$source_retention <- 0.91 + rnorm(n, mean = 0, sd = 0.03)
records$trainable_parameter_share <- 0.00
records$compute_cost_index <- 0.05

for (i in 1:nrow(records)) {
  method <- records$method[i]

  if (method == "linear_head_only") {
    records$target_performance[i] <- records$target_performance[i] + rnorm(1, 0.05, 0.03)
    records$source_retention[i] <- records$source_retention[i] - rnorm(1, 0.01, 0.01)
    records$trainable_parameter_share[i] <- 0.01
    records$compute_cost_index[i] <- 0.12
  } else if (method == "full_fine_tuning") {
    records$target_performance[i] <- records$target_performance[i] + rnorm(1, 0.12, 0.04)
    records$source_retention[i] <- records$source_retention[i] - rnorm(1, 0.10, 0.04)
    records$trainable_parameter_share[i] <- 1.00
    records$compute_cost_index[i] <- 0.90
  } else if (method == "regularized_fine_tuning") {
    records$target_performance[i] <- records$target_performance[i] + rnorm(1, 0.10, 0.035)
    records$source_retention[i] <- records$source_retention[i] - rnorm(1, 0.05, 0.02)
    records$trainable_parameter_share[i] <- 1.00
    records$compute_cost_index[i] <- 0.88
  } else if (method == "adapter_tuning") {
    records$target_performance[i] <- records$target_performance[i] + rnorm(1, 0.09, 0.03)
    records$source_retention[i] <- records$source_retention[i] - rnorm(1, 0.02, 0.015)
    records$trainable_parameter_share[i] <- 0.04
    records$compute_cost_index[i] <- 0.28
  } else if (method == "lora") {
    records$target_performance[i] <- records$target_performance[i] + rnorm(1, 0.10, 0.03)
    records$source_retention[i] <- records$source_retention[i] - rnorm(1, 0.02, 0.015)
    records$trainable_parameter_share[i] <- 0.02
    records$compute_cost_index[i] <- 0.24
  } else if (method == "qlora") {
    records$target_performance[i] <- records$target_performance[i] + rnorm(1, 0.09, 0.035)
    records$source_retention[i] <- records$source_retention[i] - rnorm(1, 0.025, 0.015)
    records$trainable_parameter_share[i] <- 0.02
    records$compute_cost_index[i] <- 0.16
  }
}

records$target_performance <- pmin(pmax(records$target_performance, 0), 1)
records$source_retention <- pmin(pmax(records$source_retention, 0), 1)

baseline <- mean(records$target_performance[records$method == "base_model_zero_shot"])

if (is.nan(baseline)) {
  baseline <- 0.62
}

records$transfer_gain <- records$target_performance - baseline
records$forgetting_risk <- 1 - records$source_retention

records$overfit_risk <- 0.35 * (1 - records$target_data_quality) +
  0.35 * (1 / sqrt(records$target_dataset_size / 100)) +
  0.30 * records$domain_shift_score

records$adaptation_risk <- 0.30 * records$forgetting_risk +
  0.25 * records$overfit_risk +
  0.20 * records$domain_shift_score +
  0.15 * records$sensitive_domain +
  0.10 * records$compute_cost_index

records$review_required <- records$adaptation_risk > 0.45 |
  records$transfer_gain < 0 |
  records$source_retention < 0.80 |
  records$sensitive_domain == 1

method_summary <- aggregate(
  cbind(
    target_performance,
    transfer_gain,
    source_retention,
    adaptation_risk,
    review_required,
    trainable_parameter_share,
    compute_cost_index
  ) ~ method,
  data = records,
  FUN = mean
)

governance_summary <- data.frame(
  experiments_reviewed = nrow(records),
  methods_compared = length(unique(records$method)),
  review_required = sum(records$review_required),
  negative_transfer_cases = sum(records$transfer_gain < 0),
  high_forgetting_risk_cases = sum(records$source_retention < 0.80),
  mean_transfer_gain = mean(records$transfer_gain),
  mean_adaptation_risk = mean(records$adaptation_risk)
)

write.csv(records, file.path(output_dir, "r_adaptation_experiment_records.csv"), row.names = FALSE)
write.csv(method_summary, file.path(output_dir, "r_adaptation_method_summary.csv"), row.names = FALSE)
write.csv(governance_summary, file.path(output_dir, "r_adaptation_governance_summary.csv"), row.names = FALSE)

print("Method summary")
print(method_summary)

print("Governance summary")
print(governance_summary)
