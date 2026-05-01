# The Future of Artificial Intelligence Systems Diagnostics
#
# This educational workflow simulates:
# - AI futures scenario scoring
# - governance-readiness analysis
# - infrastructure and legitimacy constraints
# - systemic-risk summaries

scenarios <- data.frame(
  scenario = c(
    "centralized_frontier_dominance",
    "distributed_intelligence_networks",
    "hybrid_public_private_infrastructure",
    "regulated_high_risk_ai",
    "governance_lag_and_systemic_fragility"
  ),
  capability = c(0.95, 0.74, 0.86, 0.80, 0.88),
  infrastructure = c(0.88, 0.70, 0.82, 0.75, 0.66),
  governance = c(0.55, 0.68, 0.84, 0.90, 0.35),
  resilience = c(0.52, 0.78, 0.80, 0.74, 0.40),
  legitimacy = c(0.50, 0.72, 0.82, 0.86, 0.34),
  systemic_risk = c(0.78, 0.46, 0.38, 0.42, 0.90)
)

scenarios$scenario_score <-
  0.22 * scenarios$capability +
  0.18 * scenarios$infrastructure +
  0.22 * scenarios$governance +
  0.18 * scenarios$resilience +
  0.15 * scenarios$legitimacy -
  0.20 * scenarios$systemic_risk

scenarios$governance_gap <- scenarios$capability - scenarios$governance

scenarios$risk_warning <- scenarios$governance_gap > 0.20 |
  scenarios$systemic_risk > 0.70

ranked_scenarios <- scenarios[order(-scenarios$scenario_score), ]

constraint_summary <- data.frame(
  metric = c(
    "mean_capability",
    "mean_governance",
    "mean_resilience",
    "mean_systemic_risk",
    "share_with_risk_warning"
  ),
  value = c(
    mean(scenarios$capability),
    mean(scenarios$governance),
    mean(scenarios$resilience),
    mean(scenarios$systemic_risk),
    mean(scenarios$risk_warning)
  )
)

systems <- data.frame(
  system = c(
    "centralized_frontier",
    "compute_optimal_specialist",
    "distributed_edge_network",
    "hybrid_governed_platform",
    "undergoverned_agentic_stack"
  ),
  capability = c(0.95, 0.83, 0.74, 0.88, 0.91),
  efficiency = c(0.42, 0.86, 0.78, 0.74, 0.45),
  governance_capacity = c(0.62, 0.78, 0.70, 0.90, 0.38),
  trust = c(0.58, 0.80, 0.72, 0.86, 0.42),
  systemic_risk = c(0.72, 0.38, 0.44, 0.32, 0.86),
  cost = c(0.90, 0.48, 0.55, 0.62, 0.76)
)

systems$system_fitness <-
  0.30 * systems$capability +
  0.18 * systems$efficiency +
  0.22 * systems$governance_capacity +
  0.18 * systems$trust -
  0.20 * systems$systemic_risk -
  0.12 * systems$cost

systems$responsible_scaling_gap <- systems$capability - systems$governance_capacity
systems$governance_warning <- systems$responsible_scaling_gap > 0.15

ranked_systems <- systems[order(-systems$system_fitness), ]

dir.create("../outputs", recursive = TRUE, showWarnings = FALSE)

write.csv(scenarios, "../outputs/r_ai_future_scenarios.csv", row.names = FALSE)
write.csv(ranked_scenarios, "../outputs/r_ranked_ai_future_scenarios.csv", row.names = FALSE)
write.csv(constraint_summary, "../outputs/r_ai_future_constraint_summary.csv", row.names = FALSE)
write.csv(systems, "../outputs/r_ai_future_systems.csv", row.names = FALSE)
write.csv(ranked_systems, "../outputs/r_ranked_ai_future_systems.csv", row.names = FALSE)

print(ranked_scenarios)
print(constraint_summary)
print(ranked_systems)
