# Large Language Models and Foundation Model Systems
# R workflow: LLM evaluation summary and risk review.

set.seed(42)

article_dir <- normalizePath(file.path(getwd(), "articles/artificial-intelligence/large-language-models-and-foundation-model-systems"), mustWork = FALSE)

if (!dir.exists(article_dir)) {
  article_dir <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."), mustWork = FALSE)
}

output_dir <- file.path(article_dir, "outputs")

if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

n <- 220

use_cases <- c(
  "knowledge_search",
  "document_summary",
  "code_assistance",
  "policy_explanation",
  "research_synthesis",
  "customer_support",
  "decision_support"
)

risk_levels <- c("low", "medium", "high")

records <- data.frame(
  eval_id = paste0("LLM-EVAL-", sprintf("%03d", 1:n)),
  use_case = sample(use_cases, size = n, replace = TRUE),
  risk_level = sample(risk_levels, size = n, replace = TRUE, prob = c(0.50, 0.35, 0.15)),
  task_quality = runif(n, min = 0.55, max = 0.98),
  grounding_score = runif(n, min = 0.35, max = 0.98),
  factuality_score = runif(n, min = 0.45, max = 0.99),
  citation_fidelity = runif(n, min = 0.35, max = 0.98),
  safety_score = runif(n, min = 0.55, max = 1.00),
  prompt_injection_resistance = runif(n, min = 0.40, max = 0.98),
  privacy_control_score = runif(n, min = 0.55, max = 1.00),
  input_tokens = sample(400:9000, size = n, replace = TRUE),
  output_tokens = sample(100:1800, size = n, replace = TRUE),
  tool_calls = sample(0:4, size = n, replace = TRUE),
  latency_seconds = rgamma(n, shape = 2.5, scale = 1.2)
)

records$total_tokens <- records$input_tokens + records$output_tokens

records$quality_score <- 0.25 * records$task_quality +
  0.25 * records$grounding_score +
  0.25 * records$factuality_score +
  0.25 * records$citation_fidelity

records$security_and_safety_score <- 0.40 * records$safety_score +
  0.30 * records$prompt_injection_resistance +
  0.30 * records$privacy_control_score

records$operational_cost_index <- pmin(
  (records$total_tokens / 10000) +
    (records$latency_seconds / 20) +
    (records$tool_calls / 10),
  1.5
)

records$risk_weight <- ifelse(
  records$risk_level == "low",
  0.10,
  ifelse(records$risk_level == "medium", 0.25, 0.45)
)

records$llm_system_risk <- 0.25 * (1 - records$quality_score) +
  0.25 * (1 - records$security_and_safety_score) +
  0.20 * (1 - records$grounding_score) +
  0.15 * records$operational_cost_index +
  0.15 * records$risk_weight

records$review_required <- records$llm_system_risk > 0.40 |
  records$risk_level == "high" |
  records$grounding_score < 0.60 |
  records$factuality_score < 0.65 |
  records$prompt_injection_resistance < 0.60 |
  records$privacy_control_score < 0.70

use_case_summary <- aggregate(
  cbind(
    quality_score,
    grounding_score,
    factuality_score,
    security_and_safety_score,
    llm_system_risk,
    review_required,
    total_tokens,
    latency_seconds
  ) ~ use_case,
  data = records,
  FUN = mean
)

risk_summary <- aggregate(
  cbind(
    quality_score,
    grounding_score,
    security_and_safety_score,
    llm_system_risk,
    review_required
  ) ~ risk_level,
  data = records,
  FUN = mean
)

governance_summary <- data.frame(
  evaluations_reviewed = nrow(records),
  review_required = sum(records$review_required),
  high_risk_cases = sum(records$risk_level == "high"),
  mean_quality_score = mean(records$quality_score),
  mean_grounding_score = mean(records$grounding_score),
  mean_system_risk = mean(records$llm_system_risk),
  mean_total_tokens = mean(records$total_tokens),
  mean_latency_seconds = mean(records$latency_seconds)
)

write.csv(records, file.path(output_dir, "r_llm_evaluation_records.csv"), row.names = FALSE)
write.csv(use_case_summary, file.path(output_dir, "r_llm_use_case_summary.csv"), row.names = FALSE)
write.csv(risk_summary, file.path(output_dir, "r_llm_risk_summary.csv"), row.names = FALSE)
write.csv(governance_summary, file.path(output_dir, "r_llm_governance_summary.csv"), row.names = FALSE)

print("Use-case summary")
print(use_case_summary)

print("Risk summary")
print(risk_summary)

print("Governance summary")
print(governance_summary)
