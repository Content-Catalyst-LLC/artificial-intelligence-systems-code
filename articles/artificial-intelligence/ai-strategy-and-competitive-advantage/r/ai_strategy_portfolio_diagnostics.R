# AI Strategy and Competitive Advantage Diagnostics
#
# This educational workflow simulates:
# - AI portfolio scoring
# - defensibility diagnostics
# - platform-dependence penalty
# - value-capture estimates
# - priority bands

initiatives <- data.frame(
  initiative = c(
    "customer_support_copilot",
    "proprietary_workflow_intelligence",
    "generic_marketing_generation",
    "regulated_decision_support",
    "internal_knowledge_agent"
  ),
  business_value = c(0.75, 0.70, 0.55, 0.82, 0.68),
  defensibility = c(0.35, 0.85, 0.20, 0.78, 0.70),
  data_readiness = c(0.70, 0.75, 0.65, 0.62, 0.82),
  workflow_fit = c(0.80, 0.78, 0.68, 0.70, 0.76),
  governance_maturity = c(0.65, 0.72, 0.55, 0.88, 0.74),
  platform_dependence = c(0.70, 0.35, 0.60, 0.45, 0.50),
  value_capture = c(0.45, 0.80, 0.35, 0.76, 0.68)
)

initiatives$capability_score <-
  0.25 * initiatives$business_value +
  0.20 * initiatives$data_readiness +
  0.20 * initiatives$workflow_fit +
  0.20 * initiatives$governance_maturity +
  0.15 * initiatives$defensibility

initiatives$strategic_advantage_score <-
  initiatives$capability_score *
  initiatives$defensibility *
  initiatives$value_capture *
  (1 - 0.40 * initiatives$platform_dependence)

initiatives$priority_band <- ifelse(
  initiatives$strategic_advantage_score < 0.10,
  "low",
  ifelse(
    initiatives$strategic_advantage_score < 0.25,
    "medium",
    "high"
  )
)

summary_table <- aggregate(
  cbind(
    business_value,
    defensibility,
    data_readiness,
    workflow_fit,
    governance_maturity,
    platform_dependence,
    value_capture,
    strategic_advantage_score
  ) ~ priority_band,
  data = initiatives,
  FUN = mean
)

dir.create("../outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(initiatives, "../outputs/r_ai_strategy_portfolio_scores.csv", row.names = FALSE)
write.csv(summary_table, "../outputs/r_ai_strategy_priority_summary.csv", row.names = FALSE)

print(initiatives[order(-initiatives$strategic_advantage_score), ])
print(summary_table)
