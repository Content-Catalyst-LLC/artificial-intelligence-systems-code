# Audit evidence and documentation-gap workflow.
# This script creates synthetic audit evidence records and estimates
# documentation completeness, audit gap, missing high-weight items,
# and evidence-staleness indicators.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
script_path <- if (length(file_arg) > 0) sub("^--file=", "", file_arg[1]) else getwd()
article_dir <- normalizePath(file.path(dirname(script_path), ".."), mustWork = FALSE)
output_dir <- file.path(article_dir, "outputs")
dir.create(output_dir, showWarnings = FALSE, recursive = TRUE)

audit_evidence <- data.frame(
  evidence_item = c(
    "system_purpose",
    "data_provenance",
    "model_card",
    "system_card",
    "risk_register",
    "evaluation_report",
    "human_oversight_plan",
    "monitoring_logs",
    "incident_response_plan",
    "appeal_and_remedy_process",
    "approval_record",
    "decommissioning_criteria"
  ),
  complete = c(1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0),
  weight = c(0.07, 0.11, 0.11, 0.10, 0.11, 0.13, 0.09, 0.11, 0.07, 0.07, 0.03, 0.00),
  days_since_review = c(20, 180, 75, 210, 45, 160, 60, 120, 30, 140, 25, 240),
  review_interval_days = c(180, 180, 90, 90, 90, 90, 90, 60, 90, 90, 180, 180)
)

audit_evidence$weighted_completion <-
  audit_evidence$complete * audit_evidence$weight

documentation_completeness <-
  sum(audit_evidence$weighted_completion) / sum(audit_evidence$weight)

audit_gap <- 1 - documentation_completeness

audit_evidence$stale <- ifelse(
  audit_evidence$days_since_review > audit_evidence$review_interval_days,
  1,
  0
)

missing_items <- subset(audit_evidence, complete == 0)
missing_items <- missing_items[order(-missing_items$weight), ]

stale_items <- subset(audit_evidence, stale == 1)
stale_items <- stale_items[order(-stale_items$weight), ]

summary_table <- data.frame(
  documentation_completeness = documentation_completeness,
  audit_gap = audit_gap,
  missing_required_items = nrow(missing_items),
  stale_items = nrow(stale_items),
  stale_weight_share = sum(stale_items$weight) / sum(audit_evidence$weight)
)

write.csv(audit_evidence, file.path(output_dir, "audit_evidence_items.csv"), row.names = FALSE)
write.csv(missing_items, file.path(output_dir, "missing_audit_evidence_items.csv"), row.names = FALSE)
write.csv(stale_items, file.path(output_dir, "stale_audit_evidence_items.csv"), row.names = FALSE)
write.csv(summary_table, file.path(output_dir, "audit_evidence_gap_summary.csv"), row.names = FALSE)

print(summary_table)
print(missing_items)
print(stale_items)
