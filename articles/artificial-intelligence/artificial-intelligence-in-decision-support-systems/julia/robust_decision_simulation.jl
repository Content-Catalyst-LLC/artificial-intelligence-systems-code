# Artificial Intelligence in Decision Support Systems
# Julia workflow for robust decision simulation and expected-utility scoring.
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

function simulate_options(n::Int; seed::Int = 42)
    Random.seed!(seed)

    risk = rand(n)
    benefit = rand(n) .* 90 .+ 20
    cost = rand(n) .* 40 .+ 10
    uncertainty = rand(n) .* 0.40 .+ 0.05
    equity = rand(n) .< 0.25

    expected_utility = risk .* benefit .- cost .+ 10 .* equity .- 8 .* uncertainty
    robust_utility = expected_utility .- 20 .* uncertainty

    return risk, benefit, cost, uncertainty, equity, expected_utility, robust_utility
end

risk, benefit, cost, uncertainty, equity, expected_utility, robust_utility = simulate_options(200)

ranking = sortperm(robust_utility, rev = true)

open(joinpath(output_dir, "julia_robust_decision_ranking.csv"), "w") do io
    println(io, "option_id,risk,benefit,cost,uncertainty,equity_priority,expected_utility,robust_utility")
    for idx in ranking
        @printf(
            io,
            "%d,%.6f,%.6f,%.6f,%.6f,%d,%.6f,%.6f\n",
            idx,
            risk[idx],
            benefit[idx],
            cost[idx],
            uncertainty[idx],
            equity[idx] ? 1 : 0,
            expected_utility[idx],
            robust_utility[idx]
        )
    end
end

open(joinpath(output_dir, "julia_decision_summary.csv"), "w") do io
    println(io, "mean_expected_utility,mean_robust_utility,best_robust_utility")
    @printf(io, "%.6f,%.6f,%.6f\n", mean(expected_utility), mean(robust_utility), maximum(robust_utility))
end

println("Julia robust decision simulation complete.")
println("Best robust utility: ", round(maximum(robust_utility), digits = 4))
