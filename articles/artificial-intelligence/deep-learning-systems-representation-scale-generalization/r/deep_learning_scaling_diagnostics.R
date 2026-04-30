# Deep Learning Scaling and Generalization Diagnostics
#
# This educational workflow simulates:
# - a power-law scaling curve
# - training and test error across capacity levels
# - generalization gap diagnostics

set.seed(42)

capacity <- seq(50, 5000, length.out = 80)

scaling_loss <- 2.0 * capacity^(-0.18) + 0.25 + rnorm(length(capacity), 0, 0.01)

train_error <- 0.45 * exp(-capacity / 900) + 0.02
test_error <- 0.30 * exp(-capacity / 1400) + 0.08 +
  0.05 * exp(-((capacity - 900)^2) / (2 * 280^2))

diagnostics <- data.frame(
  capacity = capacity,
  simulated_scaling_loss = scaling_loss,
  train_error = train_error,
  test_error = test_error,
  generalization_gap = test_error - train_error
)

summary_table <- data.frame(
  min_scaling_loss = min(diagnostics$simulated_scaling_loss),
  max_generalization_gap = max(diagnostics$generalization_gap),
  capacity_at_min_test_error = diagnostics$capacity[which.min(diagnostics$test_error)]
)

dir.create("../outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(diagnostics, "../outputs/r_deep_learning_scaling_diagnostics.csv", row.names = FALSE)
write.csv(summary_table, "../outputs/r_deep_learning_summary.csv", row.names = FALSE)

print(summary_table)
