# Planning, Search, and Sequential Decision Systems
# R workflow: sequential decision evaluation summary.

set.seed(42)

article_dir <- normalizePath(file.path(getwd(), "articles/artificial-intelligence/planning-search-and-sequential-decision-systems"), mustWork = FALSE)

if (!dir.exists(article_dir)) {
  article_dir <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."), mustWork = FALSE)
}

output_dir <- file.path(article_dir, "outputs")

if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

n <- 240

records <- data.frame(
  evaluation_id = paste0("PLAN-EVAL-", sprintf("%03d", 1:n)),
  system_type = sample(
    c("heuristic_search", "reinforcement_learning", "tool_using_agent", "workflow_planner", "resource_allocator"),
    size = n,
    replace = TRUE
  ),
  plan_cost = runif(n, min = 0.05, max = 0.80),
  uncertainty_risk = runif(n, min = 0.00, max = 0.70),
  constraint_violation_risk = runif(n, min = 0.00, max = 0.40),
  irreversibility_risk = runif(n, min = 0.00, max = 0.35),
  policy_performance = runif(n, min = 0.45, max = 0.98),
  human_review_score = runif(n, min = 0.40, max = 1.00),
  traceability_score = runif(n, min = 0.35, max = 1.00)
)

records$planning_risk <- 0.30 * records$plan_cost +
  0.25 * records$uncertainty_risk +
  0.25 * records$constraint_violation_risk +
  0.20 * records$irreversibility_risk

records$governance_readiness <- 0.45 * records$human_review_score +
  0.55 * records$traceability_score

records$review_required <- records$planning_risk > 0.28 |
  records$constraint_violation_risk > 0.20 |
  records$irreversibility_risk > 0.15 |
  records$uncertainty_risk > 0.45 |
  records$governance_readiness < 0.65

system_summary <- aggregate(
  cbind(
    plan_cost,
    uncertainty_risk,
    constraint_violation_risk,
    irreversibility_risk,
    policy_performance,
    planning_risk,
    governance_readiness,
    review_required
  ) ~ system_type,
  data = records,
  FUN = mean
)

governance_summary <- data.frame(
  evaluations_reviewed = nrow(records),
  review_required = sum(records$review_required),
  mean_policy_performance = mean(records$policy_performance),
  mean_planning_risk = mean(records$planning_risk),
  max_planning_risk = max(records$planning_risk),
  max_constraint_violation_risk = max(records$constraint_violation_risk),
  max_irreversibility_risk = max(records$irreversibility_risk),
  mean_governance_readiness = mean(records$governance_readiness)
)

write.csv(records, file.path(output_dir, "r_sequential_decision_records.csv"), row.names = FALSE)
write.csv(system_summary, file.path(output_dir, "r_planning_system_summary.csv"), row.names = FALSE)
write.csv(governance_summary, file.path(output_dir, "r_planning_governance_summary.csv"), row.names = FALSE)

print("System summary")
print(system_summary)

print("Governance summary")
print(governance_summary)
