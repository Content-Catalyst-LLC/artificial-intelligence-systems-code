# Artificial Intelligence as a Systems Discipline
# R workflow: lifecycle governance and assurance review.

set.seed(42)

article_dir <- normalizePath(file.path(getwd(), "articles/artificial-intelligence/artificial-intelligence-as-a-systems-discipline"), mustWork = FALSE)

if (!dir.exists(article_dir)) {
  article_dir <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."), mustWork = FALSE)
}

output_dir <- file.path(article_dir, "outputs")

if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

n <- 150

systems <- data.frame(
  system_id = paste0("AI-SYS-", sprintf("%03d", 1:n)),
  domain = sample(
    c(
      "decision_support",
      "generative_content",
      "infrastructure",
      "environmental_monitoring",
      "scientific_research",
      "customer_operations",
      "internal_productivity"
    ),
    size = n,
    replace = TRUE
  ),
  risk_tier = sample(
    c("low", "medium", "high"),
    size = n,
    replace = TRUE,
    prob = c(0.35, 0.45, 0.20)
  ),
  data_quality = runif(n, min = 0.40, max = 0.98),
  model_reliability = runif(n, min = 0.45, max = 0.97),
  infrastructure_readiness = runif(n, min = 0.35, max = 0.96),
  human_oversight = runif(n, min = 0.25, max = 0.95),
  monitoring_coverage = runif(n, min = 0.20, max = 0.95),
  governance_readiness = runif(n, min = 0.20, max = 0.95),
  explainability = runif(n, min = 0.20, max = 0.95),
  security_readiness = runif(n, min = 0.30, max = 0.96),
  external_impact = runif(n, min = 0.05, max = 0.90)
)

systems$high_stakes <- ifelse(systems$risk_tier == "high", 1, 0)

systems$technical_maturity <- 0.30 * systems$data_quality +
  0.30 * systems$model_reliability +
  0.20 * systems$infrastructure_readiness +
  0.20 * systems$security_readiness

systems$governance_maturity <- 0.30 * systems$human_oversight +
  0.30 * systems$monitoring_coverage +
  0.25 * systems$governance_readiness +
  0.15 * systems$explainability

systems$system_maturity <- 0.50 * systems$technical_maturity +
  0.50 * systems$governance_maturity

systems$systemic_risk <- 0.30 * (1 - systems$system_maturity) +
  0.20 * (1 - systems$monitoring_coverage) +
  0.20 * (1 - systems$governance_readiness) +
  0.15 * systems$external_impact +
  0.15 * systems$high_stakes

systems$review_required <- systems$systemic_risk > 0.45 |
  systems$governance_readiness < 0.45 |
  systems$monitoring_coverage < 0.40 |
  (systems$high_stakes == 1 & systems$human_oversight < 0.65)

domain_summary <- aggregate(
  cbind(
    technical_maturity,
    governance_maturity,
    system_maturity,
    systemic_risk,
    review_required
  ) ~ domain,
  data = systems,
  FUN = mean
)

risk_tier_summary <- aggregate(
  cbind(
    technical_maturity,
    governance_maturity,
    system_maturity,
    systemic_risk,
    review_required
  ) ~ risk_tier,
  data = systems,
  FUN = mean
)

governance_summary <- data.frame(
  systems_reviewed = nrow(systems),
  review_required = sum(systems$review_required),
  high_stakes_systems = sum(systems$high_stakes),
  mean_system_maturity = mean(systems$system_maturity),
  mean_systemic_risk = mean(systems$systemic_risk),
  low_monitoring_systems = sum(systems$monitoring_coverage < 0.40),
  low_governance_systems = sum(systems$governance_readiness < 0.45)
)

write.csv(systems, file.path(output_dir, "r_ai_system_lifecycle_inventory.csv"), row.names = FALSE)
write.csv(domain_summary, file.path(output_dir, "r_domain_maturity_summary.csv"), row.names = FALSE)
write.csv(risk_tier_summary, file.path(output_dir, "r_risk_tier_maturity_summary.csv"), row.names = FALSE)
write.csv(governance_summary, file.path(output_dir, "r_ai_systems_governance_summary.csv"), row.names = FALSE)

print("Domain-level AI systems maturity summary")
print(domain_summary)

print("Risk-tier AI systems maturity summary")
print(risk_tier_summary)

print("Governance summary")
print(governance_summary)
