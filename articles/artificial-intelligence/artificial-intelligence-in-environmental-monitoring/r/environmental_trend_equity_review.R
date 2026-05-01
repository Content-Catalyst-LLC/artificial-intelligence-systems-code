# Artificial Intelligence in Environmental Monitoring
# R workflow: environmental trend and equity review.

set.seed(42)

article_dir <- normalizePath(file.path(getwd(), "articles/artificial-intelligence/artificial-intelligence-in-environmental-monitoring"), mustWork = FALSE)

if (!dir.exists(article_dir)) {
  article_dir <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."), mustWork = FALSE)
}

output_dir <- file.path(article_dir, "outputs")

if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

n <- 150

monitoring <- data.frame(
  zone_id = paste0("Z", sprintf("%03d", 1:n)),
  region_type = sample(
    c("urban", "industrial", "agricultural", "forest", "coastal"),
    size = n,
    replace = TRUE,
    prob = c(0.28, 0.16, 0.24, 0.20, 0.12)
  ),
  pm25 = pmax(rnorm(n, mean = 14, sd = 6), 1),
  ozone = pmax(rnorm(n, mean = 52, sd = 14), 5),
  water_turbidity = pmax(rnorm(n, mean = 8, sd = 4), 0),
  water_temperature = pmax(rnorm(n, mean = 18, sd = 5), 0),
  vegetation_index = pmin(pmax(rnorm(n, mean = 0.55, sd = 0.18), 0), 1),
  surface_temperature = rnorm(n, mean = 24, sd = 7),
  precipitation_anomaly = rnorm(n, mean = 0, sd = 1),
  sensor_health = runif(n, min = 0.65, max = 1.00),
  population_exposure = sample(100:25000, size = n, replace = TRUE),
  environmental_justice_priority = sample(c(0, 1), size = n, replace = TRUE, prob = c(0.72, 0.28))
)

monitoring$industrial_or_urban <- ifelse(
  monitoring$region_type %in% c("urban", "industrial"),
  1,
  0
)

monitoring$data_quality_risk <- 1 - monitoring$sensor_health

monitoring$air_pollution_index <- 0.55 * (monitoring$pm25 / max(monitoring$pm25)) +
  0.45 * (monitoring$ozone / max(monitoring$ozone))

monitoring$water_stress_index <- 0.60 * (monitoring$water_turbidity / max(monitoring$water_turbidity)) +
  0.40 * (monitoring$water_temperature / max(monitoring$water_temperature))

monitoring$vegetation_stress_index <- 1 - monitoring$vegetation_index

monitoring$climate_anomaly_index <- 0.50 * abs(monitoring$precipitation_anomaly) / max(abs(monitoring$precipitation_anomaly)) +
  0.50 * (monitoring$surface_temperature - min(monitoring$surface_temperature)) /
  (max(monitoring$surface_temperature) - min(monitoring$surface_temperature))

logit <- -2.8 +
  2.0 * monitoring$air_pollution_index +
  1.6 * monitoring$water_stress_index +
  1.4 * monitoring$vegetation_stress_index +
  1.2 * monitoring$climate_anomaly_index +
  0.6 * monitoring$industrial_or_urban +
  0.8 * monitoring$data_quality_risk

monitoring$environmental_stress_probability <- 1 / (1 + exp(-logit))

monitoring$anomaly_score <- (
  abs(monitoring$pm25 - mean(monitoring$pm25)) / sd(monitoring$pm25) +
    abs(monitoring$water_turbidity - mean(monitoring$water_turbidity)) / sd(monitoring$water_turbidity) +
    abs(monitoring$surface_temperature - mean(monitoring$surface_temperature)) / sd(monitoring$surface_temperature)
) / 3

monitoring$human_review_required <- monitoring$environmental_stress_probability > 0.60 |
  monitoring$anomaly_score > 1.25 |
  monitoring$data_quality_risk > 0.25 |
  monitoring$environmental_justice_priority == 1

monitoring$priority_score <- 0.35 * monitoring$environmental_stress_probability +
  0.20 * pmin(monitoring$anomaly_score, 2) / 2 +
  0.15 * monitoring$data_quality_risk +
  0.15 * (monitoring$population_exposure / max(monitoring$population_exposure)) +
  0.15 * monitoring$environmental_justice_priority

priority_table <- monitoring[order(-monitoring$priority_score), ]

region_review <- aggregate(
  cbind(
    environmental_stress_probability,
    anomaly_score,
    data_quality_risk,
    human_review_required,
    environmental_justice_priority
  ) ~ region_type,
  data = monitoring,
  FUN = mean
)

governance_summary <- data.frame(
  zones_reviewed = nrow(monitoring),
  mean_stress_probability = mean(monitoring$environmental_stress_probability),
  high_stress_zones = sum(monitoring$environmental_stress_probability > 0.60),
  human_review_required = sum(monitoring$human_review_required),
  environmental_justice_priority_zones = sum(monitoring$environmental_justice_priority),
  mean_data_quality_risk = mean(monitoring$data_quality_risk)
)

write.csv(priority_table, file.path(output_dir, "r_environmental_priority_table.csv"), row.names = FALSE)
write.csv(region_review, file.path(output_dir, "r_environmental_region_review.csv"), row.names = FALSE)
write.csv(governance_summary, file.path(output_dir, "r_environmental_governance_summary.csv"), row.names = FALSE)

print("Top environmental monitoring zones for review")
print(head(priority_table, 10))

print("Region-level environmental review")
print(region_review)

print("Governance summary")
print(governance_summary)
