# Multimodal AI: Language, Vision, Audio, and Action
# R workflow: multimodal evaluation summary and risk review.

set.seed(42)

article_dir <- normalizePath(file.path(getwd(), "articles/artificial-intelligence/multimodal-ai-language-vision-audio-and-action"), mustWork = FALSE)

if (!dir.exists(article_dir)) {
  article_dir <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."), mustWork = FALSE)
}

output_dir <- file.path(article_dir, "outputs")

if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

n <- 240

use_cases <- c(
  "visual_question_answering",
  "audio_event_understanding",
  "video_event_summary",
  "document_image_analysis",
  "sensor_fusion_monitoring",
  "robotic_action_planning",
  "multimodal_retrieval"
)

records <- data.frame(
  eval_id = paste0("MM-EVAL-", sprintf("%03d", 1:n)),
  use_case = sample(use_cases, size = n, replace = TRUE),
  has_text = rbinom(n, size = 1, prob = 0.90),
  has_vision = rbinom(n, size = 1, prob = 0.75),
  has_audio = rbinom(n, size = 1, prob = 0.45),
  has_video = rbinom(n, size = 1, prob = 0.35),
  has_sensor = rbinom(n, size = 1, prob = 0.40),
  cross_modal_alignment = runif(n, min = 0.35, max = 0.98),
  grounding_score = runif(n, min = 0.35, max = 0.98),
  robustness_score = runif(n, min = 0.40, max = 0.98),
  conflict_detection_score = runif(n, min = 0.30, max = 0.95),
  privacy_control_score = runif(n, min = 0.50, max = 1.00),
  accessibility_score = runif(n, min = 0.45, max = 1.00),
  human_review_score = runif(n, min = 0.45, max = 1.00),
  latency_seconds = rgamma(n, shape = 2.4, scale = 1.2),
  compute_cost_index = runif(n, min = 0.10, max = 0.95)
)

records$has_action <- ifelse(records$use_case == "robotic_action_planning", 1, 0)
records$action_safety_score <- ifelse(
  records$has_action == 1,
  runif(n, min = 0.50, max = 1.00),
  runif(n, min = 0.70, max = 1.00)
)

records$modality_count <- records$has_text +
  records$has_vision +
  records$has_audio +
  records$has_video +
  records$has_sensor +
  records$has_action

records$modality_coverage_score <- pmin(records$modality_count / 4, 1)
records$modality_missing_risk <- pmax(0, 0.50 - (records$modality_count / 6))
records$modality_conflict_risk <- rbeta(n, shape1 = 2.0, shape2 = 5.5)

records$multimodal_capability_score <- 0.20 * records$modality_coverage_score +
  0.20 * records$cross_modal_alignment +
  0.20 * records$grounding_score +
  0.15 * records$robustness_score +
  0.15 * records$conflict_detection_score +
  0.10 * records$accessibility_score

records$safety_and_governance_score <- 0.25 * records$privacy_control_score +
  0.25 * records$action_safety_score +
  0.20 * records$human_review_score +
  0.15 * records$conflict_detection_score +
  0.15 * records$robustness_score

records$multimodal_system_risk <- 0.22 * (1 - records$multimodal_capability_score) +
  0.22 * (1 - records$safety_and_governance_score) +
  0.16 * records$modality_missing_risk +
  0.16 * records$modality_conflict_risk +
  0.12 * records$compute_cost_index +
  0.12 * pmin(records$latency_seconds / 10, 1)

records$review_required <- records$multimodal_system_risk > 0.42 |
  records$cross_modal_alignment < 0.60 |
  records$grounding_score < 0.60 |
  records$conflict_detection_score < 0.55 |
  records$privacy_control_score < 0.70 |
  records$accessibility_score < 0.65 |
  (records$has_action == 1 & records$action_safety_score < 0.80)

use_case_summary <- aggregate(
  cbind(
    modality_count,
    cross_modal_alignment,
    grounding_score,
    robustness_score,
    multimodal_capability_score,
    safety_and_governance_score,
    multimodal_system_risk,
    review_required
  ) ~ use_case,
  data = records,
  FUN = mean
)

governance_summary <- data.frame(
  evaluations_reviewed = nrow(records),
  review_required = sum(records$review_required),
  action_cases = sum(records$has_action),
  low_grounding_cases = sum(records$grounding_score < 0.60),
  low_alignment_cases = sum(records$cross_modal_alignment < 0.60),
  mean_capability_score = mean(records$multimodal_capability_score),
  mean_safety_governance_score = mean(records$safety_and_governance_score),
  mean_multimodal_system_risk = mean(records$multimodal_system_risk)
)

write.csv(records, file.path(output_dir, "r_multimodal_evaluation_records.csv"), row.names = FALSE)
write.csv(use_case_summary, file.path(output_dir, "r_multimodal_use_case_summary.csv"), row.names = FALSE)
write.csv(governance_summary, file.path(output_dir, "r_multimodal_governance_summary.csv"), row.names = FALSE)

print("Use-case summary")
print(use_case_summary)

print("Governance summary")
print(governance_summary)
