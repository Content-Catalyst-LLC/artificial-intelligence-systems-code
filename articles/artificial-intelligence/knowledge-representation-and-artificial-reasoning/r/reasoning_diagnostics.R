# Knowledge Representation and Reasoning Diagnostics
#
# This educational workflow simulates rule coverage and inference diagnostics.

set.seed(42)

n <- 1000

reasoning_log <- data.frame(
  domain = sample(
    c("medicine", "law", "infrastructure", "environment"),
    n,
    replace = TRUE,
    prob = c(0.25, 0.25, 0.25, 0.25)
  ),
  rule_type = sample(
    c("deductive", "default", "probabilistic", "constraint"),
    n,
    replace = TRUE,
    prob = c(0.35, 0.25, 0.25, 0.15)
  ),
  evidence_quality = sample(
    c("high", "medium", "low"),
    n,
    replace = TRUE,
    prob = c(0.45, 0.35, 0.20)
  )
)

base_success <- ifelse(
  reasoning_log$rule_type == "deductive", 0.92,
  ifelse(reasoning_log$rule_type == "constraint", 0.86,
  ifelse(reasoning_log$rule_type == "probabilistic", 0.78, 0.72))
)

evidence_modifier <- ifelse(
  reasoning_log$evidence_quality == "high", 1.00,
  ifelse(reasoning_log$evidence_quality == "medium", 0.88, 0.70)
)

reasoning_log$successful_inference <- rbinom(
  n,
  size = 1,
  prob = pmin(base_success * evidence_modifier, 0.99)
)

summary_table <- aggregate(
  successful_inference ~ domain + rule_type + evidence_quality,
  data = reasoning_log,
  FUN = mean
)

names(summary_table)[4] <- "simulated_success_rate"

coverage_table <- aggregate(
  successful_inference ~ rule_type,
  data = reasoning_log,
  FUN = length
)

names(coverage_table)[2] <- "rule_applications"

dir.create("../outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(summary_table, "../outputs/r_reasoning_success_diagnostics.csv", row.names = FALSE)
write.csv(coverage_table, "../outputs/r_rule_coverage_diagnostics.csv", row.names = FALSE)

print(summary_table)
print(coverage_table)
