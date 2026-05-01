# Artificial Intelligence in Decision Support Systems
# R workflow: decision quality and scenario review.

set.seed(42)

article_dir <- normalizePath(file.path(getwd(), "articles/artificial-intelligence/artificial-intelligence-in-decision-support-systems"), mustWork = FALSE)

if (!dir.exists(article_dir)) {
  article_dir <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."), mustWork = FALSE)
}

output_dir <- file.path(article_dir, "outputs")

if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

n <- 150

options <- data.frame(
  option_id = paste0("A", sprintf("%03d", 1:n)),
  predicted_risk = rbeta(n, shape1 = 2.5, shape2 = 4.0),
  benefit_if_successful = pmax(rnorm(n, mean = 100, sd = 25), 10),
  cost = pmax(rnorm(n, mean = 35, sd = 10), 5),
  uncertainty = runif(n, min = 0.05, max = 0.45),
  service_population = sample(100:10000, size = n, replace = TRUE),
  equity_priority = sample(c(0, 1), size = n, replace = TRUE, prob = c(0.75, 0.25)),
  capacity_required = sample(1:5, size = n, replace = TRUE)
)

options$population_weight <- options$service_population / max(options$service_population)

options$expected_benefit <- options$predicted_risk * options$benefit_if_successful

options$baseline_utility <- options$expected_benefit -
  options$cost +
  15 * options$population_weight +
  10 * options$equity_priority -
  8 * options$uncertainty

options$optimistic_utility <- options$baseline_utility + 15 * options$uncertainty
options$pessimistic_utility <- options$baseline_utility - 20 * options$uncertainty

options$robust_score <- pmin(
  options$baseline_utility,
  options$optimistic_utility,
  options$pessimistic_utility
)

options$human_review_required <- options$uncertainty > 0.30 |
  options$equity_priority == 1 |
  options$predicted_risk > 0.70

priority_table <- options[order(-options$robust_score), ]

scenario_summary <- data.frame(
  scenario = c("optimistic", "baseline", "pessimistic"),
  mean_utility = c(
    mean(options$optimistic_utility),
    mean(options$baseline_utility),
    mean(options$pessimistic_utility)
  ),
  best_utility = c(
    max(options$optimistic_utility),
    max(options$baseline_utility),
    max(options$pessimistic_utility)
  )
)

governance_summary <- data.frame(
  options_reviewed = nrow(options),
  human_review_required = sum(options$human_review_required),
  equity_priority_options = sum(options$equity_priority),
  mean_uncertainty = mean(options$uncertainty),
  mean_baseline_utility = mean(options$baseline_utility),
  mean_robust_score = mean(options$robust_score)
)

write.csv(priority_table, file.path(output_dir, "r_decision_priority_table.csv"), row.names = FALSE)
write.csv(scenario_summary, file.path(output_dir, "r_scenario_summary.csv"), row.names = FALSE)
write.csv(governance_summary, file.path(output_dir, "r_decision_governance_summary.csv"), row.names = FALSE)

print("Top decision options")
print(head(priority_table, 10))

print("Scenario summary")
print(scenario_summary)

print("Governance summary")
print(governance_summary)
