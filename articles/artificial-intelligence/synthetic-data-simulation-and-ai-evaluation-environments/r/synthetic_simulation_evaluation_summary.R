# Synthetic Data, Simulation, and AI Evaluation Environments
# R workflow: synthetic data and simulation evaluation summary.

set.seed(42)

article_dir <- normalizePath(file.path(getwd(), "articles/artificial-intelligence/synthetic-data-simulation-and-ai-evaluation-environments"), mustWork = FALSE)

if (!dir.exists(article_dir)) {
  article_dir <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."), mustWork = FALSE)
}

output_dir <- file.path(article_dir, "outputs")

if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

n <- 240

records <- data.frame(
  evaluation_id = paste0("SYN-EVAL-", sprintf("%03d", 1:n)),
  artifact_type = sample(
    c("tabular_synthetic_data", "scenario_simulation", "digital_twin", "benchmark_environment", "llm_eval_set"),
    size = n,
    replace = TRUE
  ),
  fidelity_risk = runif(n, min = 0.02, max = 0.35),
  utility_gap = runif(n, min = 0.00, max = 0.12),
  privacy_proximity_risk = runif(n, min = 0.00, max = 0.10),
  rare_case_coverage_gap = runif(n, min = 0.00, max = 0.12),
  sim_to_real_gap = runif(n, min = 0.00, max = 0.30),
  benchmark_overfit_risk = runif(n, min = 0.00, max = 0.25),
  expert_review_score = runif(n, min = 0.45, max = 1.00),
  documentation_score = runif(n, min = 0.40, max = 1.00)
)

records$evaluation_risk <- 0.22 * records$fidelity_risk +
  0.18 * records$utility_gap +
  0.20 * records$privacy_proximity_risk +
  0.16 * records$rare_case_coverage_gap +
  0.16 * records$sim_to_real_gap +
  0.08 * records$benchmark_overfit_risk

records$governance_readiness <- 0.55 * records$expert_review_score +
  0.45 * records$documentation_score

records$review_required <- records$evaluation_risk > 0.12 |
  records$privacy_proximity_risk > 0.05 |
  records$rare_case_coverage_gap > 0.06 |
  records$sim_to_real_gap > 0.18 |
  records$governance_readiness < 0.65

artifact_summary <- aggregate(
  cbind(
    fidelity_risk,
    utility_gap,
    privacy_proximity_risk,
    rare_case_coverage_gap,
    sim_to_real_gap,
    benchmark_overfit_risk,
    evaluation_risk,
    governance_readiness,
    review_required
  ) ~ artifact_type,
  data = records,
  FUN = mean
)

governance_summary <- data.frame(
  evaluations_reviewed = nrow(records),
  review_required = sum(records$review_required),
  mean_evaluation_risk = mean(records$evaluation_risk),
  max_evaluation_risk = max(records$evaluation_risk),
  max_privacy_proximity_risk = max(records$privacy_proximity_risk),
  max_sim_to_real_gap = max(records$sim_to_real_gap),
  mean_governance_readiness = mean(records$governance_readiness)
)

write.csv(records, file.path(output_dir, "r_synthetic_simulation_evaluation_records.csv"), row.names = FALSE)
write.csv(artifact_summary, file.path(output_dir, "r_artifact_type_evaluation_summary.csv"), row.names = FALSE)
write.csv(governance_summary, file.path(output_dir, "r_synthetic_governance_summary.csv"), row.names = FALSE)

print("Artifact summary")
print(artifact_summary)

print("Governance summary")
print(governance_summary)
