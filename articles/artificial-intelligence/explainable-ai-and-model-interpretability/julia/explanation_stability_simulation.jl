# Explainable AI and Model Interpretability
# Julia simulation for explanation stability and counterfactual distance.
#
# Uses only Julia standard libraries.

using Random
using Statistics
using Printf

article_dir = joinpath(@__DIR__, "..")
output_dir = joinpath(article_dir, "outputs")

if !isdir(output_dir)
    mkpath(output_dir)
end

function simulate_explanation_vectors(n_cases::Int, n_features::Int; seed::Int = 42)
    Random.seed!(seed)

    base = randn(n_cases, n_features)
    noise = randn(n_cases, n_features) .* 0.15
    repeated = base .+ noise

    distances = sqrt.(sum((base .- repeated).^2, dims = 2))
    stability = 1.0 ./ (1.0 .+ vec(distances))

    return stability
end

function simulate_counterfactual_distances(n_cases::Int; seed::Int = 7)
    Random.seed!(seed)

    distances = abs.(randn(n_cases) .* 0.35 .+ 0.65)
    plausibility = clamp.(1.0 .- distances ./ maximum(distances), 0.0, 1.0)
    actionability = clamp.(plausibility .+ randn(n_cases) .* 0.08, 0.0, 1.0)

    return distances, plausibility, actionability
end

stability = simulate_explanation_vectors(1000, 8)
distances, plausibility, actionability = simulate_counterfactual_distances(1000)

open(joinpath(output_dir, "julia_explanation_stability.csv"), "w") do io
    println(io, "case_id,stability_score")
    for i in eachindex(stability)
        @printf(io, "%d,%.6f\n", i, stability[i])
    end
end

open(joinpath(output_dir, "julia_counterfactual_quality.csv"), "w") do io
    println(io, "case_id,counterfactual_distance,plausibility_score,actionability_score")
    for i in eachindex(distances)
        @printf(io, "%d,%.6f,%.6f,%.6f\n", i, distances[i], plausibility[i], actionability[i])
    end
end

println("Julia explanation stability simulation complete.")
println("Mean stability score: ", round(mean(stability), digits = 4))
println("Mean actionability score: ", round(mean(actionability), digits = 4))
