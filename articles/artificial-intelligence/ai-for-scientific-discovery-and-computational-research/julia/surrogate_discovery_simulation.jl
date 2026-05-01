# AI for Scientific Discovery and Computational Research
# Julia workflow for surrogate simulation and discovery optimization.
#
# Uses only Julia standard libraries.

using Random
using Statistics
using Printf
using LinearAlgebra

article_dir = joinpath(@__DIR__, "..")
output_dir = joinpath(article_dir, "outputs")

if !isdir(output_dir)
    mkpath(output_dir)
end

function create_candidates(n::Int; seed::Int = 42)
    Random.seed!(seed)

    x1 = rand(n)
    x2 = rand(n)
    x3 = rand(n)

    y = 1.8 .* sin.(pi .* x1) .+
        1.1 .* cos.(pi .* x2) .+
        0.7 .* x3.^2 .+
        randn(n) .* 0.05

    return x1, x2, x3, y
end

function design_matrix(x1, x2, x3)
    n = length(x1)
    return hcat(
        ones(n),
        x1,
        x2,
        x3,
        x1.^2,
        x2.^2,
        x3.^2,
        x1 .* x2
    )
end

function ridge_fit(X, y; lambda::Float64 = 0.01)
    p = size(X, 2)
    penalty = Matrix{Float64}(I, p, p)
    penalty[1, 1] = 0.0
    return (X' * X + lambda * penalty) \ (X' * y)
end

x1, x2, x3, y = create_candidates(1000)
observed = collect(1:80)

X_obs = design_matrix(x1[observed], x2[observed], x3[observed])
beta = ridge_fit(X_obs, y[observed])

X_all = design_matrix(x1, x2, x3)
prediction = X_all * beta

uncertainty = abs.(x1 .- mean(x1[observed])) .+
    abs.(x2 .- mean(x2[observed])) .+
    abs.(x3 .- mean(x3[observed]))

uncertainty = uncertainty ./ maximum(uncertainty)

acquisition = 0.70 .* prediction .+ 0.30 .* uncertainty

ranking = sortperm(acquisition, rev = true)[1:50]

open(joinpath(output_dir, "julia_surrogate_candidate_ranking.csv"), "w") do io
    println(io, "candidate_id,prediction,uncertainty,acquisition,true_property")
    for idx in ranking
        @printf(io, "%d,%.6f,%.6f,%.6f,%.6f\n", idx, prediction[idx], uncertainty[idx], acquisition[idx], y[idx])
    end
end

open(joinpath(output_dir, "julia_surrogate_summary.csv"), "w") do io
    println(io, "mean_prediction,mean_true_property,best_true_property")
    @printf(io, "%.6f,%.6f,%.6f\n", mean(prediction), mean(y), maximum(y[ranking]))
end

println("Julia surrogate discovery simulation complete.")
println("Best selected true property: ", round(maximum(y[ranking]), digits = 4))
