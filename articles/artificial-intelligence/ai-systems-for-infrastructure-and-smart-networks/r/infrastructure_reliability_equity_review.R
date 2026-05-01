# AI Systems for Infrastructure and Smart Networks
# R workflow: infrastructure reliability and equity review.

set.seed(42)

article_dir <- normalizePath(file.path(getwd(), "articles/artificial-intelligence/ai-systems-for-infrastructure-and-smart-networks"), mustWork = FALSE)

if (!dir.exists(article_dir)) {
  article_dir <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."), mustWork = FALSE)
}

output_dir <- file.path(article_dir, "outputs")

if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

n <- 100

assets <- data.frame(
  asset_id = paste0("A", sprintf("%03d", 1:n)),
  area_type = sample(
    c("central", "industrial", "residential", "historically_underinvested"),
    size = n,
    replace = TRUE,
    prob = c(0.25, 0.20, 0.35, 0.20)
  ),
  asset_age = pmax(rnorm(n, mean = 24, sd = 10), 1),
  sensor_health = runif(n, min = 0.60, max = 1.00),
  service_population = sample(250:6000, size = n, replace = TRUE),
  historical_failures = rpois(n, lambda = 1.4),
  pressure_drop = pmin(pmax(rnorm(n, mean = 0.18, sd = 0.07), 0), 1),
  network_centrality = runif(n, min = 0, max = 1),
  climate_exposure = runif(n, min = 0, max = 1)
)

assets$equity_priority <- ifelse(
  assets$area_type == "historically_underinvested",
  1,
  0
)

assets$data_quality_risk <- 1 - assets$sensor_health

logit <- -3.6 +
  0.045 * assets$asset_age +
  1.9 * assets$pressure_drop +
  0.24 * assets$historical_failures +
  1.1 * assets$network_centrality +
  0.7 * assets$data_quality_risk +
  0.6 * assets$climate_exposure

assets$failure_probability <- 1 / (1 + exp(-logit))

assets$criticality_score <- 0.32 * assets$failure_probability +
  0.22 * assets$network_centrality +
  0.16 * (assets$service_population / max(assets$service_population)) +
  0.10 * assets$data_quality_risk +
  0.10 * assets$equity_priority +
  0.10 * assets$climate_exposure

assets$review_required <- assets$failure_probability > 0.55 |
  assets$data_quality_risk > 0.25 |
  assets$equity_priority == 1 |
  assets$climate_exposure > 0.80

priority_table <- assets[order(-assets$criticality_score), ]

area_review <- aggregate(
  cbind(
    failure_probability,
    data_quality_risk,
    review_required,
    equity_priority,
    climate_exposure
  ) ~ area_type,
  data = assets,
  FUN = mean
)

names(area_review) <- c(
  "area_type",
  "mean_failure_probability",
  "mean_data_quality_risk",
  "review_rate",
  "equity_priority_rate",
  "mean_climate_exposure"
)

governance_summary <- data.frame(
  assets_reviewed = nrow(assets),
  mean_failure_probability = mean(assets$failure_probability),
  high_risk_assets = sum(assets$failure_probability > 0.55),
  human_review_required = sum(assets$review_required),
  equity_priority_assets = sum(assets$equity_priority),
  high_climate_exposure_assets = sum(assets$climate_exposure > 0.80),
  mean_data_quality_risk = mean(assets$data_quality_risk)
)

write.csv(priority_table, file.path(output_dir, "r_infrastructure_priority_table.csv"), row.names = FALSE)
write.csv(area_review, file.path(output_dir, "r_area_equity_review.csv"), row.names = FALSE)
write.csv(governance_summary, file.path(output_dir, "r_infrastructure_governance_summary.csv"), row.names = FALSE)

print("Top infrastructure assets for review")
print(head(priority_table, 10))

print("Area-level equity and reliability review")
print(area_review)

print("Governance summary")
print(governance_summary)
