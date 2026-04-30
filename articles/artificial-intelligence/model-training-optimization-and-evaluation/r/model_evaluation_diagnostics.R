# Model Evaluation Diagnostics in R
#
# This educational workflow simulates classification errors across
# synthetic groups and deployment conditions.

set.seed(42)

n <- 2000

eval_data <- data.frame(
  group = sample(c("A", "B", "C"), n, replace = TRUE, prob = c(0.5, 0.3, 0.2)),
  condition = sample(c("development_like", "moderate_shift", "high_shift"), n, replace = TRUE),
  target = rbinom(n, size = 1, prob = 0.4)
)

condition_error <- ifelse(
  eval_data$condition == "development_like", 0.08,
  ifelse(eval_data$condition == "moderate_shift", 0.14, 0.24)
)

group_error <- ifelse(
  eval_data$group == "A", 1.00,
  ifelse(eval_data$group == "B", 1.15, 1.35)
)

error_probability <- pmin(condition_error * group_error, 0.90)
is_error <- rbinom(n, size = 1, prob = error_probability)

eval_data$prediction <- ifelse(
  is_error == 1,
  1 - eval_data$target,
  eval_data$target
)

eval_data$error <- eval_data$prediction != eval_data$target

summary_table <- aggregate(
  error ~ group + condition,
  data = eval_data,
  FUN = mean
)

names(summary_table)[3] <- "classification_error_rate"

dir.create("../outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(summary_table, "../outputs/r_model_evaluation_diagnostics.csv", row.names = FALSE)

print(summary_table)
