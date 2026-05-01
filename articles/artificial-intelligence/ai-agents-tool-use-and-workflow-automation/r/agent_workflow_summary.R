# AI Agents, Tool Use, and Workflow Automation
# R workflow: agent workflow evaluation summary and governance review.

set.seed(42)

article_dir <- normalizePath(file.path(getwd(), "articles/artificial-intelligence/ai-agents-tool-use-and-workflow-automation"), mustWork = FALSE)

if (!dir.exists(article_dir)) {
  article_dir <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."), mustWork = FALSE)
}

output_dir <- file.path(article_dir, "outputs")

if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

n <- 260

workflow_types <- c(
  "research_summary",
  "database_query",
  "code_execution",
  "ticket_creation",
  "calendar_coordination",
  "document_update",
  "multi_step_operations"
)

tool_risk_levels <- c("read_only", "compute", "write", "external_action", "sensitive")

records <- data.frame(
  eval_id = paste0("AGENT-EVAL-", sprintf("%03d", 1:n)),
  workflow_type = sample(workflow_types, size = n, replace = TRUE),
  tool_risk = sample(tool_risk_levels, size = n, replace = TRUE, prob = c(0.40, 0.25, 0.18, 0.09, 0.08)),
  steps = sample(2:18, size = n, replace = TRUE),
  tool_calls = sample(1:16, size = n, replace = TRUE),
  task_success = runif(n, min = 0.45, max = 1.00),
  tool_selection_score = runif(n, min = 0.45, max = 1.00),
  argument_validity = runif(n, min = 0.50, max = 1.00),
  permission_compliance = runif(n, min = 0.60, max = 1.00),
  error_recovery_score = runif(n, min = 0.35, max = 1.00),
  safety_score = runif(n, min = 0.55, max = 1.00),
  auditability_score = runif(n, min = 0.55, max = 1.00),
  human_review_score = runif(n, min = 0.45, max = 1.00),
  latency_seconds = rgamma(n, shape = 2.6, scale = 1.4),
  token_cost_index = runif(n, min = 0.05, max = 1.00)
)

records$confirmation_required <- ifelse(
  records$tool_risk %in% c("write", "external_action", "sensitive"),
  1,
  0
)

records$confirmation_obtained <- ifelse(
  records$confirmation_required == 1,
  rbinom(n, size = 1, prob = 0.88),
  1
)

records$denied_action_attempt <- rbinom(n, size = 1, prob = 0.12)
records$prompt_injection_exposure <- rbinom(n, size = 1, prob = 0.14)

records$execution_quality_score <- 0.25 * records$task_success +
  0.20 * records$tool_selection_score +
  0.20 * records$argument_validity +
  0.15 * records$error_recovery_score +
  0.10 * records$auditability_score +
  0.10 * records$human_review_score

records$safety_governance_score <- 0.30 * records$safety_score +
  0.25 * records$permission_compliance +
  0.20 * records$auditability_score +
  0.15 * records$human_review_score +
  0.10 * records$argument_validity

records$risk_weight <- ifelse(
  records$tool_risk == "read_only",
  0.05,
  ifelse(
    records$tool_risk == "compute",
    0.15,
    ifelse(
      records$tool_risk == "write",
      0.30,
      ifelse(records$tool_risk == "external_action", 0.45, 0.55)
    )
  )
)

records$workflow_complexity_index <- pmin(
  (records$steps / 20) + (records$tool_calls / 20),
  1.5
)

records$operational_cost_index <- pmin(
  (records$latency_seconds / 15) + records$token_cost_index,
  1.5
)

records$agent_system_risk <- 0.20 * (1 - records$execution_quality_score) +
  0.25 * (1 - records$safety_governance_score) +
  0.15 * records$risk_weight +
  0.10 * records$workflow_complexity_index +
  0.10 * records$operational_cost_index +
  0.10 * records$denied_action_attempt +
  0.10 * records$prompt_injection_exposure

records$review_required <- records$agent_system_risk > 0.42 |
  records$tool_risk %in% c("external_action", "sensitive") |
  records$task_success < 0.65 |
  records$argument_validity < 0.70 |
  records$permission_compliance < 0.80 |
  records$safety_score < 0.75 |
  records$denied_action_attempt == 1 |
  records$prompt_injection_exposure == 1 |
  (records$confirmation_required == 1 & records$confirmation_obtained == 0)

workflow_summary <- aggregate(
  cbind(
    steps,
    tool_calls,
    execution_quality_score,
    safety_governance_score,
    agent_system_risk,
    review_required,
    denied_action_attempt,
    prompt_injection_exposure
  ) ~ workflow_type,
  data = records,
  FUN = mean
)

tool_risk_summary <- aggregate(
  cbind(
    execution_quality_score,
    safety_governance_score,
    agent_system_risk,
    review_required,
    confirmation_required,
    confirmation_obtained
  ) ~ tool_risk,
  data = records,
  FUN = mean
)

governance_summary <- data.frame(
  evaluations_reviewed = nrow(records),
  review_required = sum(records$review_required),
  sensitive_or_external_action_cases = sum(records$tool_risk %in% c("external_action", "sensitive")),
  failed_confirmation_cases = sum(records$confirmation_required == 1 & records$confirmation_obtained == 0),
  denied_action_attempts = sum(records$denied_action_attempt),
  prompt_injection_exposures = sum(records$prompt_injection_exposure),
  mean_execution_quality = mean(records$execution_quality_score),
  mean_safety_governance = mean(records$safety_governance_score),
  mean_agent_system_risk = mean(records$agent_system_risk)
)

write.csv(records, file.path(output_dir, "r_agent_workflow_records.csv"), row.names = FALSE)
write.csv(workflow_summary, file.path(output_dir, "r_agent_workflow_summary.csv"), row.names = FALSE)
write.csv(tool_risk_summary, file.path(output_dir, "r_agent_tool_risk_summary.csv"), row.names = FALSE)
write.csv(governance_summary, file.path(output_dir, "r_agent_governance_summary.csv"), row.names = FALSE)

print("Workflow summary")
print(workflow_summary)

print("Tool-risk summary")
print(tool_risk_summary)

print("Governance summary")
print(governance_summary)
