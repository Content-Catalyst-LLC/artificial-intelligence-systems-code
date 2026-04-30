# Human-AI Interaction and Interface Design Diagnostics

set.seed(42)

n <- 1800

interaction_data <- data.frame(
  case_id = paste0("HIAI-", sprintf("%04d", 1:n)),
  model_confidence = rbeta(n, 5, 2),
  explanation_quality = rbeta(n, 4, 3),
  uncertainty_clarity = rbeta(n, 3.5, 3),
  user_expertise = sample(c("novice", "intermediate", "expert"), n, replace = TRUE, prob = c(0.30, 0.45, 0.25)),
  time_pressure = sample(c("low", "medium", "high"), n, replace = TRUE, prob = c(0.35, 0.40, 0.25)),
  risk_level = sample(c("low", "medium", "high"), n, replace = TRUE, prob = c(0.45, 0.35, 0.20))
)

correct_probability <- pmin(pmax(0.20 + 0.75 * interaction_data$model_confidence, 0), 1)
interaction_data$model_correct <- rbinom(n, size = 1, prob = correct_probability)

expertise_adjustment <- ifelse(interaction_data$user_expertise == "novice", 0.10,
  ifelse(interaction_data$user_expertise == "intermediate", 0.03, -0.04)
)

pressure_adjustment <- ifelse(interaction_data$time_pressure == "low", -0.04,
  ifelse(interaction_data$time_pressure == "medium", 0.03, 0.12)
)

risk_adjustment <- ifelse(interaction_data$risk_level == "low", 0.06,
  ifelse(interaction_data$risk_level == "medium", 0.00, -0.10)
)

acceptance_probability <- 0.10 +
  0.48 * interaction_data$model_confidence +
  0.16 * interaction_data$explanation_quality +
  0.12 * interaction_data$uncertainty_clarity +
  expertise_adjustment +
  pressure_adjustment +
  risk_adjustment

acceptance_probability <- pmin(pmax(acceptance_probability, 0.02), 0.98)

interaction_data$user_accepted_ai <- rbinom(n, size = 1, prob = acceptance_probability)

escalation_probability <- 0.05 +
  0.20 * (interaction_data$risk_level == "high") +
  0.15 * (interaction_data$uncertainty_clarity < 0.40) +
  0.10 * (interaction_data$explanation_quality < 0.40)

escalation_probability <- pmin(pmax(escalation_probability, 0.01), 0.80)

interaction_data$user_escalated <- rbinom(n, size = 1, prob = escalation_probability)

interaction_data$overreliance <- interaction_data$user_accepted_ai == 1 & interaction_data$model_correct == 0
interaction_data$underreliance <- interaction_data$user_accepted_ai == 0 & interaction_data$model_correct == 1
interaction_data$reliance_gap <- abs(interaction_data$user_accepted_ai - interaction_data$model_correct)

summary_table <- aggregate(
  cbind(model_confidence, explanation_quality, uncertainty_clarity, model_correct, user_accepted_ai, user_escalated, overreliance, underreliance, reliance_gap) ~
    user_expertise + risk_level + time_pressure,
  data = interaction_data,
  FUN = mean
)

count_table <- aggregate(
  case_id ~ user_expertise + risk_level + time_pressure,
  data = interaction_data,
  FUN = length
)

names(count_table)[4] <- "cases"

summary_table <- merge(
  summary_table,
  count_table,
  by = c("user_expertise", "risk_level", "time_pressure")
)

dir.create("../outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(interaction_data, "../outputs/r_human_ai_interaction_synthetic_dataset.csv", row.names = FALSE)
write.csv(summary_table, "../outputs/r_human_ai_interaction_diagnostics.csv", row.names = FALSE)

print(summary_table)
