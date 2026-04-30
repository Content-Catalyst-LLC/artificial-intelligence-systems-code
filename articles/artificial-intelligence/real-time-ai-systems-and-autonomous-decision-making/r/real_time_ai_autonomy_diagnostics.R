# Real-Time AI Systems and Autonomous Decision-Making Diagnostics
#
# This educational workflow simulates:
# - real-time AI task latencies
# - deadlines
# - deadline misses
# - latency margins
# - fallback flags

set.seed(42)

n <- 1500

task_type <- sample(
  c("perception", "tracking", "planning", "control", "safety_monitor"),
  n,
  replace = TRUE,
  prob = c(0.32, 0.20, 0.18, 0.20, 0.10)
)

deadline_ms <- sample(
  c(20, 40, 80, 120),
  n,
  replace = TRUE,
  prob = c(0.20, 0.35, 0.30, 0.15)
)

risk_level <- sample(
  c("low", "medium", "high"),
  n,
  replace = TRUE,
  prob = c(0.45, 0.35, 0.20)
)

base_latency <- ifelse(
  task_type == "perception", 18,
  ifelse(
    task_type == "tracking", 10,
    ifelse(
      task_type == "planning", 35,
      ifelse(task_type == "control", 8, 12)
    )
  )
)

latency_sd <- ifelse(
  task_type == "perception", 8,
  ifelse(
    task_type == "tracking", 4,
    ifelse(
      task_type == "planning", 15,
      ifelse(task_type == "control", 3, 5)
    )
  )
)

latency_ms <- pmax(
  1,
  rnorm(n, mean = base_latency + 15, sd = latency_sd)
)

rtai_results <- data.frame(
  task_id = paste0("rtai-", sprintf("%04d", 1:n)),
  task_type = task_type,
  deadline_ms = deadline_ms,
  risk_level = risk_level,
  latency_ms = latency_ms
)

rtai_results$deadline_miss <- rtai_results$latency_ms > rtai_results$deadline_ms
rtai_results$latency_margin_ms <- rtai_results$deadline_ms - rtai_results$latency_ms

rtai_results$fallback_required <-
  rtai_results$deadline_miss |
  (rtai_results$risk_level == "high" & rtai_results$latency_margin_ms < 10)

rtai_results$timing_risk_score <- pmin(
  2,
  pmax(
    0,
    1 - (rtai_results$latency_margin_ms / rtai_results$deadline_ms)
  )
)

summary_table <- aggregate(
  cbind(
    latency_ms,
    deadline_miss,
    fallback_required,
    latency_margin_ms,
    timing_risk_score
  ) ~ task_type + risk_level,
  data = rtai_results,
  FUN = mean
)

dir.create("../outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(rtai_results, "../outputs/r_real_time_ai_latency_results.csv", row.names = FALSE)
write.csv(summary_table, "../outputs/r_real_time_ai_latency_summary.csv", row.names = FALSE)

print(summary_table)
