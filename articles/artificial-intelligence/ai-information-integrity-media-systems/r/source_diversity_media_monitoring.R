# Source diversity and media-system monitoring workflow.
# This script creates synthetic media events and estimates source diversity,
# provenance coverage, correction effectiveness, and low-integrity amplification.

set.seed(42)

args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
script_path <- if (length(file_arg) > 0) sub("^--file=", "", file_arg[1]) else getwd()
article_dir <- normalizePath(file.path(dirname(script_path), ".."), mustWork = FALSE)
output_dir <- file.path(article_dir, "outputs")
dir.create(output_dir, showWarnings = FALSE, recursive = TRUE)

n <- 800

media_events <- data.frame(
  event_id = 1:n,
  source_type = sample(
    c(
      "public_media",
      "local_news",
      "national_news",
      "platform_creator",
      "official_source",
      "unknown_source"
    ),
    n,
    replace = TRUE,
    prob = c(0.15, 0.15, 0.25, 0.25, 0.10, 0.10)
  ),
  content_type = sample(
    c(
      "article",
      "short_video",
      "news_summary",
      "synthetic_image",
      "health_claim",
      "public_update"
    ),
    n,
    replace = TRUE
  ),
  views = round(rlnorm(n, meanlog = 8, sdlog = 1)),
  provenance_available = sample(c(0, 1), n, replace = TRUE, prob = c(0.45, 0.55)),
  ai_generated_or_assisted = sample(c(0, 1), n, replace = TRUE, prob = c(0.65, 0.35)),
  low_integrity_signal = runif(n, 0, 1),
  correction_reach = round(rlnorm(n, meanlog = 6, sdlog = 1)),
  original_reach = round(rlnorm(n, meanlog = 8, sdlog = 1)),
  human_reviewed = sample(c(0, 1), n, replace = TRUE, prob = c(0.35, 0.65))
)

source_attention <- aggregate(
  views ~ source_type,
  data = media_events,
  FUN = sum
)

source_attention$attention_share <- source_attention$views / sum(source_attention$views)

source_diversity <- -sum(
  source_attention$attention_share * log(source_attention$attention_share)
)

provenance_coverage <- mean(media_events$provenance_available)

ai_provenance_coverage <- mean(
  media_events$provenance_available[media_events$ai_generated_or_assisted == 1]
)

correction_effectiveness <- sum(media_events$correction_reach) /
  sum(media_events$original_reach)

low_integrity_amplification <- mean(
  media_events$low_integrity_signal * media_events$views / max(media_events$views)
)

review_coverage <- mean(media_events$human_reviewed)

summary_table <- data.frame(
  source_diversity = source_diversity,
  provenance_coverage = provenance_coverage,
  ai_provenance_coverage = ai_provenance_coverage,
  correction_effectiveness = correction_effectiveness,
  low_integrity_amplification = low_integrity_amplification,
  review_coverage = review_coverage
)

source_integrity <- aggregate(
  cbind(
    provenance_available,
    low_integrity_signal,
    human_reviewed,
    ai_generated_or_assisted
  ) ~ source_type,
  data = media_events,
  FUN = mean
)

write.csv(media_events, file.path(output_dir, "synthetic_media_events.csv"), row.names = FALSE)
write.csv(source_attention, file.path(output_dir, "source_attention_summary.csv"), row.names = FALSE)
write.csv(source_integrity, file.path(output_dir, "source_integrity_summary.csv"), row.names = FALSE)
write.csv(summary_table, file.path(output_dir, "media_integrity_monitoring_summary.csv"), row.names = FALSE)

print(source_attention)
print(source_integrity)
print(summary_table)
