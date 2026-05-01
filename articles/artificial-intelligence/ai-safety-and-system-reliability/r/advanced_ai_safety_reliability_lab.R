# Advanced AI Safety and System Reliability Lab
#
# This R workflow expands the article's statistical analysis layer with
# drift review, calibration assessment, subgroup safety analysis, threshold
# sweeps, incident review, and reliability-style survival analysis.
#
# The workflow uses base R so it can run without additional package installation.

set.seed(42)

article_dir <- normalizePath(file.path(getwd(), "articles/artificial-intelligence/ai-safety-and-system-reliability"), mustWork = FALSE)

if (!dir.exists(article_dir)) {
  article_dir <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."), mustWork = FALSE)
}

output_dir <- file.path(article_dir, "outputs")

if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

sigmoid <- function(z) {
  1 / (1 + exp(-z))
}

simulate_inference_log <- function(
  n,
  seed,
  shift = 0,
  adversarial_rate = 0,
  missingness_rate = 0
) {
  set.seed(seed)

  region <- sample(
    c("north", "south", "east", "west"),
    size = n,
    replace = TRUE,
    prob = c(0.25, 0.25, 0.25, 0.25)
  )

  asset_age <- pmax(rnorm(n, mean = 10 + shift, sd = 3), 0)
  sensor_load <- pmin(pmax(rnorm(n, mean = 0.50 + 0.03 * shift, sd = 0.15), 0), 1)
  maintenance_gap <- pmax(rnorm(n, mean = 90 + 8 * shift, sd = 30), 0)

  region_effect <- ifelse(
    region == "south", 0.20,
    ifelse(region == "east", -0.10,
      ifelse(region == "west", 0.10, 0.00)
    )
  )

  adversarial_or_corrupted <- rbinom(n, size = 1, prob = adversarial_rate)
  sensor_load[adversarial_or_corrupted == 1] <-
    pmax(sensor_load[adversarial_or_corrupted == 1] - 0.25, 0)

  missing_sensor <- rbinom(n, size = 1, prob = missingness_rate)
  sensor_load_observed <- sensor_load
  sensor_load_observed[missing_sensor == 1] <- NA

  sensor_load_imputed <- sensor_load_observed
  sensor_load_imputed[is.na(sensor_load_imputed)] <- mean(sensor_load_observed, na.rm = TRUE)

  latent_risk <- -3.2 +
    0.12 * asset_age +
    2.5 * sensor_load +
    0.014 * maintenance_gap +
    region_effect +
    rnorm(n, mean = 0, sd = 0.35)

  true_probability <- sigmoid(latent_risk)

  predicted_probability <- sigmoid(
    -3.0 +
      0.11 * asset_age +
      2.25 * sensor_load_imputed +
      0.013 * maintenance_gap +
      rnorm(n, mean = 0, sd = 0.25)
  )

  uncertainty <- 0.08 +
    0.38 * exp(-((predicted_probability - 0.50)^2) / 0.035) +
    0.03 * abs(shift) +
    0.08 * missing_sensor +
    0.06 * adversarial_or_corrupted +
    rnorm(n, mean = 0, sd = 0.02)

  uncertainty <- pmin(pmax(uncertainty, 0), 1)
  observed_outcome <- rbinom(n, size = 1, prob = true_probability)

  data.frame(
    region = region,
    asset_age = asset_age,
    sensor_load = sensor_load_observed,
    sensor_load_imputed = sensor_load_imputed,
    maintenance_gap = maintenance_gap,
    predicted_probability = predicted_probability,
    uncertainty = uncertainty,
    observed_outcome = observed_outcome,
    missing_sensor = missing_sensor,
    adversarial_or_corrupted = adversarial_or_corrupted
  )
}

calculate_psi <- function(expected, actual, bins = 10) {
  expected <- expected[!is.na(expected)]
  actual <- actual[!is.na(actual)]

  breaks <- unique(quantile(expected, probs = seq(0, 1, length.out = bins + 1)))

  if (length(breaks) < 3) {
    return(0)
  }

  expected_cut <- cut(expected, breaks = breaks, include.lowest = TRUE)
  actual_cut <- cut(actual, breaks = breaks, include.lowest = TRUE)

  expected_share <- as.numeric(prop.table(table(expected_cut)))
  actual_share <- as.numeric(prop.table(table(actual_cut)))

  length_needed <- min(length(expected_share), length(actual_share))
  expected_share <- expected_share[seq_len(length_needed)]
  actual_share <- actual_share[seq_len(length_needed)]

  expected_share[expected_share == 0] <- 0.0001
  actual_share[actual_share == 0] <- 0.0001

  sum((actual_share - expected_share) * log(actual_share / expected_share))
}

