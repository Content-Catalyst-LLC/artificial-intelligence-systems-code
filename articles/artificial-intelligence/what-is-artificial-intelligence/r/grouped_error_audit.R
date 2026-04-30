# Grouped Error Audit in R
#
# Synthetic educational workflow for:
# "What Is Artificial Intelligence?"

set.seed(42)

n <- 3000

audit_data <- data.frame(
  group = sample(c("A", "B", "C"), size = n, replace = TRUE, prob = c(0.5, 0.3, 0.2)),
  target = rbinom(n, size = 1, prob = 0.35),
  score = pmin(pmax(rbeta(n, shape1 = 2.3, shape2 = 3.1), 0), 1)
)

audit_data$prediction <- ifelse(audit_data$score >= 0.5, 1, 0)

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
  sample_size = sapply(groups, nrow),
  selection_rate = sapply(groups, function(df) mean(df$prediction == 1)),
  false_positive_rate = sapply(groups, false_positive_rate),
  false_negative_rate = sapply(groups, false_negative_rate),
  row.names = NULL
)

dir.create("../outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(error_rates, "../outputs/r_grouped_error_audit.csv", row.names = FALSE)

print(error_rates)
