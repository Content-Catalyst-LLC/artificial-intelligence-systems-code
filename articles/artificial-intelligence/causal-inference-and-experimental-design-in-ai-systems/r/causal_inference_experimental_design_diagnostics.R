# Causal Inference and Experimental Design in AI Systems Diagnostics
#
# This educational workflow simulates:
# - randomized assignment
# - observational confounding
# - treatment-effect estimation
# - balance diagnostics

set.seed(42)

n <- 5000

prior_activity <- rnorm(n, mean = 0, sd = 1)
domain_expertise <- rnorm(n, mean = 0, sd = 1)

true_tau <- 0.08 +
  0.04 * (prior_activity > 0) +
  0.03 * (domain_expertise > 0)

y0 <- 0.30 +
  0.08 * prior_activity +
  0.04 * domain_expertise +
  rnorm(n, mean = 0, sd = 0.05)

y1 <- y0 + true_tau

randomized_treatment <- rbinom(n, size = 1, prob = 0.5)

randomized_outcome <- ifelse(
  randomized_treatment == 1,
  y1,
  y0
)

propensity <- 1 / (1 + exp(-(-0.2 + 1.2 * prior_activity)))
observed_treatment <- rbinom(n, size = 1, prob = propensity)

observed_outcome <- ifelse(
  observed_treatment == 1,
  y1,
  y0
)

causal_data <- data.frame(
  prior_activity = prior_activity,
  domain_expertise = domain_expertise,
  true_tau = true_tau,
  randomized_treatment = randomized_treatment,
  randomized_outcome = randomized_outcome,
  observed_treatment = observed_treatment,
  observed_outcome = observed_outcome,
  propensity = propensity
)

true_ate <- mean(causal_data$true_tau)

randomized_estimate <-
  mean(causal_data$randomized_outcome[causal_data$randomized_treatment == 1]) -
  mean(causal_data$randomized_outcome[causal_data$randomized_treatment == 0])

naive_observational_estimate <-
  mean(causal_data$observed_outcome[causal_data$observed_treatment == 1]) -
  mean(causal_data$observed_outcome[causal_data$observed_treatment == 0])

ipw_weights <-
  causal_data$observed_treatment / causal_data$propensity +
  (1 - causal_data$observed_treatment) / (1 - causal_data$propensity)

treated_weighted_mean <- weighted.mean(
  causal_data$observed_outcome[causal_data$observed_treatment == 1],
  ipw_weights[causal_data$observed_treatment == 1]
)

control_weighted_mean <- weighted.mean(
  causal_data$observed_outcome[causal_data$observed_treatment == 0],
  ipw_weights[causal_data$observed_treatment == 0]
)

ipw_estimate <- treated_weighted_mean - control_weighted_mean

balance_table <- aggregate(
  cbind(prior_activity, domain_expertise, propensity) ~ observed_treatment,
  data = causal_data,
  FUN = mean
)

summary_table <- data.frame(
  estimate = c(
    "true_ate",
    "randomized_estimate",
    "naive_observational_estimate",
    "ipw_estimate"
  ),
  value = c(
    true_ate,
    randomized_estimate,
    naive_observational_estimate,
    ipw_estimate
  )
)

dir.create("../outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(causal_data, "../outputs/r_causal_inference_synthetic_data.csv", row.names = FALSE)
write.csv(summary_table, "../outputs/r_causal_inference_estimates.csv", row.names = FALSE)
write.csv(balance_table, "../outputs/r_causal_inference_balance_table.csv", row.names = FALSE)

print(summary_table)
print(balance_table)
