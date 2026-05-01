# Retrieval-Augmented Generation and AI Knowledge Systems
# R workflow: RAG evaluation summary and source-support review.

set.seed(42)

article_dir <- normalizePath(file.path(getwd(), "articles/artificial-intelligence/retrieval-augmented-generation-and-ai-knowledge-systems"), mustWork = FALSE)

if (!dir.exists(article_dir)) {
  article_dir <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."), mustWork = FALSE)
}

output_dir <- file.path(article_dir, "outputs")

if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

n <- 240

query_types <- c(
  "direct_fact",
  "multi_hop_question",
  "policy_lookup",
  "technical_support",
  "research_synthesis",
  "compliance_question",
  "unknown_answer"
)

source_types <- c(
  "official_policy",
  "technical_manual",
  "peer_reviewed_paper",
  "internal_note",
  "support_article",
  "archived_document"
)

records <- data.frame(
  eval_id = paste0("RAG-EVAL-", sprintf("%03d", 1:n)),
  query_type = sample(query_types, size = n, replace = TRUE),
  source_type = sample(source_types, size = n, replace = TRUE),
  retrieved_k = sample(3:12, size = n, replace = TRUE),
  relevant_retrieved = sample(0:8, size = n, replace = TRUE),
  supporting_sources = sample(0:5, size = n, replace = TRUE),
  source_authority = runif(n, min = 0.35, max = 1.00),
  freshness_score = runif(n, min = 0.25, max = 1.00),
  grounding_score = runif(n, min = 0.35, max = 1.00),
  citation_fidelity = runif(n, min = 0.30, max = 1.00),
  answer_quality = runif(n, min = 0.45, max = 1.00),
  prompt_injection_resistance = runif(n, min = 0.45, max = 1.00),
  access_control_score = runif(n, min = 0.60, max = 1.00),
  latency_seconds = rgamma(n, shape = 2.3, scale = 1.1),
  total_tokens = sample(1200:12000, size = n, replace = TRUE)
)

records$relevant_retrieved <- pmin(records$relevant_retrieved, records$retrieved_k)
records$retrieval_recall <- records$relevant_retrieved / records$retrieved_k

records$source_authority[records$source_type == "official_policy"] <- pmax(
  records$source_authority[records$source_type == "official_policy"],
  0.80
)

records$freshness_score[records$source_type == "archived_document"] <- pmin(
  records$freshness_score[records$source_type == "archived_document"],
  0.45
)

records$abstained <- ifelse(
  records$query_type == "unknown_answer",
  rbinom(n, size = 1, prob = 0.65),
  rbinom(n, size = 1, prob = 0.10)
)

records$unsupported_answer_risk <- ifelse(
  records$query_type == "unknown_answer",
  1 - records$abstained,
  pmax(0, 0.65 - records$grounding_score)
)

records$retrieval_quality_score <- 0.45 * records$retrieval_recall +
  0.25 * pmin(records$supporting_sources / 3, 1) +
  0.15 * records$source_authority +
  0.15 * records$freshness_score

records$answer_grounding_score <- 0.35 * records$grounding_score +
  0.30 * records$citation_fidelity +
  0.20 * records$answer_quality +
  0.15 * pmin(records$supporting_sources / 3, 1)

records$security_score <- 0.55 * records$prompt_injection_resistance +
  0.45 * records$access_control_score

records$operational_cost_index <- pmin(
  (records$latency_seconds / 10) + (records$total_tokens / 15000),
  1.5
)

records$rag_system_risk <- 0.25 * (1 - records$retrieval_quality_score) +
  0.25 * (1 - records$answer_grounding_score) +
  0.20 * (1 - records$security_score) +
  0.15 * records$unsupported_answer_risk +
  0.15 * records$operational_cost_index

records$review_required <- records$rag_system_risk > 0.42 |
  records$grounding_score < 0.60 |
  records$citation_fidelity < 0.60 |
  records$source_authority < 0.55 |
  records$freshness_score < 0.45 |
  records$prompt_injection_resistance < 0.60 |
  records$access_control_score < 0.75 |
  (records$query_type == "unknown_answer" & records$abstained == 0)

query_summary <- aggregate(
  cbind(
    retrieval_quality_score,
    answer_grounding_score,
    security_score,
    rag_system_risk,
    review_required,
    abstained,
    latency_seconds,
    total_tokens
  ) ~ query_type,
  data = records,
  FUN = mean
)

source_summary <- aggregate(
  cbind(
    source_authority,
    freshness_score,
    retrieval_quality_score,
    answer_grounding_score,
    review_required
  ) ~ source_type,
  data = records,
  FUN = mean
)

governance_summary <- data.frame(
  evaluations_reviewed = nrow(records),
  review_required = sum(records$review_required),
  unknown_answer_cases = sum(records$query_type == "unknown_answer"),
  failed_abstention_cases = sum(records$query_type == "unknown_answer" & records$abstained == 0),
  mean_retrieval_quality = mean(records$retrieval_quality_score),
  mean_answer_grounding = mean(records$answer_grounding_score),
  mean_security_score = mean(records$security_score),
  mean_rag_system_risk = mean(records$rag_system_risk)
)

write.csv(records, file.path(output_dir, "r_rag_evaluation_records.csv"), row.names = FALSE)
write.csv(query_summary, file.path(output_dir, "r_rag_query_type_summary.csv"), row.names = FALSE)
write.csv(source_summary, file.path(output_dir, "r_rag_source_type_summary.csv"), row.names = FALSE)
write.csv(governance_summary, file.path(output_dir, "r_rag_governance_summary.csv"), row.names = FALSE)

print("Query summary")
print(query_summary)

print("Source summary")
print(source_summary)

print("Governance summary")
print(governance_summary)
