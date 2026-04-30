# Fairness Diagnostics by Group and Condition
#
# This educational workflow simulates decision outcomes across groups
# and deployment conditions, then summarizes disparities.

set.seed(42)

n <- 2500

fairness_data <- data.frame(
  group = sample(c("A", "B", "C"), n, replace = TRUE, prob = c(0.45, 0.35, 0.20)),
  condition = sample(c("development_like", "moderate_shift", "high_shift"), n, replace = TRUE),
  target = rbinom(n, size = 1, prob = 0.40)
)

base_score <- ifelse(
  fairness_data$target == 1,
  rbeta(n, 5, 3),
  rbeta(n, 3, 5)
)

group_shift <- ifelse(
  fairness_data$group == "A", 0.03,
  ifelse(fairness_data$group == "B", -0.02, -0.06)
)

condition_shift <- ifelse(
  fairness_data$condition == "development_like", 0.00,
  ifelse(fairness_data$condition == "moderate_shift", -0.03, -0.08)
)

fairness_data$score <- pmin(pmax(base_score + group_shift + condition_shift, 0), 1)
fairness_data$prediction <- ifelse(fairness_data$score >= 0.50, 1, 0)

fairness_data$true_positive <- fairness_data$prediction == 1 & fairness_data$target == 1
fairness_data$false_positive <- fairness_data$prediction == 1 & fairness_data$target == 0
fairness_data$actual_positive <- fairness_data$target == 1
fairness_data$actual_negative <- fairness_data$target == 0

summary_table <- aggregate(
  cbind(prediction, target, true_positive, false_positive, actual_positive, actual_negative) ~ group + condition,
  data = fairness_data,
  FUN = sum
)

summary_table$sample_size <- aggregate(
  prediction ~ group + condition,
  data = fairness_data,
  FUN = length
)$prediction

summary_table$selection_rate <- summary_table$prediction / summary_table$sample_size
summary_table$base_rate <- summary_table$target / summary_table$sample_size
summary_table$true_positive_rate <- summary_table$true_positive / pmax(summary_table$actual_positive, 1)
summary_table$false_positive_rate <- summary_table$false_positive / pmax(summary_table$actual_negative, 1)

dir.create("../outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(summary_table, "../outputs/r_fairness_group_condition_diagnostics.csv", row.names = FALSE)

print(summary_table)
