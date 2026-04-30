# Reinforcement Learning in Dynamic Environments Diagnostics
#
# This educational workflow simulates:
# - episode rewards
# - dynamic reward shifts
# - exploration phases
# - policy performance summaries
# - constraint violation tracking

set.seed(42)

episodes <- 800

rl_results <- data.frame(
  episode = 1:episodes,
  phase = ifelse(1:episodes <= 400, "early_environment", "shifted_environment")
)

rl_results$exploration_rate <- pmax(
  0.05,
  0.30 * exp(-rl_results$episode / 250)
)

rl_results$base_reward <- ifelse(
  rl_results$phase == "early_environment",
  8.0,
  5.5
)

rl_results$total_reward <-
  rl_results$base_reward +
  3.0 * (1 - rl_results$exploration_rate) +
  rnorm(episodes, mean = 0, sd = 1.25)

rl_results$constraint_violation <-
  rbinom(
    episodes,
    size = 1,
    prob = pmin(0.25, rl_results$exploration_rate + 0.03)
  )

rl_results$reached_goal <-
  rbinom(
    episodes,
    size = 1,
    prob = ifelse(
      rl_results$phase == "early_environment",
      0.82,
      0.68
    )
  )

summary_table <- aggregate(
  cbind(
    exploration_rate,
    total_reward,
    constraint_violation,
    reached_goal
  ) ~ phase,
  data = rl_results,
  FUN = mean
)

dir.create("../outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(rl_results, "../outputs/r_rl_dynamic_environment_results.csv", row.names = FALSE)
write.csv(summary_table, "../outputs/r_rl_dynamic_environment_summary.csv", row.names = FALSE)

print(summary_table)
