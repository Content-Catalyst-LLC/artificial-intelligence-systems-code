# Edge AI and Distributed Intelligence Diagnostics
#
# This educational workflow simulates:
# - edge deployment readiness
# - latency and bandwidth diagnostics
# - resource constraint scoring
# - distributed governance risk

set.seed(42)

nodes <- data.frame(
  node_id = paste0("edge_node_", sprintf("%02d", 1:8)),
  compute_capacity = runif(8, 0.45, 0.95),
  model_compute_demand = runif(8, 0.30, 0.90),
  memory_capacity = runif(8, 0.40, 0.95),
  model_memory_demand = runif(8, 0.25, 0.90),
  energy_budget = runif(8, 0.45, 0.95),
  model_energy_demand = runif(8, 0.25, 0.88),
  edge_latency_ms = runif(8, 35, 90),
  cloud_latency_ms = runif(8, 80, 180),
  raw_bandwidth_mb_s = runif(8, 20, 150),
  edge_output_mb_s = runif(8, 1, 8),
  node_trust = runif(8, 0.65, 0.98),
  governance_review = sample(c(0, 1), 8, replace = TRUE, prob = c(0.25, 0.75))
)

nodes$compute_feasible <- nodes$model_compute_demand <= nodes$compute_capacity
nodes$memory_feasible <- nodes$model_memory_demand <= nodes$memory_capacity
nodes$energy_feasible <- nodes$model_energy_demand <= nodes$energy_budget
nodes$latency_feasible <- nodes$edge_latency_ms <= 100

nodes$deployment_feasible <-
  nodes$compute_feasible &
  nodes$memory_feasible &
  nodes$energy_feasible &
  nodes$latency_feasible

nodes$latency_gain <- nodes$cloud_latency_ms - nodes$edge_latency_ms

nodes$bandwidth_savings <- 1 - nodes$edge_output_mb_s / nodes$raw_bandwidth_mb_s

nodes$resource_margin <-
  0.34 * (nodes$compute_capacity - nodes$model_compute_demand) +
  0.33 * (nodes$memory_capacity - nodes$model_memory_demand) +
  0.33 * (nodes$energy_budget - nodes$model_energy_demand)

nodes$distributed_risk <-
  0.35 * (1 - nodes$node_trust) +
  0.30 * (1 - nodes$governance_review) +
  0.20 * (!nodes$deployment_feasible) +
  0.15 * pmax(0, -nodes$resource_margin)

summary_table <- data.frame(
  metric = c(
    "share_deployment_feasible",
    "mean_latency_gain",
    "mean_bandwidth_savings",
    "mean_resource_margin",
    "mean_node_trust",
    "mean_distributed_risk",
    "share_governance_review_complete"
  ),
  value = c(
    mean(nodes$deployment_feasible),
    mean(nodes$latency_gain),
    mean(nodes$bandwidth_savings),
    mean(nodes$resource_margin),
    mean(nodes$node_trust),
    mean(nodes$distributed_risk),
    mean(nodes$governance_review)
  )
)

dir.create("../outputs", recursive = TRUE, showWarnings = FALSE)

write.csv(nodes, "../outputs/r_edge_ai_nodes.csv", row.names = FALSE)
write.csv(summary_table, "../outputs/r_edge_ai_summary.csv", row.names = FALSE)

print(nodes[order(-nodes$distributed_risk), ])
print(summary_table)
