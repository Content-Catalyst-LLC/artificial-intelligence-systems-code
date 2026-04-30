# Learning Paradigm Diagnostics
#
# This educational workflow simulates diagnostic differences across
# supervised, unsupervised, and reinforcement learning settings.

set.seed(42)

n <- 1200

paradigm_eval <- data.frame(
  paradigm = sample(
    c("supervised", "unsupervised", "reinforcement"),
    n,
    replace = TRUE,
    prob = c(0.45, 0.30, 0.25)
  ),
  signal_quality = sample(
    c("high", "medium", "low"),
    n,
    replace = TRUE,
    prob = c(0.40, 0.40, 0.20)
  )
)

base_risk <- ifelse(
  paradigm_eval$paradigm == "supervised", 0.10,
  ifelse(paradigm_eval$paradigm == "unsupervised", 0.16, 0.22)
)

signal_multiplier <- ifelse(
  paradigm_eval$signal_quality == "high", 0.75,
  ifelse(paradigm_eval$signal_quality == "medium", 1.00, 1.45)
)

paradigm_eval$failure_probability <- pmin(base_risk * signal_multiplier, 0.90)
paradigm_eval$failure_event <- rbinom(n, size = 1, prob = paradigm_eval$failure_probability)

summary_table <- aggregate(
  failure_event ~ paradigm + signal_quality,
  data = paradigm_eval,
  FUN = mean
)

names(summary_table)[3] <- "simulated_failure_rate"

dir.create("../outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(summary_table, "../outputs/r_learning_paradigm_diagnostics.csv", row.names = FALSE)

print(summary_table)
