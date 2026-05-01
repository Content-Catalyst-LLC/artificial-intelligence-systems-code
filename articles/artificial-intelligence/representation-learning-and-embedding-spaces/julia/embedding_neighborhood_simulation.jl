# Representation Learning and Embedding Spaces
# Julia workflow for embedding simulation and neighborhood diagnostics.
#
# Uses only Julia standard libraries.

using Random
using Statistics
using LinearAlgebra
using Printf

article_dir = joinpath(@__DIR__, "..")
output_dir = joinpath(article_dir, "outputs")

if !isdir(output_dir)
    mkpath(output_dir)
end

function normalize_rows(matrix)
    output = copy(matrix)

    for i in 1:size(output, 1)
        norm_value = norm(output[i, :])
        if norm_value > 0
            output[i, :] ./= norm_value
        end
    end

    return output
end

function simulate_embeddings(n::Int, dim::Int; seed::Int = 42)
    Random.seed!(seed)

    embeddings = randn(n, dim)
    labels = Vector{String}(undef, n)

    for i in 1:n
        group = mod(i, 4) + 1
        labels[i] = "group_$(group)"
        start_index = (group - 1) * 3 + 1
        end_index = min(start_index + 2, dim)
        embeddings[i, start_index:end_index] .+= 1.5
    end

    return normalize_rows(embeddings), labels
end

embeddings, labels = simulate_embeddings(100, 12)
similarity = embeddings * transpose(embeddings)

open(joinpath(output_dir, "julia_embedding_nearest_neighbors.csv"), "w") do io
    println(io, "object_id,label,nearest_neighbor,neighbor_label,similarity,same_label")

    for i in 1:size(similarity, 1)
        scores = copy(similarity[i, :])
        scores[i] = -Inf
        neighbor = argmax(scores)
        same_label = labels[i] == labels[neighbor] ? 1 : 0

        @printf(
            io,
            "%d,%s,%d,%s,%.6f,%d\n",
            i,
            labels[i],
            neighbor,
            labels[neighbor],
            similarity[i, neighbor],
            same_label
        )
    end
end

same_label_rates = Float64[]

for i in 1:size(similarity, 1)
    scores = copy(similarity[i, :])
    scores[i] = -Inf
    neighbor = argmax(scores)
    push!(same_label_rates, labels[i] == labels[neighbor] ? 1.0 : 0.0)
end

open(joinpath(output_dir, "julia_embedding_summary.csv"), "w") do io
    println(io, "mean_similarity,same_label_neighbor_rate")
    @printf(io, "%.6f,%.6f\n", mean(similarity), mean(same_label_rates))
end

println("Julia embedding neighborhood simulation complete.")
println("Same-label neighbor rate: ", round(mean(same_label_rates), digits = 4))
