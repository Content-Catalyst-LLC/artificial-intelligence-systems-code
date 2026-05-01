# Audit evidence and documentation-gap workflow.
# This script creates synthetic audit evidence records and estimates
# documentation completeness, audit gap, and missing high-weight items.

article_dir <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."), mustWork = FALSE)
output_dir <- file.path(article_dir, "outputs")
dir.create(output_dir, showWarnings = FALSE, recursive = TRUE)

audit_evidence <- data.frame(
  evidence_item = c(
    "system_purpose",
    "data_provenance",
    "model_card",
    "risk_register",
    "evaluation_report",
    "human_oversight_plan",
    "monitoring_logs",
    "incident_response_plan",
    "appeal_and_remedy_process",
    "approval_record"
  ),
  complete = c(1, 0, 1, 1, 0, 1, 0, 1, 0, 1),
  weight = c(0.08, 0.12, 0.12, 0.12, 0.14, 0.10, 0.12, 0.08, 0.08, 0.04)
)

audit_evidence$weighted_completion <-
  audit_evidence$complete * audit_evidence$weight

documentation_completeness <-
  sum(audit_evidence$weighted_completion) / sum(audit_evidence$weight)

audit_gap <- 1 - documentation_completeness

missing_items <- subset(audit_evidence, complete == 0)
missing_items <- missing_items[order(-missing_items$weight), ]

summary_table <- data.frame(
  documentation_completeness = documentation_completeness,
  audit_gap = audit_gap,
  missing_required_items = nrow(missing_items)
)

write.csv(audit_evidence, file.path(output_dir, "audit_evidence_items.csv"), row.names = FALSE)
write.csv(missing_items, file.path(output_dir, "missing_audit_evidence_items.csv"), row.names = FALSE)
write.csv(summary_table, file.path(output_dir, "audit_evidence_gap_summary.csv"), row.names = FALSE)

print(summary_table)
print(missing_items)
