# Robustness and Adversarial Resilience in Machine Learning
# R workflow: robustness evaluation summary and governance review.

set.seed(42)

article_dir <- normalizePath(file.path(getwd(), "articles/artificial-intelligence/robustness-and-adversarial-resilience-in-machine-learning"), mustWork = FALSE)

if (!dir.exists(article_dir)) {
  article_dir <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."), mustWork = FALSE)
}

output_dir <- file.path(article_dir, "outputs")

if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

n <- 280

system_types <- c(
  "image_classifier",
  "tabular_risk_model",
  "text_classifier",
  "rag_assistant",
  "llm_application",
  "ai_agent",
  "multimodal_system"
)

attack_types <- c(
  "corruption",
  "evasion",
  "data_poisoning",
  "prompt_injection",
  "retrieval_poisoning",
  "model_extraction",
  "feedback_manipulation",
  "out_of_distribution"
)

records <- data.frame(
  eval_id = paste0("ROBUST-EVAL-", sprintf("%03d", 1:n)),
  system_type = sample(system_types, size = n, replace = TRUE),
  attack_type = sample(attack_types, size = n, replace = TRUE),
  clean_performance = runif(n, min = 0.78, max = 0.98),
  detection_score = runif(n, min = 0.35, max = 0.98),
  containment_score = runif(n, min = 0.40, max = 1.00),
  recovery_score = runif(n, min = 0.35, max = 1.00),
  auditability_score = runif(n, min = 0.55, max = 1.00),
  privacy_control_score = runif(n, min = 0.45, max = 1.00),
  human_review_score = runif(n, min = 0.45, max = 1.00),
  attack_success_rate = runif(n, min = 0.02, max = 0.55),
  incident_severity = sample(1:5, size = n, replace = TRUE, prob = c(0.32, 0.28, 0.20, 0.13, 0.07)),
  exposure_level = runif(n, min = 0.05, max = 1.00)
)

records$corruption_performance <- pmax(
  0,
  records$clean_performance - runif(n, min = 0.02, max = 0.22)
)

records$adversarial_performance <- pmax(
  0,
  records$clean_performance - runif(n, min = 0.05, max = 0.38)
)

records$ood_performance <- pmax(
  0,
  records$clean_performance - runif(n, min = 0.04, max = 0.30)
)

records$corruption_drop <- records$clean_performance - records$corruption_performance
records$adversarial_drop <- records$clean_performance - records$adversarial_performance
records$ood_drop <- records$clean_performance - records$ood_performance

records$robustness_score <- pmin(
  1,
  pmax(
    0,
    1 - (
      0.30 * records$corruption_drop +
        0.45 * records$adversarial_drop +
        0.25 * records$ood_drop
    )
  )
)

records$resilience_score <- 0.25 * records$detection_score +
  0.25 * records$containment_score +
  0.20 * records$recovery_score +
  0.15 * records$auditability_score +
  0.15 * records$human_review_score

records$security_control_score <- 0.35 * records$detection_score +
  0.25 * records$privacy_control_score +
  0.20 * records$containment_score +
  0.20 * records$auditability_score

records$impact_index <- pmin(
  1,
  0.45 * records$attack_success_rate +
    0.30 * (records$incident_severity / 5) +
    0.25 * records$exposure_level
)

records$adversarial_system_risk <- 0.25 * (1 - records$robustness_score) +
  0.25 * (1 - records$resilience_score) +
  0.20 * (1 - records$security_control_score) +
  0.30 * records$impact_index

records$review_required <- records$adversarial_system_risk > 0.42 |
  records$adversarial_drop > 0.22 |
  records$attack_success_rate > 0.30 |
  records$incident_severity >= 4 |
  records$privacy_control_score < 0.65 |
  records$containment_score < 0.65 |
  records$recovery_score < 0.60

attack_summary <- aggregate(
  cbind(
    clean_performance,
    adversarial_drop,
    robustness_score,
    resilience_score,
    attack_success_rate,
    adversarial_system_risk,
    review_required
  ) ~ attack_type,
  data = records,
  FUN = mean
)

system_summary <- aggregate(
  cbind(
    clean_performance,
    adversarial_drop,
    robustness_score,
    resilience_score,
    attack_success_rate,
    adversarial_system_risk,
    review_required
  ) ~ system_type,
  data = records,
  FUN = mean
)

governance_summary <- data.frame(
  evaluations_reviewed = nrow(records),
  review_required = sum(records$review_required),
  high_severity_cases = sum(records$incident_severity >= 4),
  high_attack_success_cases = sum(records$attack_success_rate > 0.30),
  mean_robustness_score = mean(records$robustness_score),
  mean_resilience_score = mean(records$resilience_score),
  mean_security_control_score = mean(records$security_control_score),
  mean_adversarial_system_risk = mean(records$adversarial_system_risk)
)

write.csv(records, file.path(output_dir, "r_robustness_evaluation_records.csv"), row.names = FALSE)
write.csv(attack_summary, file.path(output_dir, "r_attack_type_summary.csv"), row.names = FALSE)
write.csv(system_summary, file.path(output_dir, "r_system_type_robustness_summary.csv"), row.names = FALSE)
write.csv(governance_summary, file.path(output_dir, "r_robustness_governance_summary.csv"), row.names = FALSE)

print("Attack summary")
print(attack_summary)

print("System summary")
print(system_summary)

print("Governance summary")
print(governance_summary)
