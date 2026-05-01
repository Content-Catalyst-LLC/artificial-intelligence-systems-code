# AI Systems in Organizations and Institutions Diagnostics
#
# This educational workflow simulates:
# - organizational AI readiness scoring
# - decision risk scoring
# - governance gap analysis
# - institutional oversight classification

use_cases <- data.frame(
  use_case = c(
    "customer_support_routing",
    "employee_performance_review",
    "clinical_triage_support",
    "procurement_anomaly_detection",
    "public_benefits_eligibility",
    "infrastructure_emergency_response"
  ),
  data_quality = c(0.86, 0.62, 0.78, 0.82, 0.66, 0.74),
  infrastructure = c(0.82, 0.70, 0.76, 0.84, 0.68, 0.80),
  staff_ai_literacy = c(0.74, 0.58, 0.72, 0.76, 0.60, 0.70),
  governance_maturity = c(0.72, 0.50, 0.74, 0.78, 0.55, 0.82),
  workflow_fit = c(0.88, 0.44, 0.70, 0.86, 0.52, 0.68),
  trust = c(0.78, 0.42, 0.66, 0.80, 0.48, 0.70),
  harm_potential = c(0.20, 0.74, 0.86, 0.40, 0.88, 0.94),
  rights_impact = c(0.18, 0.82, 0.72, 0.24, 0.92, 0.70),
  irreversibility = c(0.14, 0.68, 0.78, 0.32, 0.75, 0.90),
  opacity = c(0.40, 0.66, 0.58, 0.50, 0.72, 0.52)
)

use_cases$ai_readiness <-
  0.20 * use_cases$data_quality +
  0.16 * use_cases$infrastructure +
  0.16 * use_cases$staff_ai_literacy +
  0.22 * use_cases$governance_maturity +
  0.16 * use_cases$workflow_fit +
  0.10 * use_cases$trust

use_cases$decision_risk <-
  0.40 * use_cases$harm_potential +
  0.30 * use_cases$rights_impact +
  0.20 * use_cases$irreversibility +
  0.10 * use_cases$opacity

use_cases$recommended_mode <- ifelse(
  use_cases$decision_risk >= 0.70,
  "human_led_with_ai_support_and_strong_review",
  ifelse(
    use_cases$decision_risk >= 0.40,
    "human_in_the_loop",
    ifelse(
      use_cases$ai_readiness >= 0.70,
      "monitored_automation",
      "ai_decision_support_only"
    )
  )
)

use_cases$governance_gap <-
  use_cases$decision_risk - use_cases$governance_maturity

use_cases$requires_governance_action <-
  use_cases$governance_gap > 0.15

governance_summary <- data.frame(
  metric = c(
    "mean_ai_readiness",
    "mean_decision_risk",
    "share_requiring_governance_action",
    "share_high_risk_decisions"
  ),
  value = c(
    mean(use_cases$ai_readiness),
    mean(use_cases$decision_risk),
    mean(use_cases$requires_governance_action),
    mean(use_cases$decision_risk >= 0.70)
  )
)

dir.create("../outputs", recursive = TRUE, showWarnings = FALSE)

write.csv(use_cases, "../outputs/r_organizational_ai_use_cases.csv", row.names = FALSE)
write.csv(governance_summary, "../outputs/r_organizational_ai_governance_summary.csv", row.names = FALSE)

print(use_cases[order(-use_cases$decision_risk), ])
print(governance_summary)
