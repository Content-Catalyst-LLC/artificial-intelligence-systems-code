# Expert disagreement and review-quality monitoring workflow.
# This script creates synthetic expert judgments and AI recommendations.

set.seed(42)

args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
script_path <- if (length(file_arg) > 0) sub("^--file=", "", file_arg[1]) else getwd()
article_dir <- normalizePath(file.path(dirname(script_path), ".."), mustWork = FALSE)
output_dir <- file.path(article_dir, "outputs")
dir.create(output_dir, showWarnings = FALSE, recursive = TRUE)

n <- 800

review_data <- data.frame(
  case_id = 1:n,
  domain_complexity = runif(n, 0, 1),
  ai_recommendation = runif(n, 0, 1),
  expert_1 = runif(n, 0, 1),
  expert_2 = runif(n, 0, 1),
  expert_3 = runif(n, 0, 1)
)

review_data$expert_mean <- rowMeans(
  review_data[, c("expert_1", "expert_2", "expert_3")]
)

review_data$expert_disagreement <- apply(
  review_data[, c("expert_1", "expert_2", "expert_3")],
  1,
  sd
)

review_data$ai_expert_gap <- abs(
  review_data$ai_recommendation - review_data$expert_mean
)

review_data$review_required <- ifelse(
  review_data$domain_complexity > 0.65 |
    review_data$expert_disagreement > 0.25 |
    review_data$ai_expert_gap > 0.30,
  1,
  0
)

review_data$complexity_band <- cut(
  review_data$domain_complexity,
  breaks = c(0, 0.33, 0.66, 1),
  labels = c("low", "medium", "high"),
  include.lowest = TRUE
)

summary_table <- data.frame(
  mean_expert_disagreement = mean(review_data$expert_disagreement),
  mean_ai_expert_gap = mean(review_data$ai_expert_gap),
  review_required_rate = mean(review_data$review_required)
)

band_summary <- aggregate(
  cbind(expert_disagreement, ai_expert_gap, review_required) ~ complexity_band,
  data = review_data,
  FUN = mean
)

write.csv(review_data, file.path(output_dir, "expert_review_synthetic.csv"), row.names = FALSE)
write.csv(summary_table, file.path(output_dir, "expert_review_summary.csv"), row.names = FALSE)
write.csv(band_summary, file.path(output_dir, "expert_review_band_summary.csv"), row.names = FALSE)

print(summary_table)
print(band_summary)
