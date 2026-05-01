# Generative AI and Synthetic Content Systems
# Julia workflow for latent-space sampling and quality-risk simulation.
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

function sigmoid(x)
    return 1.0 / (1.0 + exp(-x))
end

function simulate_latent_samples(n::Int; seed::Int = 42)
    Random.seed!(seed)

    z1 = randn(n)
    z2 = randn(n)
    z3 = randn(n)

    quality = sigmoid.(1.2 .* z1 .- 0.4 .* z2 .+ 0.3 .* z3)
    diversity = abs.(z2) ./ maximum(abs.(z2))
    risk = sigmoid.(-1.0 .+ 0.7 .* z2 .+ 0.5 .* abs.(z3))
    provenance = clamp.(0.75 .- 0.25 .* risk .+ randn(n) .* 0.08, 0.0, 1.0)

    return z1, z2, z3, quality, diversity, risk, provenance
end

z1, z2, z3, quality, diversity, risk, provenance = simulate_latent_samples(1000)

open(joinpath(output_dir, "julia_latent_sampling_records.csv"), "w") do io
    println(io, "sample_id,z1,z2,z3,quality_score,diversity_score,risk_score,provenance_score")
    for i in eachindex(z1)
        @printf(
            io,
            "%d,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f\n",
            i,
            z1[i],
            z2[i],
            z3[i],
            quality[i],
            diversity[i],
            risk[i],
            provenance[i]
        )
    end
end

open(joinpath(output_dir, "julia_latent_sampling_summary.csv"), "w") do io
    println(io, "mean_quality,mean_diversity,mean_risk,mean_provenance")
    @printf(io, "%.6f,%.6f,%.6f,%.6f\n", mean(quality), mean(diversity), mean(risk), mean(provenance))
end

println("Julia latent sampling simulation complete.")
println("Mean quality: ", round(mean(quality), digits = 4))
println("Mean risk: ", round(mean(risk), digits = 4))
