# Speech Recognition Error Diagnostics
#
# This educational workflow simulates word error rates across
# synthetic groups and noise conditions.

set.seed(42)

n <- 1000

speech_eval <- data.frame(
  speaker_group = sample(c("A", "B", "C"), n, replace = TRUE, prob = c(0.5, 0.3, 0.2)),
  noise_condition = sample(c("clean", "moderate_noise", "high_noise"), n, replace = TRUE),
  reference_words = sample(5:30, n, replace = TRUE)
)

noise_multiplier <- ifelse(
  speech_eval$noise_condition == "clean", 0.05,
  ifelse(speech_eval$noise_condition == "moderate_noise", 0.12, 0.22)
)

group_multiplier <- ifelse(
  speech_eval$speaker_group == "A", 1.00,
  ifelse(speech_eval$speaker_group == "B", 1.15, 1.35)
)

expected_errors <- speech_eval$reference_words * noise_multiplier * group_multiplier

speech_eval$substitutions <- rpois(n, expected_errors * 0.45)
speech_eval$deletions <- rpois(n, expected_errors * 0.35)
speech_eval$insertions <- rpois(n, expected_errors * 0.20)

speech_eval$wer <- (
  speech_eval$substitutions +
    speech_eval$deletions +
    speech_eval$insertions
) / speech_eval$reference_words

group_summary <- aggregate(
  wer ~ speaker_group + noise_condition,
  data = speech_eval,
  FUN = mean
)

names(group_summary)[3] <- "mean_word_error_rate"

dir.create("../outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(group_summary, "../outputs/r_speech_error_diagnostics.csv", row.names = FALSE)

print(group_summary)
