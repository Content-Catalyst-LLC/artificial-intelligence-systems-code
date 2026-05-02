# Job-quality and automation-risk monitoring workflow.
# This script creates synthetic worker records and summarizes AI exposure,
# job quality, monitoring burden, training access, worker voice,
# work intensification, and transition priority.

set.seed(42)

args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
script_path <- if (length(file_arg) > 0) sub("^--file=", "", file_arg[1]) else getwd()
article_dir <- normalizePath(file.path(dirname(script_path), ".."), mustWork = FALSE)
output_dir <- file.path(article_dir, "outputs")
dir.create(output_dir, showWarnings = FALSE, recursive = TRUE)

n <- 800

workers <- data.frame(
  worker_id = 1:n,
  role_group = sample(
    c("administrative", "technical", "professional", "support"),
    n,
    replace = TRUE,
    prob = c(0.30, 0.25, 0.30, 0.15)
  ),
  employment_status = sample(
    c("employee", "contractor", "temporary"),
    n,
    replace = TRUE,
    prob = c(0.70, 0.20, 0.10)
  ),
  ai_exposure = runif(n, 0, 1),
  wage_security = runif(n, 0.30, 1.00),
  autonomy = runif(n, 0.20, 1.00),
  skill_development = runif(n, 0.10, 1.00),
  health_safety = runif(n, 0.40, 1.00),
  worker_voice = runif(n, 0.10, 1.00),
  monitoring_burden = runif(n, 0, 1),
  training_access = runif(n, 0, 1),
  workload_intensity = runif(n, 0, 1),
  schedule_predictability = runif(n, 0.20, 1.00)
)

workers$job_quality_score <-
  0.18 * workers$wage_security +
  0.18 * workers$autonomy +
  0.18 * workers$skill_development +
  0.14 * workers$health_safety +
  0.14 * workers$worker_voice +
  0.10 * workers$schedule_predictability -
  0.08 * workers$monitoring_burden -
  0.08 * workers$workload_intensity

workers$job_quality_score <- pmax(0, pmin(1, workers$job_quality_score))

workers$transition_priority <- ifelse(
  workers$ai_exposure > 0.60 &
    workers$training_access < 0.50 &
    workers$job_quality_score < 0.55,
  1,
  0
)

workers$consultation_priority <- ifelse(
  workers$monitoring_burden > 0.60 |
    workers$workload_intensity > 0.65 |
    workers$worker_voice < 0.35,
  1,
  0
)

role_summary <- aggregate(
  cbind(
    ai_exposure,
    job_quality_score,
    monitoring_burden,
    workload_intensity,
    training_access,
    worker_voice,
    transition_priority,
    consultation_priority
  ) ~ role_group,
  data = workers,
  FUN = mean
)

status_summary <- aggregate(
  cbind(
    ai_exposure,
    job_quality_score,
    monitoring_burden,
    training_access,
    transition_priority
  ) ~ employment_status,
  data = workers,
  FUN = mean
)

write.csv(workers, file.path(output_dir, "synthetic_worker_job_quality_records.csv"), row.names = FALSE)
write.csv(role_summary, file.path(output_dir, "job_quality_role_group_summary.csv"), row.names = FALSE)
write.csv(status_summary, file.path(output_dir, "job_quality_employment_status_summary.csv"), row.names = FALSE)

print(role_summary)
print(status_summary)