score_deployment <- function(
  df,
  decision_threshold = 0.70,
  uncertainty_threshold = 0.30
) {
  df$recommended_action <- ifelse(
    df$predicted_probability >= decision_threshold,
    "flag",
    "do_not_flag"
  )

  df$review_required <- df$uncertainty > uncertainty_threshold

  df$missed_failure <- df$recommended_action == "do_not_flag" &
    df$observed_outcome == 1

  df$automated_high_confidence <- df$review_required == FALSE &
    df$recommended_action == "flag"

  df
}

make_drift_report <- function(baseline, deployment, features) {
  rows <- list()

  for (feature in features) {
    base_values <- baseline[[feature]]
    deploy_values <- deployment[[feature]]

    ks_result <- suppressWarnings(ks.test(
      base_values[!is.na(base_values)],
      deploy_values[!is.na(deploy_values)]
    ))

    psi <- calculate_psi(base_values, deploy_values)

    status <- ifelse(
      psi >= 0.25, "action",
      ifelse(psi >= 0.10, "warning", "normal")
    )

    rows[[length(rows) + 1]] <- data.frame(
      feature = feature,
      baseline_mean = mean(base_values, na.rm = TRUE),
      deployment_mean = mean(deploy_values, na.rm = TRUE),
      baseline_sd = sd(base_values, na.rm = TRUE),
      deployment_sd = sd(deploy_values, na.rm = TRUE),
      population_stability_index = psi,
      ks_statistic = as.numeric(ks_result$statistic),
      ks_p_value = as.numeric(ks_result$p.value),
      drift_status = status
    )
  }

  do.call(rbind, rows)
}

make_calibration_table <- function(df, bins = 10) {
  df$risk_band <- cut(
    df$predicted_probability,
    breaks = seq(0, 1, length.out = bins + 1),
    include.lowest = TRUE
  )

  predicted_mean <- aggregate(predicted_probability ~ risk_band, df, mean)
  observed_rate <- aggregate(observed_outcome ~ risk_band, df, mean)
  counts <- aggregate(observed_outcome ~ risk_band, df, length)

  table <- merge(predicted_mean, observed_rate, by = "risk_band")
  table <- merge(table, counts, by = "risk_band")

  names(table) <- c("risk_band", "predicted_mean", "observed_rate", "count")
  table$absolute_gap <- abs(table$predicted_mean - table$observed_rate)
  table$weighted_gap <- table$count / sum(table$count) * table$absolute_gap

  table
}

expected_calibration_error <- function(calibration_table) {
  sum(calibration_table$weighted_gap, na.rm = TRUE)
}

brier_score <- function(df) {
  mean((df$predicted_probability - df$observed_outcome)^2)
}

make_subgroup_report <- function(scored) {
  aggregate_values <- aggregate(
    cbind(
      observed_outcome,
      predicted_probability,
      uncertainty,
      review_required,
      missed_failure,
      adversarial_or_corrupted,
      missing_sensor
    ) ~ region,
    scored,
    mean
  )

  names(aggregate_values) <- c(
    "region",
    "event_rate",
    "mean_prediction",
    "mean_uncertainty",
    "review_rate",
    "missed_failure_rate",
    "corrupted_share",
    "missing_sensor_share"
  )

  counts <- aggregate(observed_outcome ~ region, scored, length)
  names(counts) <- c("region", "records")

  report <- merge(counts, aggregate_values, by = "region")
  report$calibration_gap <- report$mean_prediction - report$event_rate

  report
}

make_threshold_sweep <- function(deployment, uncertainty_threshold = 0.30) {
  thresholds <- seq(0.10, 0.90, by = 0.05)
  rows <- list()

  for (threshold in thresholds) {
    scored <- score_deployment(
      deployment,
      decision_threshold = threshold,
      uncertainty_threshold = uncertainty_threshold
    )

    rows[[length(rows) + 1]] <- data.frame(
      decision_threshold = threshold,
      flag_rate = mean(scored$recommended_action == "flag"),
      review_rate = mean(scored$review_required),
      missed_failure_rate = mean(scored$missed_failure),
      observed_event_rate = mean(scored$observed_outcome),
      mean_uncertainty = mean(scored$uncertainty)
    )
  }

  do.call(rbind, rows)
}

