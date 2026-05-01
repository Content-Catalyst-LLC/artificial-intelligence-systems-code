# Explainable AI and Model Interpretability
# R workflow for transparent baseline modeling and explanation audits.

set.seed(42)

article_dir <- normalizePath(file.path(getwd(), "articles/artificial-intelligence/explainable-ai-and-model-interpretability"), mustWork = FALSE)

if (!dir.exists(article_dir)) {
  article_dir <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."), mustWork = FALSE)
}

output_dir <- file.path(article_dir, "outputs")

if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

n <- 3000

asset_age <- pmax(rnorm(n, mean = 10, sd = 3), 0)
sensor_load <- pmin(pmax(rnorm(n, mean = 0.5, sd = 0.15), 0), 1)
maintenance_gap <- pmax(rnorm(n, mean = 90, sd = 30), 0)
weather_stress <- pmin(pmax(rnorm(n, mean = 0.4, sd = 0.2), 0), 1)
inspection_score <- pmin(pmax(rnorm(n, mean = 0.7, sd = 0.15), 0), 1)

logit <- -3.0 +
  0.10 * asset_age +
  2.2 * sensor_load +
  0.012 * maintenance_gap +
  1.3 * weather_stress -
  1.6 * inspection_score +
  rnorm(n, mean = 0, sd = 0.25)

probability <- 1 / (1 + exp(-logit))
outcome <- rbinom(n, size = 1, prob = probability)

data <- data.frame(
  asset_age = asset_age,
  sensor_load = sensor_load,
  maintenance_gap = maintenance_gap,
  weather_stress = weather_stress,
  inspection_score = inspection_score,
  outcome = outcome
)

model <- glm(
  outcome ~ asset_age + sensor_load + maintenance_gap + weather_stress + inspection_score,
  data = data,
  family = binomial()
)

model_summary <- summary(model)

case_index <- 10
case <- data[case_index, ]

coefficients <- coef(model)
feature_names <- names(coefficients)[names(coefficients) != "(Intercept)"]

contributions <- coefficients[feature_names] * as.numeric(case[feature_names])

local_explanation <- data.frame(
  feature = feature_names,
  value = as.numeric(case[feature_names]),
  coefficient = as.numeric(coefficients[feature_names]),
  contribution_to_logit = as.numeric(contributions)
)

local_explanation <- local_explanation[
  order(abs(local_explanation$contribution_to_logit), decreasing = TRUE),
]

predicted_probability <- predict(model, newdata = case, type = "response")

counterfactual <- case

for (step in 1:60) {
  cf_probability <- predict(model, newdata = counterfactual, type = "response")

  if (cf_probability < 0.50) {
    break
  }

  counterfactual$maintenance_gap <- max(counterfactual$maintenance_gap - 4, 0)
  counterfactual$sensor_load <- max(counterfactual$sensor_load - 0.015, 0)
  counterfactual$weather_stress <- max(counterfactual$weather_stress - 0.012, 0)
}

counterfactual_probability <- predict(model, newdata = counterfactual, type = "response")

counterfactual_summary <- data.frame(
  feature = feature_names,
  original_value = as.numeric(case[feature_names]),
  counterfactual_value = as.numeric(counterfactual[feature_names]),
  change = as.numeric(counterfactual[feature_names]) - as.numeric(case[feature_names])
)

audit_table <- data.frame(
  audit_item = c(
    "Model is intrinsically interpretable",
    "Feature coefficients are inspectable",
    "Local explanation generated",
    "Counterfactual generated",
    "Actionable variables used in counterfactual",
    "Explanation requires causal review"
  ),
  status = c(TRUE, TRUE, TRUE, TRUE, TRUE, TRUE)
)

write.csv(data, file.path(output_dir, "r_synthetic_explainability_data.csv"), row.names = FALSE)
write.csv(local_explanation, file.path(output_dir, "r_local_explanation.csv"), row.names = FALSE)
write.csv(counterfactual_summary, file.path(output_dir, "r_counterfactual_summary.csv"), row.names = FALSE)
write.csv(audit_table, file.path(output_dir, "r_explanation_audit_table.csv"), row.names = FALSE)

capture.output(model_summary, file = file.path(output_dir, "r_model_summary.txt"))

memo <- paste0(
  "# R Explanation Audit Memo\n\n",
  "Predicted probability: ", round(predicted_probability, 4), "\n",
  "Counterfactual probability: ", round(counterfactual_probability, 4), "\n\n",
  "The transparent logistic baseline provides inspectable coefficients, local contribution-style values, and a simple counterfactual recourse example.\n"
)

writeLines(memo, file.path(output_dir, "r_explanation_audit_memo.md"))

print(memo)
