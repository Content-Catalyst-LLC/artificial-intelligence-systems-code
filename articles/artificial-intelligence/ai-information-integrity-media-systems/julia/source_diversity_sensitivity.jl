# Source-diversity sensitivity analysis.
# This workflow demonstrates how source concentration affects entropy.

using Random
using Statistics

Random.seed!(42)

function entropy(shares)
    safe = filter(x -> x > 0, shares)
    return -sum(safe .* log.(safe))
end

concentration_values = collect(0.20:0.05:0.90)
results = []

for dominant_share in concentration_values
    remaining = 1.0 - dominant_share
    other_shares = fill(remaining / 5, 5)
    shares = vcat([dominant_share], other_shares)
    diversity = entropy(shares)
    concentration_index = sum(shares .^ 2)

    push!(results, (dominant_share, diversity, concentration_index))
end

output_dir = joinpath(@__DIR__, "..", "outputs")
mkpath(output_dir)

open(joinpath(output_dir, "julia_source_diversity_sensitivity.csv"), "w") do io
    println(io, "dominant_source_share,source_diversity_entropy,source_concentration_index")
    for row in results
        println(io, "$(row[1]),$(row[2]),$(row[3])")
    end
end

println("Source diversity sensitivity analysis complete.")
