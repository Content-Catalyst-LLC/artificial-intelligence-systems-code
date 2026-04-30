# Hybrid AI Diagnostics
#
# This educational workflow simulates:
# - neural model scores
# - symbolic rule triggers
# - hybrid final decisions
# - audit summaries by decision source

set.seed(42)

n <- 800

hybrid_data <- data.frame(
  entity_id = paste0("E-", sprintf("%04d", 1:n)),
  neural_risk_score = rbeta(n, 2.2, 4.0),
  condition_score = runif(n, min = 0.10, max = 0.98),
  criticality = sample(
    c("low", "medium", "high"),
    n,
    replace = TRUE,
    prob = c(0.45, 0.35, 0.20)
  ),
  sensitive_workflow = rbinom(n, size = 1, prob = 0.20)
)

hybrid_data$neural_recommendation <- hybrid_data$neural_risk_score >= 0.55

hybrid_data$rule_critical_low_condition <- hybrid_data$criticality == "high" &
  hybrid_data$condition_score <= 0.35

hybrid_data$rule_sensitive_workflow <- hybrid_data$sensitive_workflow == 1 &
  hybrid_data$neural_risk_score >= 0.45

hybrid_data$rule_medium_severe_condition <- hybrid_data$criticality == "medium" &
  hybrid_data$condition_score <= 0.25

hybrid_data$symbolic_review_required <- hybrid_data$rule_critical_low_condition |
  hybrid_data$rule_sensitive_workflow |
  hybrid_data$rule_medium_severe_condition

hybrid_data$hybrid_decision <- hybrid_data$neural_recommendation |
  hybrid_data$symbolic_review_required

hybrid_data$decision_source <- ifelse(
  hybrid_data$neural_recommendation & hybrid_data$symbolic_review_required,
  "neural_and_symbolic",
  ifelse(
    hybrid_data$neural_recommendation & !hybrid_data$symbolic_review_required,
    "neural_only",
    ifelse(
      !hybrid_data$neural_recommendation & hybrid_data$symbolic_review_required,
      "symbolic_only",
      "no_review"
    )
  )
)

summary_table <- aggregate(
  cbind(neural_risk_score, condition_score, hybrid_decision) ~ decision_source,
  data = hybrid_data,
  FUN = mean
)

count_table <- aggregate(
  entity_id ~ decision_source,
  data = hybrid_data,
  FUN = length
)

names(count_table)[2] <- "n"

summary_table <- merge(summary_table, count_table, by = "decision_source")

rule_summary <- data.frame(
  rule = c(
    "critical_low_condition",
    "sensitive_workflow",
    "medium_severe_condition"
  ),
  trigger_count = c(
    sum(hybrid_data$rule_critical_low_condition),
    sum(hybrid_data$rule_sensitive_workflow),
    sum(hybrid_data$rule_medium_severe_condition)
  )
)

dir.create("../outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(hybrid_data, "../outputs/r_hybrid_ai_audit_dataset.csv", row.names = FALSE)
write.csv(summary_table, "../outputs/r_hybrid_ai_decision_source_summary.csv", row.names = FALSE)
write.csv(rule_summary, "../outputs/r_hybrid_ai_rule_summary.csv", row.names = FALSE)

print(summary_table)
print(rule_summary)
