# AI in Education, Knowledge Work, and Learning Systems
# R workflow: AI learning system evaluation summary.
#
# Educational systems workflow only.
# Does not make student-specific educational decisions.

set.seed(42)

article_dir <- normalizePath(file.path(getwd(), "articles/artificial-intelligence/ai-in-education-knowledge-work-and-learning-systems"), mustWork = FALSE)

if (!dir.exists(article_dir)) {
  article_dir <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."), mustWork = FALSE)
}

output_dir <- file.path(article_dir, "outputs")

if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

n <- 4000

course_type <- sample(
  c("writing", "mathematics", "science", "programming", "professional_learning"),
  size = n,
  replace = TRUE,
  prob = c(0.25, 0.20, 0.20, 0.20, 0.15)
)

access_context <- sample(
  c("high_access", "moderate_access", "limited_access"),
  size = n,
  replace = TRUE,
  prob = c(0.46, 0.38, 0.16)
)

language_context <- sample(
  c("dominant_instruction_language", "multilingual_or_language_support"),
  size = n,
  replace = TRUE,
  prob = c(0.78, 0.22)
)

accommodation_context <- sample(
  c("no_recorded_accommodation", "accessibility_support"),
  size = n,
  replace = TRUE,
  prob = c(0.86, 0.14)
)

clamp <- function(x, lower = 0, upper = 1) {
  pmin(pmax(x, lower), upper)
}

baseline_knowledge <- clamp(rnorm(n, mean = 0.52, sd = 0.17))
effort <- clamp(rnorm(n, mean = 0.62, sd = 0.18))
ai_usage_intensity <- rbeta(n, shape1 = 2.2, shape2 = 2.5)
teacher_integration_quality <- clamp(rnorm(n, mean = 0.68, sd = 0.16))

access_penalty <- ifelse(
  access_context == "high_access",
  0.00,
  ifelse(access_context == "moderate_access", -0.04, -0.12)
)

language_support_effect <- ifelse(language_context == "multilingual_or_language_support", 0.04, 0.0)
accessibility_effect <- ifelse(accommodation_context == "accessibility_support", 0.05, 0.0)

learning_support_effect <- 0.18 * ai_usage_intensity * teacher_integration_quality +
  0.16 * effort +
  language_support_effect +
  accessibility_effect +
  access_penalty

dependency_risk <- clamp(ai_usage_intensity * (1 - effort) * (1 - teacher_integration_quality + 0.25))

post_learning_score <- clamp(
  baseline_knowledge +
    learning_support_effect -
    0.10 * dependency_risk +
    rnorm(n, mean = 0, sd = 0.07)
)

assisted_performance <- clamp(
  post_learning_score +
    0.16 * ai_usage_intensity +
    rnorm(n, mean = 0, sd = 0.05)
)

independent_transfer <- clamp(
  post_learning_score +
    0.08 * effort -
    0.18 * dependency_risk +
    rnorm(n, mean = 0, sd = 0.06)
)

feedback_quality <- clamp(
  0.35 * teacher_integration_quality +
    0.25 * baseline_knowledge +
    0.25 * effort +
    0.15 * ai_usage_intensity +
    rnorm(n, mean = 0, sd = 0.08)
)

privacy_risk <- clamp(
  0.12 +
    0.25 * ai_usage_intensity +
    0.15 * as.numeric(course_type == "professional_learning") +
    0.10 * as.numeric(course_type == "writing") +
    rnorm(n, mean = 0, sd = 0.05)
)

assessment_substitution_risk <- clamp(
  0.40 * ai_usage_intensity +
    0.35 * (1 - effort) +
    0.20 * as.numeric(course_type %in% c("writing", "programming")) -
    0.20 * teacher_integration_quality +
    rnorm(n, mean = 0, sd = 0.05)
)

records <- data.frame(
  learner_record_id = paste0("LEARN-", sprintf("%05d", 1:n)),
  course_type = course_type,
  access_context = access_context,
  language_context = language_context,
  accommodation_context = accommodation_context,
  baseline_knowledge = baseline_knowledge,
  post_learning_score = post_learning_score,
  assisted_performance = assisted_performance,
  independent_transfer = independent_transfer,
  effort = effort,
  ai_usage_intensity = ai_usage_intensity,
  teacher_integration_quality = teacher_integration_quality,
  feedback_quality = feedback_quality,
  dependency_risk = dependency_risk,
  privacy_risk = privacy_risk,
  assessment_substitution_risk = assessment_substitution_risk
)

