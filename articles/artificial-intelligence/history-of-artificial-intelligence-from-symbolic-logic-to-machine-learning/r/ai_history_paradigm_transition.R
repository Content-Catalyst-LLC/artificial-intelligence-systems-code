# AI History Paradigm Transition Model
#
# This example creates synthetic paradigm-share curves for educational use.
# It is not a measurement of publication volume or historical influence.

logistic <- function(year, midpoint, steepness) {
  1 / (1 + exp(-steepness * (year - midpoint)))
}

years <- 1950:2026

symbolic_score <- 1.4 * (1 - logistic(years, midpoint = 1990, steepness = 0.08))
statistical_score <- logistic(years, midpoint = 1995, steepness = 0.08) *
  (1 - 0.35 * logistic(years, midpoint = 2015, steepness = 0.15))
deep_learning_score <- logistic(years, midpoint = 2012, steepness = 0.20)
systems_scale_score <- logistic(years, midpoint = 2020, steepness = 0.35)

score_total <- symbolic_score + statistical_score + deep_learning_score + systems_scale_score

paradigm_shares <- data.frame(
  year = years,
  symbolic_ai = symbolic_score / score_total,
  statistical_learning = statistical_score / score_total,
  deep_learning = deep_learning_score / score_total,
  systems_scale_ai = systems_scale_score / score_total
)

dir.create("../outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(paradigm_shares, "../outputs/r_ai_history_paradigm_shares.csv", row.names = FALSE)

print(tail(paradigm_shares))
