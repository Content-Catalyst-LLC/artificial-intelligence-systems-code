# Generative AI and Synthetic Content Systems
# R workflow: synthetic content review and governance summary.

set.seed(42)

article_dir <- normalizePath(file.path(getwd(), "articles/artificial-intelligence/generative-ai-and-synthetic-content-systems"), mustWork = FALSE)

if (!dir.exists(article_dir)) {
  article_dir <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."), mustWork = FALSE)
}

output_dir <- file.path(article_dir, "outputs")

if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

n <- 180

records <- data.frame(
  artifact_id = paste0("G", sprintf("%04d", 1:n)),
  modality = sample(
    c("text", "image", "audio", "video", "code", "multimodal"),
    size = n,
    replace = TRUE,
    prob = c(0.36, 0.22, 0.10, 0.08, 0.14, 0.10)
  ),
  use_case = sample(
    c("drafting", "research", "marketing", "education", "design", "software"),
    size = n,
    replace = TRUE
  ),
  quality_score = runif(n, min = 0.45, max = 0.98),
  grounding_score = runif(n, min = 0.20, max = 0.95),
  prompt_adherence = runif(n, min = 0.40, max = 0.98),
  provenance_score = runif(n, min = 0.10, max = 1.00),
  sensitive_domain = sample(c(0, 1), size = n, replace = TRUE, prob = c(0.76, 0.24)),
  policy_risk = rbeta(n, shape1 = 2.0, shape2 = 6.0),
  human_review_completed = sample(c(0, 1), size = n, replace = TRUE, prob = c(0.32, 0.68)),
  content_credentials_attached = sample(c(0, 1), size = n, replace = TRUE, prob = c(0.55, 0.45))
)

records$reliability_score <- 0.28 * records$quality_score +
  0.28 * records$grounding_score +
  0.18 * records$prompt_adherence +
  0.18 * records$provenance_score +
  0.08 * records$content_credentials_attached

records$risk_score <- 0.38 * records$policy_risk +
  0.24 * (1 - records$grounding_score) +
  0.18 * (1 - records$provenance_score) +
  0.12 * records$sensitive_domain +
  0.08 * (1 - records$content_credentials_attached)

records$review_required <- records$risk_score > 0.45 |
  records$grounding_score < 0.50 |
  records$provenance_score < 0.45 |
  records$sensitive_domain == 1 |
  records$content_credentials_attached == 0

records$publication_ready <- records$reliability_score >= 0.70 &
  records$risk_score <= 0.40 &
  records$human_review_completed == 1 &
  records$content_credentials_attached == 1

modality_review <- aggregate(
  cbind(
    reliability_score,
    risk_score,
    review_required,
    publication_ready,
    provenance_score,
    content_credentials_attached
  ) ~ modality,
  data = records,
  FUN = mean
)

use_case_review <- aggregate(
  cbind(
    reliability_score,
    risk_score,
    review_required,
    publication_ready
  ) ~ use_case,
  data = records,
  FUN = mean
)

governance_summary <- data.frame(
  artifacts_reviewed = nrow(records),
  review_required = sum(records$review_required),
  publication_ready = sum(records$publication_ready),
  sensitive_domain_artifacts = sum(records$sensitive_domain),
  mean_reliability_score = mean(records$reliability_score),
  mean_risk_score = mean(records$risk_score),
  low_provenance_artifacts = sum(records$provenance_score < 0.45),
  low_grounding_artifacts = sum(records$grounding_score < 0.50),
  missing_content_credentials = sum(records$content_credentials_attached == 0)
)

write.csv(records, file.path(output_dir, "r_synthetic_content_records.csv"), row.names = FALSE)
write.csv(modality_review, file.path(output_dir, "r_modality_governance_review.csv"), row.names = FALSE)
write.csv(use_case_review, file.path(output_dir, "r_use_case_governance_review.csv"), row.names = FALSE)
write.csv(governance_summary, file.path(output_dir, "r_synthetic_content_governance_summary.csv"), row.names = FALSE)

print("Modality review")
print(modality_review)

print("Use-case review")
print(use_case_review)

print("Governance summary")
print(governance_summary)
