# Job-quality and automation-risk monitoring workflow.
# This script creates synthetic worker records and summarizes AI exposure,
# job quality, monitoring burden, training access, and transition priority.

set.seed(42)

article_dir <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."), mustWork = FALSE)
output_dir <- file.path(article_dir, "outputs")
dir.create(output_dir, showWarnings = FALSE, recursive = TRUE)

n <- 600

workers <- data.frame(
  worker_id = 1:n,
  role_group = sample(
    c("administrative", "technical", "professional", "support"),
    n,
    replace = TRUE,
    prob = c(0.30, 0.25, 0.30, 0.15)
  ),
  ai_exposure = runif(n, 0, 1),
  wage_security = runif(n, 0.30, 1.00),
  autonomy = runif(n, 0.20, 1.00),
  skill_development = runif(n, 0.10, 1.00),
  health_safety = runif(n, 0.40, 1.00),
  worker_voice = runif(n, 0.10, 1.00),
  monitoring_burden = runif(n, 0, 1),
  training_access = runif(n, 0, 1)
)

workers$job_quality_score <-
  0.20 * workers$wage_security +
  0.20 * workers$autonomy +
  0.20 * workers$skill_development +
  0.15 * workers$health_safety +
  0.15 * workers$worker_voice -
  0.10 * workers$monitoring_burden

workers$transition_priority <- ifelse(
  workers$ai_exposure > 0.60 &
    workers$training_access < 0.50 &
    workers$job_quality_score < 0.50,
  1,
  0
)

summary_table <- aggregate(
  cbind(
    ai_exposure,
    job_quality_score,
    monitoring_burden,
    training_access,
    transition_priority
  ) ~ role_group,
  data = workers,
  FUN = mean
)

write.csv(workers, file.path(output_dir, "synthetic_worker_job_quality_records.csv"), row.names = FALSE)
write.csv(summary_table, file.path(output_dir, "job_quality_monitoring_summary.csv"), row.names = FALSE)

print(summary_table)
