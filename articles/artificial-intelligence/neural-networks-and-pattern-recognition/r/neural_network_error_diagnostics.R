# Neural Network Error Diagnostics
#
# This educational workflow simulates classification error rates across
# synthetic groups and deployment conditions.

set.seed(42)

n <- 1800

nn_eval <- data.frame(
  group = sample(c("A", "B", "C"), n, replace = TRUE, prob = c(0.50, 0.30, 0.20)),
  condition = sample(c("training_like", "moderate_shift", "high_shift"), n, replace = TRUE),
  target = rbinom(n, size = 1, prob = 0.45)
)

condition_error <- ifelse(
  nn_eval$condition == "training_like", 0.08,
  ifelse(nn_eval$condition == "moderate_shift", 0.15, 0.26)
)

group_multiplier <- ifelse(
  nn_eval$group == "A", 1.00,
  ifelse(nn_eval$group == "B", 1.15, 1.35)
)

error_probability <- pmin(condition_error * group_multiplier, 0.90)

is_error <- rbinom(n, size = 1, prob = error_probability)

nn_eval$prediction <- ifelse(
  is_error == 1,
  1 - nn_eval$target,
  nn_eval$target
)

nn_eval$error <- nn_eval$prediction != nn_eval$target

summary_table <- aggregate(
  error ~ group + condition,
  data = nn_eval,
  FUN = mean
)

names(summary_table)[3] <- "classification_error_rate"

dir.create("../outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(summary_table, "../outputs/r_neural_network_error_diagnostics.csv", row.names = FALSE)

print(summary_table)
