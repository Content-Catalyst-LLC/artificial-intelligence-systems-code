# Robustness and Adversarial Resilience Diagnostics
#
# This educational workflow simulates:
# - perturbation budgets
# - clean accuracy
# - robust accuracy
# - robustness gaps
# - stress-test reporting

set.seed(42)

epsilons <- seq(0, 0.50, by = 0.05)

clean_accuracy <- rep(0.94, length(epsilons))

robust_accuracy <- pmax(
  0.30,
  clean_accuracy - 0.70 * epsilons + rnorm(length(epsilons), mean = 0, sd = 0.015)
)

robustness_results <- data.frame(
  epsilon = epsilons,
  clean_accuracy = clean_accuracy,
  robust_accuracy = robust_accuracy
)

robustness_results$robustness_gap <-
  robustness_results$clean_accuracy - robustness_results$robust_accuracy

robustness_results$risk_band <- ifelse(
  robustness_results$robustness_gap < 0.10,
  "low_degradation",
  ifelse(
    robustness_results$robustness_gap < 0.25,
    "moderate_degradation",
    "high_degradation"
  )
)

summary_table <- aggregate(
  cbind(clean_accuracy, robust_accuracy, robustness_gap) ~ risk_band,
  data = robustness_results,
  FUN = mean
)

dir.create("../outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(robustness_results, "../outputs/r_robustness_stress_test_results.csv", row.names = FALSE)
write.csv(summary_table, "../outputs/r_robustness_summary_by_risk_band.csv", row.names = FALSE)

print(robustness_results)
print(summary_table)
