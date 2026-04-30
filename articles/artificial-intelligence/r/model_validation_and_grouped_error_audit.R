# Model Validation and Grouped Error Audit in R

set.seed(42)

n <- 3000

audit_data <- data.frame(
  group = sample(c("A", "B", "C"), size = n, replace = TRUE, prob = c(0.5, 0.3, 0.2)),
  target = rbinom(n, size = 1, prob = 0.35),
  score = pmin(pmax(rbeta(n, shape1 = 2.3, shape2 = 3.1), 0), 1)
)

audit_data$prediction <- ifelse(audit_data$score >= 0.5, 1, 0)

accuracy <- mean(audit_data$prediction == audit_data$target)
precision <- with(audit_data, sum(prediction == 1 & target == 1) / max(sum(prediction == 1), 1))
recall <- with(audit_data, sum(prediction == 1 & target == 1) / max(sum(target == 1), 1))

grouped_audit <- aggregate(
  cbind(prediction, target) ~ group,
  data = audit_data,
  FUN = mean
)

names(grouped_audit) <- c("group", "selection_rate", "base_rate")

false_positive_rate <- function(df) {
  negatives <- df[df$target == 0, ]
  mean(negatives$prediction == 1)
}

false_negative_rate <- function(df) {
  positives <- df[df$target == 1, ]
  mean(positives$prediction == 0)
}

groups <- split(audit_data, audit_data$group)

error_rates <- data.frame(
  group = names(groups),
  false_positive_rate = sapply(groups, false_positive_rate),
  false_negative_rate = sapply(groups, false_negative_rate),
  row.names = NULL
)

summary_report <- merge(grouped_audit, error_rates, by = "group")

dir.create("../outputs", showWarnings = FALSE, recursive = TRUE)
write.csv(summary_report, "../outputs/r_grouped_error_audit.csv", row.names = FALSE)

print(list(
  accuracy = accuracy,
  precision = precision,
  recall = recall,
  grouped_audit = summary_report
))
