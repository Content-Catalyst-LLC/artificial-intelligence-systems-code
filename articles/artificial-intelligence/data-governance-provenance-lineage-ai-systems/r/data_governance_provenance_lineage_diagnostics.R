# Data Governance, Provenance, and Lineage in AI Systems Diagnostics
#
# This educational workflow simulates:
# - entities and activities
# - data lineage edges
# - quality checks
# - governance review summaries

entities <- data.frame(
  entity_id = c(
    "D_source_A",
    "D_source_B",
    "D_joined_1",
    "F_features_2",
    "M_model_3",
    "R_eval_3",
    "D_deploy_log_3"
  ),
  entity_type = c(
    "source_dataset",
    "source_dataset",
    "derived_dataset",
    "feature_table",
    "model",
    "evaluation_report",
    "deployment_log"
  ),
  version = c("2026-01", "2026-01", "v1", "v2", "v3", "v3", "v3")
)

quality_checks <- data.frame(
  entity_id = c(
    "D_source_A",
    "D_source_B",
    "D_joined_1",
    "F_features_2",
    "M_model_3",
    "R_eval_3",
    "D_deploy_log_3"
  ),
  quality_metric = c(
    "completeness",
    "completeness",
    "schema_validity",
    "missing_rate",
    "external_validation_ready",
    "governance_review_complete",
    "monitoring_ready"
  ),
  value = c(0.96, 0.88, 0.99, 0.07, 1.00, 1.00, 1.00),
  status = c("pass", "warning", "pass", "warning", "pass", "pass", "pass")
)

lineage_edges <- data.frame(
  source = c(
    "D_source_A",
    "D_source_B",
    "D_joined_1",
    "F_features_2",
    "M_model_3",
    "M_model_3"
  ),
  target = c(
    "D_joined_1",
    "D_joined_1",
    "F_features_2",
    "M_model_3",
    "R_eval_3",
    "D_deploy_log_3"
  ),
  transformation = c(
    "join",
    "join",
    "feature_engineering",
    "model_training",
    "evaluation",
    "deployment"
  )
)

governance_reviews <- data.frame(
  entity_id = c(
    "D_source_A",
    "D_source_B",
    "D_joined_1",
    "F_features_2",
    "M_model_3",
    "R_eval_3",
    "D_deploy_log_3"
  ),
  documentation_complete = c(TRUE, FALSE, TRUE, TRUE, TRUE, TRUE, TRUE),
  rights_review_complete = c(TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE),
  quality_review_complete = c(TRUE, FALSE, TRUE, FALSE, TRUE, TRUE, TRUE),
  lineage_review_complete = c(TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE)
)

summary_table <- merge(entities, quality_checks, by = "entity_id")

status_summary <- aggregate(
  entity_id ~ entity_type + status,
  data = summary_table,
  FUN = length
)

names(status_summary)[names(status_summary) == "entity_id"] <- "count"

review_summary <- data.frame(
  metric = c(
    "documentation_completion_rate",
    "rights_review_completion_rate",
    "quality_review_completion_rate",
    "lineage_review_completion_rate"
  ),
  value = c(
    mean(governance_reviews$documentation_complete),
    mean(governance_reviews$rights_review_complete),
    mean(governance_reviews$quality_review_complete),
    mean(governance_reviews$lineage_review_complete)
  )
)

dir.create("../outputs", recursive = TRUE, showWarnings = FALSE)

write.csv(entities, "../outputs/r_lineage_entities.csv", row.names = FALSE)
write.csv(lineage_edges, "../outputs/r_lineage_edges.csv", row.names = FALSE)
write.csv(quality_checks, "../outputs/r_quality_checks.csv", row.names = FALSE)
write.csv(governance_reviews, "../outputs/r_governance_reviews.csv", row.names = FALSE)
write.csv(status_summary, "../outputs/r_status_summary.csv", row.names = FALSE)
write.csv(review_summary, "../outputs/r_review_summary.csv", row.names = FALSE)

print(status_summary)
print(review_summary)
