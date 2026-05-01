# Oversight threshold sensitivity analysis in Julia

using Random
using Statistics
using DelimitedFiles

Random.seed!(42)

n = 1000
uncertainty = rand(n) .^ 2
harm_probability = rand(n) .* 0.5
harm_impact = 0.1 .+ rand(n) .* 0.9
expected_risk = harm_probability .* harm_impact

risk_thresholds = collect(0.05:0.01:0.30)
uncertainty_threshold = 0.55

results = []

for threshold in risk_thresholds
    escalate = (expected_risk .>= threshold) .| (uncertainty .>= uncertainty_threshold)
    push!(results, (threshold, mean(escalate)))
end

output_dir = joinpath(@__DIR__, "..", "outputs")
mkpath(output_dir)

open(joinpath(output_dir, "julia_threshold_sensitivity.csv"), "w") do io
    println(io, "risk_threshold,escalation_rate")
    for row in results
        println(io, "$(row[1]),$(row[2])")
    end
end

println("Threshold sensitivity analysis complete.")
