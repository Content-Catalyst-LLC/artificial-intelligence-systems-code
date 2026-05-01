# Model Validation, Benchmarking, and Generalization Diagnostics
#
# This educational workflow simulates:
# - k-fold validation performance
# - benchmark score comparisons
# - benchmark saturation scoring
# - distribution-shift degradation

set.seed(42)

models <- c("baseline_linear", "random_forest", "gradient_boosted", "neural_network")
folds <- paste0("fold_", 1:10)

cv_results <- expand.grid(
  model = models,
  fold = folds
)

model_effect <- ifelse(
  cv_results$model == "baseline_linear", 0.74,
  ifelse(
    cv_results$model == "random_forest", 0.81,
    ifelse(cv_results$model == "gradient_boosted", 0.84, 0.85)
  )
)

cv_results$validation_accuracy <- pmin(
  0.99,
  pmax(
    0.50,
    rnorm(nrow(cv_results), mean = model_effect, sd = 0.025)
  )
)

cv_summary <- aggregate(
  validation_accuracy ~ model,
  data = cv_results,
  FUN = function(x) c(mean = mean(x), sd = sd(x))
)

cv_summary <- do.call(data.frame, cv_summary)
names(cv_summary) <- c("model", "mean_accuracy", "sd_accuracy")

benchmark_results <- data.frame(
  model = models,
  public_benchmark_score = c(0.78, 0.86, 0.89, 0.90),
  external_validation_score = c(0.74, 0.80, 0.82, 0.79),
  shifted_deployment_score = c(0.70, 0.76, 0.77, 0.72)
)

benchmark_results$external_gap <-
  benchmark_results$public_benchmark_score -
  benchmark_results$external_validation_score

benchmark_results$shift_gap <-
  benchmark_results$external_validation_score -
  benchmark_results$shifted_deployment_score

top_scores <- sort(benchmark_results$public_benchmark_score, decreasing = TRUE)[1:3]

benchmark_saturation_indicator <-
  1 - (sd(top_scores) / sd(benchmark_results$public_benchmark_score))

saturation_table <- data.frame(
  metric = "benchmark_saturation_indicator",
  value = benchmark_saturation_indicator
)

dir.create("../outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(cv_results, "../outputs/r_cross_validation_results.csv", row.names = FALSE)
write.csv(cv_summary, "../outputs/r_cross_validation_summary.csv", row.names = FALSE)
write.csv(benchmark_results, "../outputs/r_benchmark_shift_results.csv", row.names = FALSE)
write.csv(saturation_table, "../outputs/r_benchmark_saturation_indicator.csv", row.names = FALSE)

print(cv_summary)
print(benchmark_results)
print(saturation_table)
