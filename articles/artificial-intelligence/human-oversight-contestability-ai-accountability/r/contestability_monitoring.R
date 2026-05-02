# Contestability monitoring workflow.
# This script creates synthetic appeal data and summarizes contestability indicators.

set.seed(42)

args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
script_path <- if (length(file_arg) > 0) sub("^--file=", "", file_arg[1]) else getwd()
article_dir <- normalizePath(file.path(dirname(script_path), ".."), mustWork = FALSE)
output_dir <- file.path(article_dir, "outputs")
dir.create(output_dir, showWarnings = FALSE, recursive = TRUE)

n <- 1200

appeals <- data.frame(
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
  appealed = sample(
    c(0, 1),
    n,
    replace = TRUE,
    prob = c(0.88, 0.12)
  ),
  corrected = 0,
  resolution_days = round(rgamma(n, shape = 3, scale = 5))
)

appeals$corrected[appeals$appealed == 1] <- sample(
  c(0, 1),
  sum(appeals$appealed == 1),
  replace = TRUE,
  prob = c(0.65, 0.35)
)

appeal_rate <- aggregate(appealed ~ group, data = appeals, FUN = mean)

success_rate <- aggregate(
  corrected ~ group,
  data = subset(appeals, appealed == 1),
  FUN = mean
)

resolution_time <- aggregate(
  resolution_days ~ group,
  data = subset(appeals, appealed == 1),
  FUN = mean
)

monitoring <- merge(appeal_rate, success_rate, by = "group")
monitoring <- merge(monitoring, resolution_time, by = "group")

names(monitoring) <- c(
  "group",
  "appeal_rate",
  "successful_appeal_rate",
  "mean_resolution_days"
)

reference_success_rate <- max(monitoring$successful_appeal_rate)
monitoring$contestability_gap <- abs(
  monitoring$successful_appeal_rate - reference_success_rate
)

monitoring$timeliness_flag <- ifelse(
  monitoring$mean_resolution_days > 21,
  "slow_resolution",
  "within_monitoring_range"
)

write.csv(appeals, file.path(output_dir, "appeals_synthetic.csv"), row.names = FALSE)
write.csv(monitoring, file.path(output_dir, "contestability_monitoring_summary.csv"), row.names = FALSE)

print(monitoring)
