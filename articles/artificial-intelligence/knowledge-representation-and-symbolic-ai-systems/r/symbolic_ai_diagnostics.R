# Knowledge Representation and Symbolic AI Diagnostics
#
# This educational workflow simulates:
# - semantic triples
# - model-dataset relations
# - rule coverage
# - inferred governance requirements

facts <- data.frame(
  subject = c("ModelA", "DatasetB", "ModelA", "ModelC", "DatasetD", "ModelC", "ModelE", "DatasetF", "ModelE"),
  predicate = c("type", "type", "trainedOn", "type", "type", "trainedOn", "type", "type", "trainedOn"),
  object = c(
    "HighImpactSystem", "SensitiveDataset", "DatasetB",
    "LowImpactSystem", "PublicDataset", "DatasetD",
    "HighImpactSystem", "SensitiveDataset", "DatasetF"
  )
)

trained_on <- facts[facts$predicate == "trainedOn", ]

has_fact <- function(subject_value, predicate_value, object_value) {
  any(
    facts$subject == subject_value &
      facts$predicate == predicate_value &
      facts$object == object_value
  )
}

inference_rows <- list()

for (i in seq_len(nrow(trained_on))) {
  model <- trained_on$subject[i]
  dataset <- trained_on$object[i]

  if (
    has_fact(model, "type", "HighImpactSystem") &&
    has_fact(dataset, "type", "SensitiveDataset")
  ) {
    inference_rows[[length(inference_rows) + 1]] <- data.frame(
      subject = model,
      predicate = "requires",
      object = "FairnessReview",
      rule_applied = "high_impact_sensitive_data_requires_fairness_review"
    )
  }
}

inferences <- do.call(rbind, inference_rows)

fact_summary <- aggregate(
  subject ~ predicate + object,
  data = facts,
  FUN = length
)

names(fact_summary)[3] <- "fact_count"

rule_summary <- aggregate(
  subject ~ rule_applied,
  data = inferences,
  FUN = length
)

names(rule_summary)[2] <- "trigger_count"

dir.create("../outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(facts, "../outputs/r_symbolic_facts.csv", row.names = FALSE)
write.csv(inferences, "../outputs/r_symbolic_inferences.csv", row.names = FALSE)
write.csv(fact_summary, "../outputs/r_fact_summary.csv", row.names = FALSE)
write.csv(rule_summary, "../outputs/r_rule_summary.csv", row.names = FALSE)

print(fact_summary)
print(rule_summary)
