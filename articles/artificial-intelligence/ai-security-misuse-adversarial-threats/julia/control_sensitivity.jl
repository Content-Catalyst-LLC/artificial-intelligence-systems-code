# Defensive control-effectiveness sensitivity analysis.
# This workflow does not implement attack techniques.

using Random
using Statistics

Random.seed!(42)

n = 1000
exposure = rand(n)
impact = 0.4 .+ 0.6 .* rand(n)
likelihood = rand(n)

control_values = collect(0.10:0.05:0.95)
results = []

for control_strength in control_values
    inherent_risk = exposure .* impact .* likelihood
    residual = inherent_risk .* (1 - control_strength)
    push!(results, (control_strength, mean(residual), maximum(residual)))
end

output_dir = joinpath(@__DIR__, "..", "outputs")
mkpath(output_dir)

open(joinpath(output_dir, "julia_control_sensitivity.csv"), "w") do io
    println(io, "control_strength,mean_residual_risk,max_residual_risk")
    for row in results
        println(io, "$(row[1]),$(row[2]),$(row[3])")
    end
end

println("Control sensitivity analysis complete.")
