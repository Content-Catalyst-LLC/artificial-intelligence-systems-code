# Governance-control sensitivity analysis for residual rights risk.

using Random
using Statistics

Random.seed!(42)

n = 1000
harm_probability = rand(n)
harm_impact = 0.3 .+ 0.7 .* rand(n)
vulnerability_exposure = rand(n)
institutional_power = rand(n)

control_values = collect(0.10:0.05:0.95)
results = []

for control_strength in control_values
    inherent =
        0.30 .* harm_probability .+
        0.30 .* harm_impact .+
        0.20 .* vulnerability_exposure .+
        0.20 .* institutional_power

    residual = inherent .* (1 - control_strength)
    high_risk_share = mean(residual .>= 0.35)
    push!(results, (control_strength, mean(residual), maximum(residual), high_risk_share))
end

output_dir = joinpath(@__DIR__, "..", "outputs")
mkpath(output_dir)

open(joinpath(output_dir, "julia_governance_control_sensitivity.csv"), "w") do io
    println(io, "governance_control_strength,mean_residual_rights_risk,max_residual_rights_risk,high_risk_share")
    for row in results
        println(io, "$(row[1]),$(row[2]),$(row[3]),$(row[4])")
    end
end

println("Governance-control sensitivity analysis complete.")