simulate_reliability_table <- function(seed = 303, n_systems = 1000, horizon = 180) {
  set.seed(seed)

  incident_times <- rweibull(n_systems, shape = 1.8, scale = 120)
  early_failure <- rbinom(n_systems, size = 1, prob = 0.05) == 1
  incident_times[early_failure] <- runif(sum(early_failure), min = 1, max = 20)

  days <- seq(1, horizon)

  reliability <- sapply(days, function(day) {
    mean(incident_times > day)
  })

  data.frame(
    day = days,
    reliability = reliability,
    cumulative_failure_probability = 1 - reliability
  )
}

baseline <- simulate_inference_log(
  n = 5000,
  seed = 101,
  shift = 0,
  adversarial_rate = 0,
  missingness_rate = 0.02
)

deployment <- simulate_inference_log(
  n = 5000,
  seed = 202,
  shift = 2,
  adversarial_rate = 0.04,
  missingness_rate = 0.08
)

scored <- score_deployment(deployment)

features <- c(
  "asset_age",
  "sensor_load_imputed",
  "maintenance_gap",
  "predicted_probability",
  "uncertainty"
)

drift_report <- make_drift_report(baseline, scored, features)
calibration <- make_calibration_table(scored)
subgroup <- make_subgroup_report(scored)
threshold_sweep <- make_threshold_sweep(scored)
reliability <- simulate_reliability_table()

dashboard <- data.frame(
  missed_failure_rate = mean(scored$missed_failure),
  expected_calibration_error = expected_calibration_error(calibration),
  brier_score = brier_score(scored),
  review_rate = mean(scored$review_required),
  corrupted_share = mean(scored$adversarial_or_corrupted),
  missing_sensor_share = mean(scored$missing_sensor),
  safety_threshold_violated = mean(scored$missed_failure) > 0.01
)

incident_review <- scored[scored$missed_failure == TRUE, ]
incident_review <- incident_review[order(-incident_review$uncertainty), ]

write.csv(baseline, file.path(output_dir, "advanced_r_baseline_log.csv"), row.names = FALSE)
write.csv(scored, file.path(output_dir, "advanced_r_deployment_scored.csv"), row.names = FALSE)
write.csv(dashboard, file.path(output_dir, "advanced_r_safety_dashboard.csv"), row.names = FALSE)
write.csv(drift_report, file.path(output_dir, "advanced_r_drift_report.csv"), row.names = FALSE)
write.csv(calibration, file.path(output_dir, "advanced_r_calibration_table.csv"), row.names = FALSE)
write.csv(subgroup, file.path(output_dir, "advanced_r_subgroup_safety_report.csv"), row.names = FALSE)
write.csv(threshold_sweep, file.path(output_dir, "advanced_r_threshold_sweep.csv"), row.names = FALSE)
write.csv(reliability, file.path(output_dir, "advanced_r_reliability_table.csv"), row.names = FALSE)
write.csv(head(incident_review, 250), file.path(output_dir, "advanced_r_incident_review.csv"), row.names = FALSE)

png(file.path(output_dir, "advanced_r_threshold_sweep.png"), width = 1000, height = 700)
plot(
  threshold_sweep$decision_threshold,
  threshold_sweep$missed_failure_rate,
  type = "b",
  xlab = "Decision threshold",
  ylab = "Rate",
  main = "AI safety threshold tradeoff review"
)
lines(threshold_sweep$decision_threshold, threshold_sweep$review_rate, type = "b")
lines(threshold_sweep$decision_threshold, threshold_sweep$flag_rate, type = "b")
legend(
  "topright",
  legend = c("Missed failure rate", "Review rate", "Flag rate"),
  lty = c(1, 1, 1),
  pch = c(1, 1, 1)
)
dev.off()

png(file.path(output_dir, "advanced_r_reliability_curve.png"), width = 1000, height = 700)
plot(
  reliability$day,
  reliability$reliability,
  type = "l",
  xlab = "Day",
  ylab = "Estimated reliability",
  main = "System reliability over time"
)
dev.off()

print("Advanced R AI safety and reliability workflow complete.")
print(dashboard)
