# Asset Management Lifecycle Cost and Reliability Diagnostics
#
# This educational workflow simulates:
# - infrastructure assets
# - condition scores
# - service consequence
# - maintenance strategy
# - expected lifecycle cost proxy
# - reliability risk summaries

set.seed(42)

n <- 300

asset_data <- data.frame(
  asset_class = sample(
    c("pump", "valve", "road_segment", "bridge_component", "substation_asset"),
    n,
    replace = TRUE,
    prob = c(0.20, 0.20, 0.25, 0.20, 0.15)
  ),
  age_years = sample(1:60, n, replace = TRUE),
  condition_score = runif(n, min = 0.15, max = 0.98),
  service_consequence = sample(1:5, n, replace = TRUE),
  environmental_exposure = runif(n, min = 0, max = 1)
)

linear_risk <- -3.0 +
  0.045 * asset_data$age_years +
  2.5 * (1 - asset_data$condition_score) +
  0.9 * asset_data$environmental_exposure

asset_data$failure_probability <- 1 / (1 + exp(-linear_risk))
asset_data$risk_score <- asset_data$failure_probability * asset_data$service_consequence

asset_data$maintenance_strategy <- ifelse(
  asset_data$risk_score >= 2.5, "urgent_review",
  ifelse(asset_data$risk_score >= 1.5, "planned_intervention",
  ifelse(asset_data$risk_score >= 0.75, "condition_based_maintenance", "monitor"))
)

strategy_cost <- ifelse(
  asset_data$maintenance_strategy == "monitor", 5000,
  ifelse(asset_data$maintenance_strategy == "condition_based_maintenance", 18000,
  ifelse(asset_data$maintenance_strategy == "planned_intervention", 50000, 90000))
)

expected_failure_cost <- asset_data$failure_probability *
  asset_data$service_consequence *
  100000

asset_data$expected_lifecycle_cost_proxy <- strategy_cost + expected_failure_cost

summary_table <- aggregate(
  cbind(risk_score, failure_probability, expected_lifecycle_cost_proxy) ~
    asset_class + maintenance_strategy,
  data = asset_data,
  FUN = mean
)

count_table <- aggregate(
  risk_score ~ asset_class + maintenance_strategy,
  data = asset_data,
  FUN = length
)

names(count_table)[3] <- "asset_count"

summary_table <- merge(
  summary_table,
  count_table,
  by = c("asset_class", "maintenance_strategy")
)

dir.create("../outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(asset_data, "../outputs/r_asset_lifecycle_dataset.csv", row.names = FALSE)
write.csv(summary_table, "../outputs/r_asset_lifecycle_reliability_summary.csv", row.names = FALSE)

print(summary_table)
