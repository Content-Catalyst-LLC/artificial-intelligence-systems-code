# Trust, Interpretability, and User-Centered AI Diagnostics
#
# This educational workflow simulates:
# - model confidence
# - explanation quality
# - user expertise
# - user reliance
# - overreliance and underreliance diagnostics

set.seed(42)

n <- 1500

ai_use <- data.frame(
  case_id = paste0("C-", sprintf("%04d", 1:n)),
  model_confidence = rbeta(n, 5, 2),
  explanation_quality = rbeta(n, 4, 3),
  user_expertise = sample(
    c("novice", "intermediate", "expert"),
    n,
    replace = TRUE,
    prob = c(0.30, 0.45, 0.25)
  ),
  risk_level = sample(
    c("low", "medium", "high"),
    n,
    replace = TRUE,
    prob = c(0.45, 0.35, 0.20)
  )
)

correct_probability <- pmin(pmax(0.20 + 0.75 * ai_use$model_confidence, 0), 1)
ai_use$model_correct <- rbinom(n, size = 1, prob = correct_probability)

expertise_adjustment <- ifelse(
  ai_use$user_expertise == "novice", 0.12,
  ifelse(ai_use$user_expertise == "intermediate", 0.04, -0.04)
)

risk_adjustment <- ifelse(
  ai_use$risk_level == "low", 0.08,
  ifelse(ai_use$risk_level == "medium", 0.00, -0.10)
)

reliance_probability <- 0.15 +
  0.50 * ai_use$model_confidence +
  0.20 * ai_use$explanation_quality +
  expertise_adjustment +
  risk_adjustment

reliance_probability <- pmin(pmax(reliance_probability, 0.02), 0.98)

ai_use$user_relied_on_ai <- rbinom(n, size = 1, prob = reliance_probability)

ai_use$overreliance <- ai_use$user_relied_on_ai == 1 & ai_use$model_correct == 0
ai_use$underreliance <- ai_use$user_relied_on_ai == 0 & ai_use$model_correct == 1
ai_use$reliance_gap <- abs(ai_use$user_relied_on_ai - ai_use$model_correct)

summary_table <- aggregate(
  cbind(model_confidence, explanation_quality, model_correct, user_relied_on_ai, overreliance, underreliance, reliance_gap) ~
    user_expertise + risk_level,
  data = ai_use,
  FUN = mean
)

count_table <- aggregate(
  case_id ~ user_expertise + risk_level,
  data = ai_use,
  FUN = length
)

names(count_table)[3] <- "cases"

summary_table <- merge(
  summary_table,
  count_table,
  by = c("user_expertise", "risk_level")
)

dir.create("../outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(ai_use, "../outputs/r_user_centered_ai_synthetic_dataset.csv", row.names = FALSE)
write.csv(summary_table, "../outputs/r_user_reliance_diagnostics.csv", row.names = FALSE)

print(summary_table)
