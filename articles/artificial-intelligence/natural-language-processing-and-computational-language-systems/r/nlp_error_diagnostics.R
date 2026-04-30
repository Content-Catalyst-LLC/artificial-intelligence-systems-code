# NLP Error Diagnostics
#
# This educational workflow simulates classification error rates across
# synthetic document domains and language varieties.

set.seed(42)

n <- 1500

nlp_eval <- data.frame(
  document_domain = sample(c("technical", "legal", "general"), n, replace = TRUE, prob = c(0.35, 0.25, 0.40)),
  language_variety = sample(c("standard", "specialized", "informal"), n, replace = TRUE),
  target = rbinom(n, size = 1, prob = 0.45)
)

domain_error <- ifelse(
  nlp_eval$document_domain == "general", 0.08,
  ifelse(nlp_eval$document_domain == "technical", 0.14, 0.18)
)

variety_error <- ifelse(
  nlp_eval$language_variety == "standard", 1.00,
  ifelse(nlp_eval$language_variety == "specialized", 1.25, 1.15)
)

error_probability <- pmin(domain_error * variety_error, 0.90)

is_error <- rbinom(n, size = 1, prob = error_probability)

nlp_eval$prediction <- ifelse(
  is_error == 1,
  1 - nlp_eval$target,
  nlp_eval$target
)

nlp_eval$error <- nlp_eval$prediction != nlp_eval$target

group_summary <- aggregate(
  error ~ document_domain + language_variety,
  data = nlp_eval,
  FUN = mean
)

names(group_summary)[3] <- "classification_error_rate"

dir.create("../outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(group_summary, "../outputs/r_nlp_error_diagnostics.csv", row.names = FALSE)

print(group_summary)
