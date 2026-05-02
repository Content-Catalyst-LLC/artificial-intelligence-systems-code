# Disparity and remedy monitoring workflow.
# This script creates synthetic AI-assisted decision records and summarizes
# adverse outcomes, appeals, remedies, time to remedy, and burden by group.

set.seed(42)

args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
script_path <- if (length(file_arg) > 0) sub("^--file=", "", file_arg[1]) else getwd()
article_dir <- normalizePath(file.path(dirname(script_path), ".."), mustWork = FALSE)
output_dir <- file.path(article_dir, "outputs")
dir.create(output_dir, showWarnings = FALSE, recursive = TRUE)

n <- 1200

records <- data.frame(
  case_id = 1:n,
  group = sample(
    c("Group A", "Group B", "Group C"),
    n,
    replace = TRUE,
    prob = c(0.50, 0.30, 0.20)
  ),
  ai_assisted_decision = sample(
    c(0, 1),
    n,
    replace = TRUE,
    prob = c(0.25, 0.75)
  ),
  adverse_outcome = sample(
    c(0, 1),
    n,
    replace = TRUE,
    prob = c(0.78, 0.22)
  ),
  appealed = sample(
    c(0, 1),
    n,
    replace = TRUE,
    prob = c(0.88, 0.12)
  ),
  remedy_provided = 0,
  remedy_days = round(rgamma(n, shape = 3, scale = 6)),
  delay_days = round(rgamma(n, shape = 2, scale = 4)),
  paperwork_burden_score = runif(n, 0, 1),
  explanation_quality_score = runif(n, 0, 1)
)

records$remedy_provided[records$appealed == 1] <- sample(
  c(0, 1),
  sum(records$appealed == 1),
  replace = TRUE,
  prob = c(0.65, 0.35)
)

records$burden_score <-
  0.35 * scale(records$delay_days)[, 1] +
  0.35 * records$paperwork_burden_score +
  0.30 * (1 - records$explanation_quality_score)

# Rescale burden score to 0-1 for easier reporting.
records$burden_score <- (records$burden_score - min(records$burden_score)) /
  (max(records$burden_score) - min(records$burden_score))

outcome_rate <- aggregate(adverse_outcome ~ group, data = records, FUN = mean)
appeal_rate <- aggregate(appealed ~ group, data = records, FUN = mean)

remedy_rate <- aggregate(
  remedy_provided ~ group,
  data = subset(records, appealed == 1),
  FUN = mean
)

time_to_remedy <- aggregate(
  remedy_days ~ group,
  data = subset(records, remedy_provided == 1),
  FUN = mean
)

burden_summary <- aggregate(
  burden_score ~ group,
  data = records,
  FUN = mean
)

monitoring <- merge(outcome_rate, appeal_rate, by = "group")
monitoring <- merge(monitoring, remedy_rate, by = "group")
monitoring <- merge(monitoring, time_to_remedy, by = "group")
monitoring <- merge(monitoring, burden_summary, by = "group")

names(monitoring) <- c(
  "group",
  "adverse_outcome_rate",
  "appeal_rate",
  "remedy_rate",
  "mean_remedy_days",
  "mean_burden_score"
)

reference_outcome_rate <- min(monitoring$adverse_outcome_rate)
monitoring$outcome_disparity_gap <- abs(
  monitoring$adverse_outcome_rate - reference_outcome_rate
)

reference_burden <- min(monitoring$mean_burden_score)
monitoring$burden_gap <- abs(monitoring$mean_burden_score - reference_burden)

write.csv(records, file.path(output_dir, "synthetic_rights_monitoring_records.csv"), row.names = FALSE)
write.csv(monitoring, file.path(output_dir, "disparity_remedy_monitoring_summary.csv"), row.names = FALSE)

print(monitoring)
