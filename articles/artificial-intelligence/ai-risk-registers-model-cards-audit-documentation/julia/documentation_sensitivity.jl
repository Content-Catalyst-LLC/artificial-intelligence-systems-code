# Documentation-completeness sensitivity analysis.

using Random
using Statistics

Random.seed!(42)

n = 1000
likelihood = rand(n)
impact = 0.3 .+ 0.7 .* rand(n)
mitigation_strength = rand(n)

documentation_values = collect(0.10:0.05:0.95)
results = []

for completeness in documentation_values
    residual_risk = likelihood .* impact .* (1 .- mitigation_strength)
    documentation_priority = residual_risk .* (1 - completeness)
    push!(results, (completeness, mean(documentation_priority)))
end

output_dir = joinpath(@__DIR__, "..", "outputs")
mkpath(output_dir)

open(joinpath(output_dir, "julia_documentation_sensitivity.csv"), "w") do io
    println(io, "documentation_completeness,mean_documentation_priority")
    for row in results
        println(io, "$(row[1]),$(row[2])")
    end
end

println("Documentation sensitivity analysis complete.")