records$learning_gain <- records$post_learning_score - records$baseline_knowledge
records$assistance_gap <- records$assisted_performance - records$independent_transfer

records$learning_system_governance_risk <- clamp(
  0.24 * records$assessment_substitution_risk +
    0.22 * records$privacy_risk +
    0.20 * records$dependency_risk +
    0.16 * (1 - records$feedback_quality) +
    0.10 * as.numeric(records$assistance_gap > 0.18) +
    0.08 * as.numeric(records$teacher_integration_quality < 0.50)
)

records$human_review_recommended <- records$learning_system_governance_risk > 0.42 |
  records$assessment_substitution_risk > 0.55 |
  records$privacy_risk > 0.48 |
  records$assistance_gap > 0.24 |
  records$feedback_quality < 0.35

summarize_group <- function(data, group_name) {
  split_data <- split(data, data[[group_name]])

  rows <- lapply(names(split_data), function(value) {
    subset <- split_data[[value]]

    data.frame(
      group_type = group_name,
      group_value = value,
      records = nrow(subset),
      mean_learning_gain = mean(subset$learning_gain),
      mean_independent_transfer = mean(subset$independent_transfer),
      mean_assisted_performance = mean(subset$assisted_performance),
      mean_assistance_gap = mean(subset$assistance_gap),
      mean_feedback_quality = mean(subset$feedback_quality),
      mean_dependency_risk = mean(subset$dependency_risk),
      mean_privacy_risk = mean(subset$privacy_risk),
      mean_assessment_substitution_risk = mean(subset$assessment_substitution_risk),
      mean_governance_risk = mean(subset$learning_system_governance_risk),
      human_review_rate = mean(subset$human_review_recommended)
    )
  })

  do.call(rbind, rows)
}

group_summary <- rbind(
  summarize_group(records, "course_type"),
  summarize_group(records, "access_context"),
  summarize_group(records, "language_context"),
  summarize_group(records, "accommodation_context")
)

overall_learning_gain <- mean(records$learning_gain)
overall_transfer <- mean(records$independent_transfer)
overall_risk <- mean(records$learning_system_governance_risk)

group_summary$learning_gain_gap_from_overall <- group_summary$mean_learning_gain - overall_learning_gain
group_summary$transfer_gap_from_overall <- group_summary$mean_independent_transfer - overall_transfer
group_summary$risk_gap_from_overall <- group_summary$mean_governance_risk - overall_risk

group_summary$review_required <- group_summary$records < 100 |
  abs(group_summary$learning_gain_gap_from_overall) > 0.06 |
  abs(group_summary$transfer_gap_from_overall) > 0.06 |
  group_summary$risk_gap_from_overall > 0.08 |
  group_summary$mean_assistance_gap > 0.18 |
  group_summary$human_review_rate > 0.35

governance_summary <- data.frame(
  records_reviewed = nrow(records),
  mean_learning_gain = mean(records$learning_gain),
  mean_independent_transfer = mean(records$independent_transfer),
  mean_assisted_performance = mean(records$assisted_performance),
  mean_assistance_gap = mean(records$assistance_gap),
  mean_feedback_quality = mean(records$feedback_quality),
  mean_dependency_risk = mean(records$dependency_risk),
  mean_privacy_risk = mean(records$privacy_risk),
  mean_assessment_substitution_risk = mean(records$assessment_substitution_risk),
  mean_governance_risk = mean(records$learning_system_governance_risk),
  human_review_recommended_records = sum(records$human_review_recommended),
  groups_requiring_review = sum(group_summary$review_required)
)

write.csv(records, file.path(output_dir, "r_learning_ai_records.csv"), row.names = FALSE)
write.csv(group_summary, file.path(output_dir, "r_learning_ai_group_review.csv"), row.names = FALSE)
write.csv(governance_summary, file.path(output_dir, "r_learning_ai_governance_summary.csv"), row.names = FALSE)

print("Group summary")
print(group_summary)

print("Governance summary")
print(governance_summary)
