# Computer Vision Error Diagnostics
#
# This educational workflow simulates classification error rates across
# synthetic image groups and lighting conditions.

set.seed(42)

n <- 1500

vision_eval <- data.frame(
  image_group = sample(c("A", "B", "C"), n, replace = TRUE, prob = c(0.5, 0.3, 0.2)),
  lighting_condition = sample(c("normal", "low_light", "harsh_light"), n, replace = TRUE),
  target = rbinom(n, size = 1, prob = 0.4)
)

lighting_error <- ifelse(
  vision_eval$lighting_condition == "normal", 0.08,
  ifelse(vision_eval$lighting_condition == "low_light", 0.18, 0.14)
)

group_error <- ifelse(
  vision_eval$image_group == "A", 1.00,
  ifelse(vision_eval$image_group == "B", 1.20, 1.35)
)

error_probability <- pmin(lighting_error * group_error, 0.90)

is_error <- rbinom(n, size = 1, prob = error_probability)

vision_eval$prediction <- ifelse(
  is_error == 1,
  1 - vision_eval$target,
  vision_eval$target
)

vision_eval$error <- vision_eval$prediction != vision_eval$target

group_summary <- aggregate(
  error ~ image_group + lighting_condition,
  data = vision_eval,
  FUN = mean
)

names(group_summary)[3] <- "classification_error_rate"

dir.create("../outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(group_summary, "../outputs/r_vision_error_diagnostics.csv", row.names = FALSE)

print(group_summary)
