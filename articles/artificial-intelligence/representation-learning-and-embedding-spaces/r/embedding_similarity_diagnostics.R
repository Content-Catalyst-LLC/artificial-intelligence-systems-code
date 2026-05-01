# Representation Learning and Embedding Spaces
# R workflow: similarity, clustering, and embedding diagnostics.

set.seed(42)

article_dir <- normalizePath(file.path(getwd(), "articles/artificial-intelligence/representation-learning-and-embedding-spaces"), mustWork = FALSE)

if (!dir.exists(article_dir)) {
  article_dir <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."), mustWork = FALSE)
}

output_dir <- file.path(article_dir, "outputs")

if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

n_docs <- 80
embedding_dim <- 12

metadata <- data.frame(
  doc_id = paste0("D", sprintf("%03d", 1:n_docs)),
  domain = sample(
    c("AI Systems", "Sustainability", "Infrastructure", "Knowledge Systems"),
    size = n_docs,
    replace = TRUE
  ),
  authority_score = runif(n_docs, min = 0.55, max = 0.98)
)

embeddings <- matrix(rnorm(n_docs * embedding_dim), nrow = n_docs, ncol = embedding_dim)

for (i in 1:n_docs) {
  if (metadata$domain[i] == "AI Systems") {
    embeddings[i, 1:3] <- embeddings[i, 1:3] + 1.2
  } else if (metadata$domain[i] == "Sustainability") {
    embeddings[i, 4:6] <- embeddings[i, 4:6] + 1.2
  } else if (metadata$domain[i] == "Infrastructure") {
    embeddings[i, 7:9] <- embeddings[i, 7:9] + 1.2
  } else {
    embeddings[i, 10:12] <- embeddings[i, 10:12] + 1.2
  }
}

normalize_rows <- function(x) {
  norms <- sqrt(rowSums(x^2))
  x / norms
}

cosine_matrix <- function(x) {
  normalized <- normalize_rows(x)
  normalized %*% t(normalized)
}

similarity <- cosine_matrix(embeddings)

nearest_neighbors <- data.frame()

for (i in 1:n_docs) {
  scores <- similarity[i, ]
  scores[i] <- -Inf
  neighbor_index <- which.max(scores)

  nearest_neighbors <- rbind(
    nearest_neighbors,
    data.frame(
      doc_id = metadata$doc_id[i],
      domain = metadata$domain[i],
      nearest_neighbor = metadata$doc_id[neighbor_index],
      neighbor_domain = metadata$domain[neighbor_index],
      similarity = similarity[i, neighbor_index],
      same_domain = metadata$domain[i] == metadata$domain[neighbor_index]
    )
  )
}

cluster_fit <- kmeans(embeddings, centers = 4, nstart = 20)

cluster_review <- data.frame(
  doc_id = metadata$doc_id,
  domain = metadata$domain,
  cluster = cluster_fit$cluster,
  authority_score = metadata$authority_score
)

cluster_summary <- aggregate(
  authority_score ~ domain + cluster,
  data = cluster_review,
  FUN = mean
)

governance_summary <- data.frame(
  documents_reviewed = n_docs,
  mean_nearest_neighbor_similarity = mean(nearest_neighbors$similarity),
  same_domain_neighbor_rate = mean(nearest_neighbors$same_domain),
  cluster_count = length(unique(cluster_fit$cluster)),
  total_within_cluster_sum_of_squares = cluster_fit$tot.withinss
)

write.csv(nearest_neighbors, file.path(output_dir, "r_nearest_neighbor_review.csv"), row.names = FALSE)
write.csv(cluster_review, file.path(output_dir, "r_embedding_cluster_review.csv"), row.names = FALSE)
write.csv(cluster_summary, file.path(output_dir, "r_embedding_cluster_summary.csv"), row.names = FALSE)
write.csv(governance_summary, file.path(output_dir, "r_embedding_governance_summary.csv"), row.names = FALSE)

print("Nearest-neighbor review")
print(head(nearest_neighbors, 10))

print("Cluster summary")
print(cluster_summary)

print("Governance summary")
print(governance_summary)
