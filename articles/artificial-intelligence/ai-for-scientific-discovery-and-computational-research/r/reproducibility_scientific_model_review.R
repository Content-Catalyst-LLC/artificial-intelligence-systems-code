# AI for Scientific Discovery and Computational Research
# R workflow: reproducibility and scientific model review.

set.seed(42)

article_dir <- normalizePath(file.path(getwd(), "articles/artificial-intelligence/ai-for-scientific-discovery-and-computational-research"), mustWork = FALSE)

if (!dir.exists(article_dir)) {
  article_dir <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."), mustWork = FALSE)
}

output_dir <- file.path(article_dir, "outputs")

if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

simulate_scientific_data <- function(n = 500, seed = 1) {
  set.seed(seed)

  x1 <- runif(n)
  x2 <- runif(n)
  x3 <- runif(n)

  y <- 1.5 * sin(pi * x1) +
    0.8 * x2^2 -
    0.6 * x3 +
    rnorm(n, mean = 0, sd = 0.10)

  data.frame(
    x1 = x1,
    x2 = x2,
    x3 = x3,
    y = y
  )
}

fit_review_model <- function(data) {
  model <- lm(y ~ x1 + x2 + x3 + I(x1^2) + I(x2^2), data = data)

  coefficients <- coef(model)
  rmse <- sqrt(mean(residuals(model)^2))

  data.frame(
    intercept = coefficients["(Intercept)"],
    x1 = coefficients["x1"],
    x2 = coefficients["x2"],
    x3 = coefficients["x3"],
    x1_squared = coefficients["I(x1^2)"],
    x2_squared = coefficients["I(x2^2)"],
    rmse = rmse
  )
}

runs <- list()

for (seed in 1:30) {
  data <- simulate_scientific_data(n = 500, seed = seed)
  runs[[seed]] <- fit_review_model(data)
}

review <- do.call(rbind, runs)
review$run_id <- 1:nrow(review)

stability_summary <- data.frame(
  metric = names(review)[names(review) != "run_id"],
  mean_value = sapply(review[names(review) != "run_id"], mean),
  sd_value = sapply(review[names(review) != "run_id"], sd),
  coefficient_of_variation = sapply(review[names(review) != "run_id"], function(x) {
    sd(x) / abs(mean(x))
  })
)

write.csv(review, file.path(output_dir, "r_reproducibility_runs.csv"), row.names = FALSE)
write.csv(stability_summary, file.path(output_dir, "r_reproducibility_stability_summary.csv"), row.names = FALSE)

print("Reproducibility stability summary")
print(stability_summary)
