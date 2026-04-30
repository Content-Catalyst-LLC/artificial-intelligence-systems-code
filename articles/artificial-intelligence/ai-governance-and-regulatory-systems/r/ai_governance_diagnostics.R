# AI Governance Diagnostics
#
# This educational workflow simulates residual risk across AI systems
# by risk tier and control maturity.

set.seed(42)

n <- 300

ai_inventory <- data.frame(
  risk_tier = sample(
    c("minimal", "limited", "high"),
    n,
    replace = TRUE,
    prob = c(0.35, 0.40, 0.25)
  ),
  domain = sample(
    c("customer_service", "employment", "healthcare", "finance", "public_sector", "infrastructure"),
    n,
    replace = TRUE
  )
)

tier_severity <- ifelse(
  ai_inventory$risk_tier == "minimal", 1.5,
  ifelse(ai_inventory$risk_tier == "limited", 3.0, 5.0)
)

ai_inventory$likelihood <- runif(n, min = 1, max = 5)
ai_inventory$severity <- pmin(tier_severity + runif(n, min = -0.5, max = 0.5), 5)
ai_inventory$control_maturity <- runif(n, min = 0.20, max = 0.95)

ai_inventory$inherent_risk <- ai_inventory$likelihood * ai_inventory$severity
ai_inventory$residual_risk <- ai_inventory$inherent_risk * (1 - ai_inventory$control_maturity)

summary_table <- aggregate(
  residual_risk ~ risk_tier + domain,
  data = ai_inventory,
  FUN = mean
)

names(summary_table)[3] <- "mean_residual_risk"

maturity_table <- aggregate(
  control_maturity ~ risk_tier,
  data = ai_inventory,
  FUN = mean
)

names(maturity_table)[2] <- "mean_control_maturity"

dir.create("../outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(summary_table, "../outputs/r_ai_governance_residual_risk.csv", row.names = FALSE)
write.csv(maturity_table, "../outputs/r_ai_governance_control_maturity.csv", row.names = FALSE)

print(summary_table)
print(maturity_table)
